// Optional browser regression suite. Requires Playwright with Chromium installed.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');
const {once} = require('node:events');
const net = require('node:net');
const playwright = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'playwright'))
  : require('playwright');

(async () => {
  const probe = net.createServer();
  probe.listen(0, '127.0.0.1');
  await once(probe, 'listening');
  const port = probe.address().port;
  await new Promise(resolve => probe.close(resolve));
  const root = path.resolve(__dirname, '..');
  const temp = fs.mkdtempSync(path.join(root, '.browser-fixture-'));
  const password = 'browser-fixture-password';
  const server = spawn('python3', ['server.py'], {
    cwd: root,
    env: {...process.env, DATA_DIR: temp, PORT: String(port), LIFEOS_PASSWORD: password, COOKIE_SECURE: 'false'},
    stdio: ['ignore', 'ignore', 'pipe'],
  });
  let browser;
  let serverErrors = '';
  server.stderr.on('data', chunk => { serverErrors += chunk; });
  try {
    const origin = `http://127.0.0.1:${port}`;
    for (let attempt = 0; attempt < 60; attempt++) {
      try { if ((await fetch(origin + '/api/health')).ok) break; } catch {}
      if (attempt === 59) throw Error('Server unavailable: ' + serverErrors);
      await new Promise(resolve => setTimeout(resolve, 50));
    }
    browser = await playwright.chromium.launch({headless: true, args: ['--no-sandbox']});
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('dialog', dialog => dialog.accept());
    await page.goto(origin);
    await page.locator('#login [name=password]').fill(password);
    await page.locator('#login button').click();
    await page.locator('nav').waitFor();
    const fixtureDay = await page.evaluate(() => today());
    await page.evaluate(async date => {
      const state = await api('state');
      state.data.projects = [{id:'p" data-injected="yes', title:'Imported project'}];
      state.data.quran = [{id:'101:1',surah:101,ayah:1,status:'practiced',date}];
      state.data.quranSessions = [
        {id:'s1',date,minutes:20,surah:101,from:1,to:11,mode:'Hafalan baru + murajaah',status:'practiced',created:1},
        {id:'s2',date,minutes:20,surah:102,from:1,to:8,mode:'Hafalan baru + murajaah',status:'practiced',created:2},
      ];
      await api('state', {revision:state.revision,data:state.data});
      await load();
    }, fixtureDay);

    // Invalid backup cannot replace the currently committed revision.
    assert.deepEqual(await page.evaluate(async date => {
      const before = await api('state');
      const invalid = structuredClone(before.data);
      invalid.events = [{id:'bad',date,time:null}];
      const response = await fetch('/api/state', {method:'POST', headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({revision:before.revision,data:invalid})});
      const after = await api('state');
      return [response.status, after.revision === before.revision, JSON.stringify(after.data) === JSON.stringify(before.data)];
    }, fixtureDay), [400, true, true]);

    await page.locator('nav [data-id="Sullamul Hifz"]').click();
    assert.equal(await page.locator('.session-card').count(), 2);
    assert.equal(await page.locator('.session-card p').filter({hasText:/^\s*·\s*$/}).count(), 0);
    assert.equal(await page.locator('.session-note').count(), 0);
    const cardHeight = await page.locator('.session-card').first().evaluate(el => el.getBoundingClientRect().height);
    assert.ok(cardHeight < 220, `Unexpected blank card height: ${cardHeight}`);

    // Correcting a session defaults to preserving present mutabaah state.
    await page.locator('[data-action=q-log-edit][data-id=s1]').click();
    assert.equal(await page.locator('[name=updateProgress]').isChecked(), false);
    await page.locator('#modal [name=status]').selectOption('teacher');
    await page.locator('#modal [name=teacher]').fill('Penyimak fixture');
    await page.locator('#modal [name=minutes]').fill('25');
    await page.locator('#modal [name=checked]').check();
    await page.locator('#feature-form button[type=submit]').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    assert.deepEqual(await page.evaluate(async () => {
      const state = await api('state');
      return [state.data.quranSessions.find(s=>s.id==='s1').minutes,state.data.quran[0].status];
    }), [25, 'practiced']);

    await page.locator('[data-action=q-log-edit][data-id=s1]').click();
    await page.locator('#modal [name=updateProgress]').check();
    await page.locator('#modal [name=checked]').check();
    await page.locator('#feature-form button[type=submit]').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    assert.equal(await page.evaluate(async () => (await api('state')).data.quran.filter(q=>q.status==='teacher').length), 11);

    // Two pages and their connection have independent assessments.
    await page.locator('#h-juz').selectOption('1');
    await page.locator('[data-action=h-log]').click();
    await page.locator('#modal [name=status]').selectOption('self');
    await page.locator('#feature-form button[type=submit]').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    const unitLog = await page.evaluate(async () => (await api('state')).data.quranUnitSessions[0]);
    assert.deepEqual(unitLog.units, ['1:1:1','1:2:1']);
    assert.equal(unitLog.connection, 'not_checked');
    assert.ok((await page.locator('.session-card').innerText()).includes('Belum diperiksa'));
    await page.locator('[data-action=h-log-edit]').click();
    await page.locator('#modal [name=connection]').selectOption('teacher');
    await page.locator('#modal [name=teacher]').fill('Penyimak sambungan');
    await page.locator('#feature-form button[type=submit]').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    assert.equal(await page.evaluate(async () => (await api('state')).data.quranUnitSessions[0].connection), 'teacher');

    // Every task completion entry point records a date; recurring copies are open.
    await page.locator('nav [data-id=Tasks]').click();
    await page.locator('[data-action=new-task]').click();
    await page.locator('#modal [name=title]').fill('Editor completed task');
    await page.locator('#modal [name=status]').selectOption('done');
    await page.locator('#modal [name=repeat]').selectOption('daily');
    assert.equal(await page.locator('#modal option[data-injected]').count(), 0);
    assert.equal(await page.locator('#modal [name=project] option').last().getAttribute('value'), 'p" data-injected="yes');
    await page.locator('#editor button.primary').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    const tasks = await page.evaluate(async () => (await api('state')).data.tasks);
    assert.equal(tasks.length, 2);
    const completed = tasks.find(t=>t.status==='done');
    assert.equal(completed.completedDay, fixtureDay);
    assert.equal(tasks.find(t=>t.status==='todo').completedDay, null);
    assert.equal(await page.evaluate(() => summaryData(today(),today()).completed), 1);
    await page.locator(`[data-action=edit-task][data-id="${completed.id}"]`).click();
    await page.locator('#modal [name=status]').selectOption('todo');
    await page.locator('#editor button.primary').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    assert.equal(await page.evaluate(() => summaryData(today(),today()).completed), 0);

    // An indicator must describe its measurement rather than silently assuming units.
    await page.locator('nav [data-id="Areas & Goals"]').click();
    await page.locator('[data-action=new-goal]').click();
    await page.locator('#modal [name=title]').fill('Improve response time');
    await page.locator('#editor button.primary').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    await page.locator('[data-action=goal-detail]').click();
    await page.locator('[data-action=goal-metric]').click();
    for (const [key,value] of Object.entries({metric:'Response time',unit:'hours',baseline:'48',target:'24',period:'per week',source:'Service log'})) {
      await page.locator(`#modal [name=${key}]`).fill(value);
    }
    await page.locator('#feature-form button[type=submit]').click();
    await page.locator('#modal').waitFor({state:'hidden'});
    const goal = await page.evaluate(async () => (await api('state')).data.goals[0]);
    assert.equal(goal.measurementVersion, 1);
    assert.equal(goal.source, 'Service log');

    // Persist/readback and responsive rendering across the actual pages.
    await page.reload();
    await page.locator('nav').waitFor();
    for (const id of ['Today','Rutinitas','Catatan Waktu','Cari Semua','Panduan','Belajar & Praktik','Sullamul Hifz','Idea Planner','Inbox','Tasks','Projects','Notes','Calendar','Focus','Review','Analytics','Areas & Goals','Settings']) {
      await page.locator(`nav [data-id="${id}"]`).click();
      assert.ok((await page.locator('#content').innerText()).length > 0, id);
    }
    await page.locator('nav [data-id="Sullamul Hifz"]').click();
    await page.locator('#h-juz').selectOption('30');
    if (process.env.LIFEOS_SCREENSHOT_DIR) {
      const out = process.env.LIFEOS_SCREENSHOT_DIR;
      fs.mkdirSync(out, {recursive:true});
      await page.locator('.session-history').screenshot({path:path.join(out,'history-desktop.png')});
      await page.setViewportSize({width:390,height:844});
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      await page.locator('.session-history').screenshot({path:path.join(out,'history-mobile.png')});
    }
    assert.deepEqual(errors, []);
    console.log('Browser checks passed: authentication, rejected backup preserves revision/data, session correction with explicit mutabaah update, S2 connection, task completion/reopening/recurrence, escaped IDs, measurement definition, persistence, 18 pages and responsive history.');
  } finally {
    if (browser) await browser.close();
    server.kill();
    await once(server, 'exit');
    fs.rmSync(temp, {recursive:true,force:true});
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
