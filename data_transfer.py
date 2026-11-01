"""Add-only imports with stable references. All persistence stays in server.py."""
import copy
import unicodedata

# Dependency order matters when matching a title inside its Area/Project.
ORDER = ['areas', 'goals', 'projects', 'inbox', 'learning', 'routines', 'tasks',
         'notes', 'events', 'sessions', 'reviews', 'plans', 'preferences',
         'quran', 'quranUnits', 'quranSessions', 'quranUnitSessions',
         'quranChecks', 'practiceLogs', 'dayPlans', 'metricLogs', 'routineLogs', 'timeEntries']
RELATIONS = {
    'goals': {'area':'areas'}, 'projects': {'area':'areas','goal':'goals'},
    'tasks': {'project':'projects','parent':'tasks','learning':'learning','nextOccurrence':'tasks'},
    'notes': {'project':'projects'}, 'events': {'task':'tasks'}, 'sessions': {'task':'tasks'},
    'plans': {'area':'areas','project':'projects','source':'inbox'},
    'learning': {'area':'areas','project':'projects'}, 'practiceLogs': {'learning':'learning'},
    'routines': {'goal':'goals'}, 'routineLogs': {'routine':'routines'},
    'timeEntries': {'task':'tasks','area':'areas'}, 'metricLogs': {'goal':'goals'},
}
TITLE_KINDS = {'areas','goals','projects','inbox','tasks','notes','learning','routines'}


def normalized_title(value):
    return ' '.join(unicodedata.normalize('NFKC', value).casefold().split()) if isinstance(value,str) else ''


def unpack(package, known):
    if not isinstance(package,dict):
        raise ValueError('File harus paket JSON dengan version dan data.')
    if package.get('kind') == 'lifeos-import':
        if package.get('version') != '1.0':raise ValueError('Versi paket impor belum didukung.')
    elif package.get('kind') is not None or type(package.get('version')) is not int or package['version'] not in [1,2,3,4]:
        raise ValueError('Format bukan paket impor LifeOS atau backup yang didukung.')
    source=package.get('data')
    if not isinstance(source,dict) or not set(source).issubset(known):
        raise ValueError('Jenis data impor tidak dikenali. File audio diimpor melalui ZIP audio.')
    for kind,items in source.items():
        if not isinstance(items,list) or len(items)>20000:raise ValueError(f'{kind}: isi harus array, maksimal 20000 baris.')
        ids=set()
        for item in items:
            if not isinstance(item,dict) or not isinstance(item.get('id'),str) or not item['id'] or len(item['id'])>250 or item['id'] in ids:
                raise ValueError(f'{kind}: ID kosong, tidak valid, atau duplikat dalam file.')
            ids.add(item['id'])
    return source


def semantic_key(kind,item):
    title=normalized_title(item.get('title'))
    if kind in TITLE_KINDS and title:
        if kind in ['tasks','notes']:return (title,item.get('project') or '')
        if kind == 'projects':return (title,item.get('area') or '',item.get('goal') or '')
        if kind == 'goals':return (title,item.get('area') or '')
        return (title,)
    if kind == 'routineLogs':return (item.get('routine'),item.get('date'))
    if kind == 'dayPlans' and item.get('date'):return (item['date'],)
    return None


def merge_import(current,package,selected=None):
    source=unpack(package,set(current))
    if selected is None:selected=list(source)
    if not isinstance(selected,list) or any(not isinstance(k,str) or k not in source for k in selected) or len(set(selected))!=len(selected):
        raise ValueError('Pilihan jenis data tidak sesuai file.')
    result=copy.deepcopy(current)
    maps={k:{} for k in current}
    additions=[]
    indicator_maps={}
    report={'added':0,'skipped':0,'collections':{},'items':[],'example':package.get('purpose')=='example'}
    for kind in ORDER:
        if kind not in selected:continue
        counts={'added':0,'skipped':0};report['collections'][kind]=counts
        by_id={item['id']:item for item in result[kind]}
        by_key={semantic_key(kind,item):item for item in result[kind] if semantic_key(kind,item) is not None}
        ambiguous=set()
        seen_keys=set()
        for existing in result[kind]:
            key=semantic_key(kind,existing)
            if key is not None:
                if key in seen_keys:ambiguous.add(key)
                seen_keys.add(key)
        for raw in source[kind]:
            item=copy.deepcopy(raw)
            for field,target in RELATIONS.get(kind,{}).items():
                if isinstance(item.get(field),str):item[field]=maps[target].get(item[field],item[field])
            match=by_id.get(item['id']);reason='ID sudah ada; data lama dipertahankan'
            if match is None:
                key=semantic_key(kind,item)
                if key in ambiguous:raise ValueError(f'{kind}: ada lebih dari satu data lama dengan nama/kunci yang sama. Gunakan ID data tujuan yang tepat atau perjelas namanya.')
                match=by_key.get(key) if key is not None else None
                reason='Nama/kunci sama; data lama dipertahankan'
            if match is not None:
                maps[kind][raw['id']]=match['id'];counts['skipped']+=1;report['skipped']+=1
                if kind=='goals':
                    existing=match.get('indicators',[])
                    for incoming in raw.get('indicators',[]):
                        found=next((i for i in existing if i['id']==incoming['id'] or (normalized_title(i.get('title'))==normalized_title(incoming.get('title')) and i.get('unit')==incoming.get('unit'))),None)
                        if found:indicator_maps[(raw['id'],incoming['id'])]=found['id']
                report['items'].append({'collection':kind,'id':raw['id'],'title':str(raw.get('title',raw['id'])),'action':'skip','reason':reason})
                continue
            if kind=='sessions' and not item.get('end'):
                raise ValueError('Impor sesi fokus hanya untuk riwayat selesai; timer aktif dimulai melalui Focus.')
            maps[kind][raw['id']]=item['id']
            result[kind].append(item);by_id[item['id']]=item
            key=semantic_key(kind,item)
            if key is not None:by_key[key]=item
            additions.append((kind,item,raw))
            counts['added']+=1;report['added']+=1
            report['items'].append({'collection':kind,'id':raw['id'],'title':str(raw.get('title',raw['id'])),'action':'add','reason':'Data baru'})
    # Second pass resolves forward references such as a task parent or recurrence.
    # Only newly added records are modified; existing records remain byte-for-byte equivalent.
    for kind,item,raw in additions:
        for field,target in RELATIONS.get(kind,{}).items():
            if isinstance(raw.get(field),str):item[field]=maps[target].get(raw[field],raw[field])
        if kind=='preferences' and item['id']=='academy-smart-draft-v1':
            draft=item.get('draft',{});goal_id=draft.get('goalId')
            if goal_id:draft['goalId']=maps['goals'].get(goal_id,goal_id)
        if kind=='metricLogs' and item.get('indicator'):
            item['indicator']=indicator_maps.get((raw.get('goal'),raw['indicator']),raw['indicator'])
    indexes={kind:{i['id'] for i in items} for kind,items in result.items()}
    for kind,item,_ in additions:
        for field,target in RELATIONS.get(kind,{}).items():
            reference=item.get(field)
            # Old applied plans may retain an Inbox source that was already consumed.
            if kind=='plans' and field=='source' and item.get('applied'):continue
            if reference and (not isinstance(reference,str) or reference not in indexes[target]):
                raise ValueError(f'{kind}.{field}: referensi {reference!r} tidak ditemukan. Sertakan data terkait atau pilih ID yang sudah ada.')
        if kind=='preferences' and item['id']=='academy-smart-draft-v1' and item.get('draft',{}).get('goalId') and item['draft']['goalId'] not in indexes['goals']:
            raise ValueError('preferences.draft.goalId: Goal pada draft SMART tidak ditemukan. Sertakan Goal terkait.')
        if kind=='metricLogs' and item.get('indicator'):
            goal=next((g for g in result['goals'] if g['id']==item.get('goal')),None)
            if goal is None or item['indicator'] not in {i['id'] for i in goal.get('indicators',[])}:
                raise ValueError('metricLogs.indicator: indikator tidak ada pada Goal tujuan. Lengkapi definisi indikator terlebih dahulu.')
    return result,report
