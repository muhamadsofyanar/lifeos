"""LifeOS single-user service. Run behind a TLS reverse proxy."""
import os, json, sqlite3, secrets, hashlib, hmac, time, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import urlsplit

ROOT = Path(__file__).parent
DATA = Path(os.environ.get('DATA_DIR', str(ROOT / 'data')))
DATA.mkdir(parents=True, exist_ok=True)
PASSWORD = os.environ.get('LIFEOS_PASSWORD', '')
SECURE = os.environ.get('COOKIE_SECURE', 'true').lower() == 'true'
SALT = secrets.token_bytes(16)
PASSWORD_HASH = hashlib.scrypt(PASSWORD.encode(), salt=SALT, n=16384, r=8, p=1)
SESSIONS, ATTEMPTS = {}, []
LOCK = threading.Lock()
KINDS = ['inbox', 'tasks', 'projects', 'notes', 'events', 'sessions', 'reviews', 'areas', 'goals']

def connect():
    db = sqlite3.connect(DATA / 'lifeos.db', timeout=20)
    db.execute('PRAGMA journal_mode=WAL')
    return db

with connect() as db:
    db.execute('CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, body TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS history (revision INTEGER PRIMARY KEY, created TEXT DEFAULT CURRENT_TIMESTAMP, body TEXT NOT NULL)')
    db.execute('INSERT OR IGNORE INTO state VALUES(1,0,?)', (json.dumps({k: [] for k in KINDS}),))

def validate(data):
    if not isinstance(data, dict) or set(data) != set(KINDS):
        raise ValueError('Struktur backup tidak sesuai.')
    for k in KINDS:
        if not isinstance(data[k], list) or len(data[k]) > 20000:
            raise ValueError('Data tidak valid atau terlalu besar.')
        ids = set()
        for item in data[k]:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or item['id'] in ids:
                raise ValueError('ID data tidak valid atau duplikat.')
            ids.add(item['id'])
    active = [s for s in data['sessions'] if not s.get('end')]
    if len(active) > 1:
        raise ValueError('Hanya satu timer boleh aktif.')

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def reply(self, code, obj, cookie=None):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.headers_common('application/json; charset=utf-8')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def headers_common(self, mime):
        self.send_header('Content-Type', mime)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'same-origin')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")

    def session(self):
        try:
            c = SimpleCookie(self.headers.get('Cookie', ''))
            token = c['lifeos'].value
            with LOCK:
                entry = SESSIONS.get(token)
                if entry and entry['expires'] > time.time(): return token, entry
        except (KeyError, ValueError): pass
        return None, None

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/health': return self.reply(200, {'ok': True})
        if path.startswith('/api/'):
            _, session = self.session()
            if not session: return self.reply(401, {'error': 'Silakan masuk.'})
            if path == '/api/state':
                with connect() as db: row = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
                return self.reply(200, {'revision': row[0], 'data': json.loads(row[1]), 'csrf': session['csrf']})
            if path == '/api/history':
                with connect() as db: rows = db.execute('SELECT revision,created FROM history ORDER BY revision DESC LIMIT 30').fetchall()
                return self.reply(200, {'history': [{'revision': r, 'created': d} for r,d in rows]})
            return self.reply(404, {'error': 'Tidak ditemukan.'})
        files = {'/': ('index.html', 'text/html; charset=utf-8'), '/app.js': ('app.js', 'text/javascript; charset=utf-8'), '/style.css': ('style.css', 'text/css; charset=utf-8'), '/manifest.json': ('manifest.json', 'application/manifest+json'), '/icon.svg': ('icon.svg', 'image/svg+xml')}
        if path not in files: return self.reply(404, {'error': 'Tidak ditemukan.'})
        filename, mime = files[path]
        content = (ROOT / 'static' / filename).read_bytes()
        self.send_response(200); self.headers_common(mime)
        self.send_header('Content-Length', str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_POST(self):
        try:
            # Require same-origin JSON; cross-site HTML forms cannot write.
            if self.headers.get('Sec-Fetch-Site') == 'cross-site': return self.reply(403, {'error': 'Origin ditolak.'})
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json': return self.reply(415, {'error': 'JSON diperlukan.'})
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 8_000_000: return self.reply(413, {'error': 'Ukuran data tidak sesuai.'})
            obj = json.loads(self.rfile.read(size))
            if not isinstance(obj, dict): raise ValueError('JSON object diperlukan.')
            path = urlsplit(self.path).path
            if path == '/api/login':
                now = time.time()
                with LOCK:
                    ATTEMPTS[:] = [t for t in ATTEMPTS if t > now-300]
                    if len(ATTEMPTS) >= 15: return self.reply(429, {'error': 'Terlalu banyak percobaan. Tunggu 5 menit.'})
                    ATTEMPTS.append(now)
                candidate = obj.get('password', '')
                if not isinstance(candidate, str) or len(candidate)>1024: raise ValueError('Password tidak valid.')
                digest = hashlib.scrypt(candidate.encode(), salt=SALT, n=16384, r=8, p=1)
                if not PASSWORD or not hmac.compare_digest(digest, PASSWORD_HASH): return self.reply(401, {'error': 'Password salah.'})
                token = secrets.token_urlsafe(32)
                with LOCK:
                    for key in list(SESSIONS):
                        if SESSIONS[key]['expires'] < now: del SESSIONS[key]
                    SESSIONS[token] = {'expires': now+604800, 'csrf': secrets.token_urlsafe(32)}
                return self.reply(200, {'ok': True}, f'lifeos={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800' + ('; Secure' if SECURE else ''))
            token, session = self.session()
            if not session: return self.reply(401, {'error': 'Silakan masuk.'})
            if not hmac.compare_digest(self.headers.get('X-CSRF-Token',''), session['csrf']): return self.reply(403, {'error': 'Token keamanan tidak sesuai. Muat ulang.'})
            if path == '/api/logout':
                with LOCK: SESSIONS.pop(token, None)
                return self.reply(200, {'ok':True}, 'lifeos=; Path=/; Max-Age=0; HttpOnly; SameSite=Strict')
            if path == '/api/state':
                validate(obj.get('data'))
                with connect() as db:
                    db.execute('BEGIN IMMEDIATE')
                    rev, old = db.execute('SELECT revision,body FROM state WHERE id=1').fetchone()
                    if obj.get('revision') != rev: return self.reply(409, {'error': 'Ada perubahan dari tab/perangkat lain. Muat ulang sebelum mengedit.'})
                    db.execute('INSERT INTO history(revision,body) VALUES(?,?)', (rev,old))
                    db.execute('DELETE FROM history WHERE revision < ?', (rev-29,))
                    db.execute('UPDATE state SET revision=?,body=? WHERE id=1', (rev+1,json.dumps(obj['data'])))
                return self.reply(200, {'revision': rev+1})
            return self.reply(404, {'error':'Tidak ditemukan.'})
        except (ValueError, TypeError) as e: self.reply(400, {'error':str(e)})
        except Exception: self.reply(500, {'error':'Server gagal menyimpan. Coba lagi.'})

if __name__ == '__main__':
    if len(PASSWORD) < 12: raise SystemExit('Set LIFEOS_PASSWORD minimal 12 karakter sebelum menjalankan server.')
    ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT','8000'))), Handler).serve_forever()
