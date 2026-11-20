#!/usr/bin/env python3
"""Holt ALLE Angebote aus den Prospekten der kommenden Woche und ersetzt sie in data.json.

Quellen
- kaufDA-Prospekte (Lidl, Penny, Netto, REWE … sobald dort für die Woche online):
  Prospektliste aus den kaufDA-Seiten für Lübeck, Angebote je Seite aus
  content-viewer-be.kaufda.de/v1/brochures/<id>/pages (Name, Marke, Preise, Produktfoto, Kategorie).
- NORMA: norma-online.de/de/angebote/ab-<tag>,-TT.MM.JJ/
Märkte ohne vollständige Quelle (z. B. Aldi aus der Aldi-Vorschau, Jawoll, Krümet) bleiben unverändert.

Nutzung: python3 tools/gather.py [data.json] [--monday YYYY-MM-DD]
"""
import json, re, subprocess, sys, time, datetime, html as H

UA = 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/124 Mobile Safari/537.36'
def curl(url):
    for t in range(3):
        r = subprocess.run(['curl', '-sL', '--max-time', '60', '-A', UA, url], capture_output=True)
        if r.returncode == 0 and r.stdout: return r.stdout.decode('utf-8', 'replace')
        time.sleep(2)
    return ''

args = [a for a in sys.argv[1:] if not a.startswith('--')]
PATH = args[0] if args else 'data.json'
today = datetime.date.today()
MON = today + datetime.timedelta(days=(7 - today.weekday()) % 7 or 7)
if '--monday' in sys.argv: MON = datetime.date.fromisoformat(sys.argv[sys.argv.index('--monday') + 1])
SAT = MON + datetime.timedelta(days=5)
WD = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

# ---------- Kategorien ----------
R_MEAT = re.compile(r'hähnchen|haehnchen|hühner|geflügel|pute|puten|schwein|rind|kalb|lamm|hack|wurst|würst|wiener|schinken|salami|speck|bacon|kassler|kasseler|braten|steak|schnitzel|gulasch|filet(?!.*(lachs|fisch|thun|hering|forelle|kabeljau|seelachs))|kotelett|nacken|roulade|frikadell|leberkäs|\bente\b|\benten|\bgans\b|gänse|gänse|bratwurst|cevapcici|gyros|döner|aufschnitt|\bmett\b|mettwurst|lyoner|kochschinken|chorizo|bierschinken|keule', re.I)
R_DRINK = re.compile(r'\bcola\b|coca|pepsi|fanta|sprite|mezzo|limo|bier\b|biere|pils|radler|weizen|helles|export|wein\b|weine|sekt|prosecco|crémant|champagner|glühwein|punsch|saft|nektar|schorle|wasser|mineral|energy|red bull|monster|eistee|whisk(?!as)|wodka|vodka|gin\b|rum\b|likör|liqueur|aperitif|aperol|spirituose|korn\b|jägermeister|kaffee|espresso|cappuccino|tee\b|kakao|drink|smoothie|milchgetränk|eierlikör|baileys|captain|havana|bacardi|lillet|kräuter\b', re.I)
R_SWEET = re.compile(r'schoko|praline|keks|cookie|chips|flips|gummi|haribo|bonbon|lakritz|lebkuchen|stollen|spekulatius|marzipan|riegel|nougat|nutella|knabber|crisps|popcorn|waffel|kuchen|torte|dominosteine|printen|adventskalender|mon chéri|merci|ferrero|raffaello|toffifee|milka|lindt|ritter sport|kinder|m&m|snickers|twix|mars\b|duplo|eiscreme|\beis\b|magnum|cornetto|knoppers|hanuta|pick up|oreo|leibniz|bahlsen|kekse|zuckerstange|baumkuchen|elisen|christstollen|plätzchen', re.I)
R_PLANT = re.compile(r'pflanze|weihnachtsstern|orchidee|tanne|nordmann|kaktus|blume|strauß|rosen\b|amaryllis|christrose|gesteck|kranz', re.I)
R_TOY = re.compile(r'spielzeug|puzzle|lego|playmobil|plüsch|kuscheltier|spiel\b|spiele\b|bausatz|puppe|kinderküche|ravensburger|clementoni', re.I)
R_PET = re.compile(r'hund|katze|katzen|tierfutter|vogelfutter|meisenknödel|futter|whiskas|felix|pedigree|kitekat|sheba|frolic|zooroyal|nager', re.I)
R_MODE = re.compile(r'shirt|hose|jeans|pullover|pulli|hoodie|jacke|mantel|socken|strumpf|unterwäsche|slip|boxershorts|pyjama|schlafanzug|kleid|rock\b|leggings|schal\b|mütze|handschuh|stiefel|schuh|sneaker|hausschuh|bademantel|bh\b|weste|fleece', re.I)
R_DECO = re.compile(r'deko|kerze|lichterkette|led-|leuchte|lampe|weihnachts(?!stern)|advents|krippe|figur|kissen|decke|teppich|vase|bettwäsche|handtuch|vorhang|gardine|bilderrahmen|möbel|regal|sessel|stuhl|tisch', re.I)
R_HH = re.compile(r'waschmittel|spülmittel|reiniger|toilettenpapier|küchenrolle|taschentücher|zewa|tempo|ariel|persil|lenor|somat|finish|frosch|duschgel|shampoo|zahnpasta|deo|creme|windeln|müllbeutel|folie|batterie|pfanne|topf|messer|mixer|maschine|staubsauger|fritteuse|kocher|toaster|werkzeug|akku|bohrer|schrauber|lampe|kabel|ladegerät|kopfhörer|lautsprecher|fernseher|tablet|smartphone|uhr\b|koffer|rucksack|tasche|box\b|aufbewahrung|kleiderbügel|schwamm|besen|eimer|wäsche', re.I)

R_FOOD = re.compile(r'käse|milch|joghurt|quark|sahne|butter|\bei(er)?\b|brot|brötchen|toast|nudel|pasta|spaghetti|reis\b|kartoffel|obst|gemüse|apfel|äpfel|birne|banane|orange|mandarine|clementine|zitrone|traube|beere|tomate|gurke|paprika|zwiebel|salat|kohl|möhre|karotte|pilz|champignon|nuss|nüsse|kerne|mandel|öl\b|olivenöl|essig|gewürz|sauce|soße|suppe|brühe|pizza|mehl|zucker|honig|marmelade|konfitüre|aufstrich|fisch|lachs|garnele|hering|thunfisch|müsli|cornflakes|flakes|tiefgekühlt|konserve|mais|bohnen|erbsen|linsen|wraps|tortilla|baguette|croissant|frischkäse|mozzarella|feta|gouda|camembert|dessert|pudding|asia|curry|noodle|sushi|dip\b|senf|ketchup|mayonnaise|antipasti|oliven|dattel|feige|rosine|trockenfr|smoothie|vegan|veggie|tofu|kürbis|ingwer|knoblauch|avocado|ananas|kiwi|mango|granatapfel', re.I)
def classify(name, paths=()):
    segs = set(paths); p = ' > '.join(paths)
    n = name
    if 'Dienstleistungen' in p: return None
    food = 'Lebensmittel und Getränke' in p or not p
    if not food and 'Saison und Events' in p and (R_FOOD.search(n) or R_MEAT.search(n) or R_SWEET.search(n) or R_DRINK.search(n)) and not R_DECO.search(n): food = True
    if 'Tierbedarf' in p or (not food and R_PET.search(n)): return 'Tier'
    if 'Spielzeug' in p or 'Baby und Kinder' in p: return 'Spielzeug'
    if 'Mode und Accessoires' in p: return 'Mode'
    if 'Pflanzen' in p or 'Blumen' in p: return 'Pflanzen'
    if food:
        if segs & {'Fleisch', 'Wurstwaren', 'Geflügel'} or R_MEAT.search(n):
            if not re.search(r'fisch|lachs|hering|matjes|thunfisch|forelle|kabeljau|seelachs|scholle|garnele|vegan|vegetar|veggie|fleischsalat|brühe|fond|gewürz|sauce|soße|chips|frischkäse|studentenfutter|iglo|schlemmer-?filet|fischstäbchen', n, re.I): return 'Fleisch & Wurst'
        if segs & {'Getränke', 'Alkoholische Getränke', 'Softdrinks', 'Heißgetränk', 'Wasser', 'Saft', 'Bier', 'Wein', 'Spirituosen'} or R_DRINK.search(n):
            if not re.search(r'wasserkocher|teelicht|kaffeemaschine|saftpresse|weinglas|gläser', n, re.I): return 'Getränke'
        if segs & {'Süßigkeiten', 'Knabberzeug', 'Süßwaren'} or R_SWEET.search(n): return 'Süßes'
        if p: return 'Lebensmittel'
    if R_PLANT.search(n): return 'Pflanzen'
    if R_TOY.search(n): return 'Spielzeug'
    if R_PET.search(n): return 'Tier'
    if R_MODE.search(n): return 'Mode'
    if 'Saison und Events' in p or 'Möbel und Wohnen' in p or 'Dekoration' in p or R_DECO.search(n): return 'Deko'
    if p: return 'Haushalt'
    # ohne Kategoriepfad (NORMA): Lebensmittel-Erkennung über Wörter
    if R_MEAT.search(n): return 'Fleisch & Wurst'
    if R_DRINK.search(n): return 'Getränke'
    if R_SWEET.search(n): return 'Süßes'
    if R_HH.search(n): return 'Haushalt'
    return None

def eur(x): return ('%.2f' % x).replace('.', ',') + ' €'
def clean(s): return re.sub(r'\s+', ' ', H.unescape(s or '')).strip(' ,;')
UNIT_RE = re.compile(r'(?:^|[\s,(])((?:je\s+)?(?:ca\.\s*)?\d+(?:[.,]\d+)?(?:\s*[x×]\s*\d+(?:[.,]\d+)?)?(?:\s*[-–]\s*\d+(?:[.,]\d+)?)?\s*(?:kg|g|ml|l|cl|Liter|Stück|Stk\.?|St\.|Rollen|Blatt|Tabs|WL|Paar|m)\b(?:-Packung|-Pckg\.|-Flasche|-Dose|-Glas|-Beutel|-Netz|-Schale|-Packg\.)?)', re.I)
def split_unit(desc):
    m = UNIT_RE.search(desc)
    if not m: return '', desc
    u = m.group(1).strip()
    rest = clean((desc[:m.start(1)] + ' ' + desc[m.end(1):]).replace(' ,', ','))
    u = re.sub(r'^je\s+', '', u, flags=re.I)
    return u, rest
def base(s):  # "1 kg = 1.56" -> "kg 1,56 €"
    if not s: return ''
    m = re.match(r'\s*1?\s*([a-zA-Z]+)\s*=\s*([\d.,]+)', s)
    if not m: return ''
    try: return m.group(1) + ' ' + eur(float(m.group(2).replace(',', '.')))
    except ValueError: return ''

def valnote(sd, ed):
    try:
        a = datetime.date.fromisoformat(sd[:10]); b = datetime.date.fromisoformat(ed[:10])
        # kaufDA liefert UTC; 23:00Z = nächster Tag 00:00 Berlin
        if sd[11:13] in ('22', '23'): a += datetime.timedelta(days=1)
    except Exception: return ''
    if a > MON and a <= SAT: return 'ab %s %s' % ({3: 'Donnerstag', 4: 'Freitag', 2: 'Mittwoch', 5: 'Samstag', 1: 'Dienstag'}.get(a.weekday(), WD[a.weekday()]), a.strftime('%d.%m.'))
    if b < SAT - datetime.timedelta(days=1) and b >= MON: return 'nur bis %s %s' % (WD[b.weekday()], b.strftime('%d.%m.'))
    return ''

# ---------- kaufDA ----------
KD_PAGES = ['Luebeck/Lidl/p-r74', 'Luebeck/Penny-Markt/p-r75', 'Luebeck/REWE/p-r101', 'Luebeck/Discounter/p-c5', 'Luebeck/Supermaerkte/p-c6', 'Luebeck']
KD_STORE = {'Lidl': 'Lidl', 'Penny': 'Penny', 'REWE': 'REWE', 'Netto Marken-Discount': 'Netto', 'ALDI Nord': 'Aldi Nord', 'Aldi Nord': 'Aldi Nord', 'NORMA': 'Norma', 'Norma': 'Norma'}
def kd_brochures():
    found = {}
    def walk(o):
        if isinstance(o, dict):
            if o.get('type') == 'BROCHURE' and o.get('contentId'):
                pub = (o.get('publisher') or {}).get('name'); st = KD_STORE.get(pub)
                if st and o.get('validFrom', '')[:10] in (str(MON - datetime.timedelta(days=1)), str(MON)) and (o.get('pageCount') or 0) >= 8:
                    found[o['contentId']] = (st, o.get('title'), o.get('pageCount'))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for p in KD_PAGES:
        h = curl('https://www.kaufda.de/' + p)
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', h, re.S)
        if m: walk(json.loads(m.group(1)))
        time.sleep(1)
    return found

def kd_items(cid, store):
    raw = curl('https://content-viewer-be.kaufda.de/v1/brochures/%s/pages?partner=kaufda_web&lat=53.87&lng=10.69' % cid)
    d = json.loads(raw); out = []
    for page in d.get('contents', []):
        for of in page.get('offers') or []:
            c = of.get('content') or {}
            prods = c.get('products') or []
            if not prods: continue
            pr = prods[0]
            nm = clean(pr.get('name'))
            br = clean(pr.get('brandName'))
            if not nm: continue
            name = nm if (not br or br.lower() in nm.lower() or br.lower() in ('ohne marke', 'diverse', 'sonstige')) else br + ' ' + nm
            if len(prods) > 1: name += ' u. a.'
            desc = clean(' '.join(x.get('paragraph', '') for x in pr.get('description') or []))
            unit, rest = split_unit(desc)
            deals = c.get('deals') or []
            byt = {}
            for dl in deals:
                if dl.get('min') is None: continue
                byt.setdefault(dl['type'], dl)
            # nur online erhältliche Artikel weglassen (im Markt nicht zu kaufen)
            allc = ' '.join(clean(x.get('other')) for dl in deals for x in dl.get('conditions') or [])
            if re.search(r'nur online|online exklusiv|nur im online-?shop|nur auf [a-z]+\.de', allc + ' ' + desc, re.I): continue
            notes = []
            sp, sa = byt.get('SPECIAL_PRICE'), byt.get('SALES_PRICE')
            main = sp or sa
            if not main: continue
            price = float(main['min'])
            if price <= 0: continue
            conds = [clean(x.get('other')) for x in main.get('conditions') or [] if clean(x.get('other'))]
            old = None
            if sp and sa and float(sa['min']) > price: old = float(sa['min']); notes.append('ohne App ' + eur(old))
            elif byt.get('REGULAR_PRICE') and float(byt['REGULAR_PRICE']['min']) > price: old = float(byt['REGULAR_PRICE']['min'])
            elif byt.get('RECOMMENDED_RETAIL_PRICE') and float(byt['RECOMMENDED_RETAIL_PRICE']['min']) > price:
                old = float(byt['RECOMMENDED_RETAIL_PRICE']['min']); notes.append('UVP')
            for cnd in conds:
                if re.search(r'lidl plus', cnd, re.I): notes.insert(0, 'mit Lidl Plus')
                elif re.search(r'app', cnd, re.I) and 'ohne' not in cnd.lower(): notes.insert(0, 'mit App')
                elif cnd.lower() not in ('je stück', 'je', 'ab') and len(cnd) < 60: notes.append(cnd)
                elif cnd.lower() == 'ab': notes.append('ab-Preis')
            prof = (c.get('publicationProfiles') or [{}])[0].get('validity') or {}
            vn = valnote(prof.get('startDate', ''), prof.get('endDate', ''))
            if vn: notes.insert(0, vn)
            b = base(main.get('priceByBaseUnit'))
            if b: notes.append(b)
            if rest and len(rest) < 90: notes.append(rest)
            if re.search(r'pfand', desc, re.I) and 'Pfand' not in ' '.join(notes): notes.append('zzgl. Pfand')
            paths = [x['name'] for x in pr.get('categoryPaths') or []]
            cat = classify(name + ' ' + desc, paths)
            if not cat: continue
            imgs = pr.get('images') or []
            img = (imgs[0]['url'] if imgs else c.get('image') or '').split('?')[0]
            out.append({'store': store, 'name': name[:90], 'unit': unit[:40], 'price': round(price, 2), 'old': round(old, 2) if old else None,
                        'cat': cat, 'note': '; '.join(dict.fromkeys(n for n in notes if n))[:160], 'img': img})
    return out

# ---------- NORMA ----------
def norma_items():
    base_url = 'https://www.norma-online.de'
    start = curl(base_url + '/de/angebote/')
    days = set()
    for m in re.finditer(r'/de/angebote/(ab-[a-z]+,-(\d\d)\.(\d\d)\.(\d\d))/', start):
        try: dt = datetime.date(2000 + int(m.group(4)), int(m.group(3)), int(m.group(2)))
        except ValueError: continue
        if MON <= dt <= SAT: days.add((dt, m.group(1)))
    out = {}
    for dt, slug in sorted(days):
        h = curl(base_url + '/de/angebote/' + slug + '/'); time.sleep(1)
        for art in re.findall(r'<article class="[^"]*produktBoxContainer"[^>]*>(.*?)</article>', h, re.S):
            g = lambda pat: (re.search(pat, art, re.S) or [None, ''])[1]
            nm = clean(g(r'produktBox-txt-headline">(.*?)</h3>')); br = clean(re.sub('<[^>]+>', '', g(r'<strong class="supplier">(.*?)</strong>')))
            if not nm: continue
            price = g(r'produktBox-cont-wrapper-price"><span aria-label="([\d.,]+) Euro"')
            if not price: continue
            price = float(price.replace('.', '').replace(',', '.'))
            uvp = g(r'produktBox-cont-wrapper-uvp">statt ([\d.,–-]+)<')
            old = None
            try: old = float(uvp.replace('–', '0').replace('-', '0').replace(',', '.')) if uvp else None
            except ValueError: old = None
            descr = clean(re.sub('<[^>]+>', ' ', g(r'produktBox-txt-description">(.*?)</p>')))
            inh = clean(re.sub('<[^>]+>', ' ', g(r'produktBox-txt-inh">(.*?)</li>')))
            prices = [clean(re.sub('<[^>]+>', ' ', x)) for x in re.findall(r'produktBox-txt-price">(.*?)</li>', art, re.S)]
            alt = clean(g(r'<img src="[^"]*" alt="([^"]*)"'))
            img = g(r'<img src="([^"]+)"')
            name = nm if (not br or br.lower() in nm.lower() or br.lower() in ('aus unserem sortiment',)) else br + ' ' + nm
            notes = []
            if dt > MON: notes.append('ab %s %s' % ({2: 'Mittwoch', 3: 'Donnerstag', 4: 'Freitag', 5: 'Samstag', 1: 'Dienstag'}[dt.weekday()], dt.strftime('%d.%m.')))
            if 'App' in alt or any('mit App' in p for p in prices): notes.append('mit NORMA Plus App')
            for p in prices:
                if p and 'ohne App' not in p:
                    b = re.match(r'1 (kg|l|Liter|m|Stück) = ([\d,–-]+)', p)
                    notes.append((b.group(1) + ' ' + b.group(2) + ' €') if b else p)
            if descr and descr.lower() != 'aus unserem sortiment': notes.append(descr)
            sec = g(r'href="/de/angebote/[^/]+/([a-z0-9_-]+)-t-\d+/')
            txt = name + ' ' + descr
            FOODSEC = re.search(r'obst|gemuese|food|nuss|festtagskueche|genuss|frisch|kaese|fleisch|wurst|getraenk|wein|suess|backen|lebensmittel', sec)
            NONSEC = re.search(r'mode|licht|kuschel|projekt|vogel|geschenk-tipps|gruene|wohn|winter-profis|haushalt|kueche-und|deko|spiel|nikolaus-t-395209|erkaeltung', sec)
            nonfood_word = re.search(r'gel\b|creme|balsam|kissen|decke|papier|beutel|lampe|leuchte|kerze|figur|set\b|teile|größe|ausführung|farbe|socken|jacke|tasche|handschuh|tabletten|kapseln|pflaster|spray', txt, re.I)
            if FOODSEC or (not NONSEC and not nonfood_word and (R_FOOD.search(txt) or R_MEAT.search(txt) or R_DRINK.search(txt) or R_SWEET.search(txt))):
                cat = classify(txt, ['Lebensmittel und Getränke'])
            else:
                cat = classify(txt, ['Sonstiges']) if (NONSEC or nonfood_word) else (classify(txt) or 'Haushalt')
                if cat in ('Lebensmittel', 'Fleisch & Wurst', 'Getränke', 'Süßes') and nonfood_word: cat = 'Haushalt'
            key = name + '|' + str(price)
            out[key] = {'store': 'Norma', 'name': name[:90], 'unit': re.sub(r'^je\s+', '', inh)[:40], 'price': price, 'old': old if old and old > price else None,
                        'cat': cat, 'note': '; '.join(dict.fromkeys(notes))[:160], 'img': (base_url + img) if img.startswith('/') else img}
    return list(out.values())

# ---------- Zusammenführen ----------
def main():
    D = json.load(open(PATH, encoding='utf-8'))
    new = {}
    for cid, (st, title, pc) in kd_brochures().items():
        try:
            its = kd_items(cid, st)
            print('kaufDA', st, title, pc, 'Seiten ->', len(its), 'Angebote', file=sys.stderr)
            new.setdefault(st, []).extend(its)
        except Exception as e: print('kaufDA Fehler', st, cid, e, file=sys.stderr)
        time.sleep(1)
    try:
        n = norma_items(); print('NORMA ->', len(n), file=sys.stderr)
        if len(n) >= 30: new['Norma'] = n
    except Exception as e: print('NORMA Fehler', e, file=sys.stderr)
    for st, its in list(new.items()):
        seen = {}; ded = []
        for i in its:
            k = (i['name'].lower(), i['price'])
            if k in seen: continue
            seen[k] = 1; ded.append(i)
        # gleiche Namen mit anderem Preis unterscheidbar machen (Schlüssel Markt|Produkt muss eindeutig sein)
        cnt = {}
        for i in ded:
            cnt[i['name']] = cnt.get(i['name'], 0) + 1
        for i in ded:
            if cnt[i['name']] > 1: i['name'] = i['name'] + (' (' + i['unit'] + ')' if i['unit'] else ' ' + eur(i['price']))
        uniq = {}
        for i in ded: uniq.setdefault(i['name'], i)
        new[st] = list(uniq.values())
        if len(new[st]) < 40: print('zu wenige für', st, '- behalte alte Daten', file=sys.stderr); del new[st]
    if not new: print('Keine vollständigen Quellen gefunden.', file=sys.stderr); return
    img = D.get('img', {})
    old_items = D['items']
    keep = [r for r in old_items if r[0] not in new]
    for k in list(img):
        if k.split('|', 1)[0] in new: del img[k]
    add = []
    order = ['Fleisch & Wurst', 'Getränke', 'Lebensmittel', 'Süßes', 'Haushalt', 'Deko', 'Mode', 'Tier', 'Pflanzen', 'Spielzeug']
    for st, its in new.items():
        its.sort(key=lambda i: (order.index(i['cat']) if i['cat'] in order else 99, -((i['old'] - i['price']) / i['old'] if i['old'] else 0)))
        for i in its:
            add.append([st, i['name'], i['unit'], i['price'], i['old'], i['cat'], i['note']])
            if i['img']: img[st + '|' + i['name']] = {'u': i['img']}
    D['items'] = keep + add
    D['img'] = img
    D['ts'] = int(time.time())
    q = D.get('quellen', [])
    for st in new:
        src = ['%s – alle Prospekt-Angebote (kaufDA)' % st, 'https://www.kaufda.de/Luebeck'] if st != 'Norma' else ['Norma – norma-online.de Angebote', 'https://www.norma-online.de/de/angebote/']
        if src not in q: q.append(src)
    D['quellen'] = q
    json.dump(D, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    print('Fertig:', dict(Counter(r[0] for r in D['items'])), file=sys.stderr)

if __name__ == '__main__': main()
