# -*- coding: utf-8 -*-
"""Crawl law-firm websites for published e-mails. Input: domains JSONL (domain, cc, city, uf). Output: crawl_<tag>.jsonl (one line per domain)."""
import sys, os, re, json, time, html, ssl, threading, urllib.parse, urllib.robotparser
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
CA = "/root/.ccr/ca-bundle.crt"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
EMAIL_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._%+\-']{0,63}@(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,24}")
JUNK = re.compile(r"(\.(png|jpe?g|gif|svg|webp|css|js)$)|example\.|sentry|wixpress|wix\.com|godaddy|yourdomain|dominio|domain\.com|email\.com|seuemail|seu-email|nome@|name@|user@|usuario|test@|teste@|noreply|no-reply|nao-responda|naoresponda|donotreply|@2x|@3x|@sentry|@gmail\.com\.br$|@hotmail\.com\.br$|@\d|unsubscribe|webmaster@|postmaster@|abuse@|privacy@|dpo@|mailer-daemon|@w3\.org|@schema\.org|@localhost|@email\.|@mail\.ru|@qq\.com", re.I)
CONTACT_WORDS = ["contato","contact","contacto","contatti","fale-conosco","faleconosco","fale_conosco","atendimento","equipe","team","nossa-equipe","our-team","people","profissionais","advogados","lawyers","attorneys","solicitors","socios","sócios","partners","staff","quem-somos","quemsomos","sobre","about","chi-siamo","equipo","abogados","avvocati","avocats","cabinet","studio","escritorio","escritório","the-firm","our-firm","nossa-historia","membros","integrantes","time","corpo-juridico","corpo-técnico","professionals","our-people","our-attorneys","meet","consultants","agents"]
AREAS = {"cível":["cível","civel","direito civil","civil"],"consumidor":["consumidor","consumerista"],"bancário":["bancário","bancario","banco","financeiro"],"previdenciário":["previdenciário","previdenciario","inss","aposentadoria"],"trabalhista":["trabalhista","trabalho"],"família":["família","familia","divórcio","divorcio","inventário","inventario","sucessões"],"empresarial":["empresarial","societário","societario","contratos","contratual"],"tributário":["tributário","tributario","fiscal"],"imobiliário":["imobiliário","imobiliario","imóveis","imoveis","condominial"],"criminal":["criminal","penal"],"imigração":["imigração","imigracao","immigration","visto","vistos","visa","visas","green card","cidadania","citizenship","nacionalidade","nationality","naturalização","naturalization","extranjería","extranjeria","immigrazione","cittadinanza","migration","migrazione","étrangers"],"saúde":["saúde","saude","plano de saúde","médico"],"digital":["digital","lgpd","proteção de dados","tecnologia"],"ambiental":["ambiental"],"agrário":["agrário","agrario","agronegócio","agro"],"administrativo":["administrativo","licitações","servidor público"],"eleitoral":["eleitoral"],"corporate":["corporate","m&a","mergers","capital markets","banking","project finance","arbitration","arbitragem","litigation","dispute"],"real estate":["real estate","property","imobiliário"],"family":["family law","divorce","custody"],"personal injury":["personal injury","accident"],"criminal defense":["criminal defense","dui"],"employment":["employment","labor law"],"wills":["estate planning","wills","probate"]}
BR_PHONE = re.compile(r"\(?\b(?:\d{2})\)?\s?(?:9\s?)?\d{4}[\s\-]?\d{4}\b")
INT_PHONE = re.compile(r"\+?\(?\d{1,4}\)?[\s\-.]?\(?\d{2,4}\)?[\s\-.]?\d{3,4}[\s\-.]?\d{3,4}")
FIRM_WORDS = re.compile(r"advoga|advocacia|law|legal|llp|llc|p\.a\.|pllc|ltd|associad|sociedade|escrit|abogad|avvocat|avocat|studio|cabinet|group|firm|office|immigration|imigra|migration|consult|servi|contact|contato|email|e-mail|telefone|phone|whatsapp|endere|address|rua |av\.|avenida|copyright|©|todos os direitos|all rights|\d", re.I)
NAME_RE = re.compile(r"^(?:Dr\.?a?\.?\s+|Dra\.?\s+|Adv\.?\s+|Me\.?\s+|Ms\.?\s+|Mr\.?\s+|Atty\.?\s+)?([A-ZÀ-Ý][a-zà-ÿ'\-]+(?:\s+(?:de|da|do|dos|das|e|y|van|von|del|della|di|la|le|du|des|&|Jr\.?|Neto|Filho|Júnior|Junior)\s+|\s+)[A-ZÀ-Ý][A-Za-zà-ÿ'\-\.]+(?:\s+[A-ZÀ-Ý][A-Za-zà-ÿ'\-\.]+){0,4})$")
lock = threading.Lock()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import names as NM
LAW_RE = re.compile(r"advogad|advocacia|\boab\b|attorney|law firm|law office|lawyer|solicitor|barrister|avvocat|abogad|avocat|rechtsanwalt|paralegal|migration agent|immigration consultant|rcic|escrit[óo]rio de advocacia|jurídic|juridic", re.I)

def decode_cfemail(s):
    try:
        b = bytes.fromhex(s); k = b[0]; return "".join(chr(c ^ k) for c in b[1:])
    except Exception: return None

def deobf(text):
    t = re.sub(r"\s*[\[\(\{]\s*(at|arroba)\s*[\]\)\}]\s*", "@", text, flags=re.I)
    t = re.sub(r"\s*[\[\(\{]\s*(dot|ponto)\s*[\]\)\}]\s*", ".", t, flags=re.I)
    return t

def clean_email(e):
    e = e.strip().strip(".,;:()<>[]\"'").lower()
    e = e.replace("mailto:", "").split("?")[0].strip()
    if not EMAIL_RE.fullmatch(e) or JUNK.search(e) or len(e) > 80: return None
    if e.count(".") > 6 or ".." in e: return None
    if re.match(r"^\d{2,}", e) or e.split("@")[0] in ("conto",): return None
    return e

def guess_name(el):
    """Walk up from a mailto element looking for a person-name text nearby."""
    node = el
    for _ in range(4):
        if node is None: break
        texts = []
        for t in node.stripped_strings:
            t = t.strip()
            if 4 <= len(t) <= 60 and not FIRM_WORDS.search(t) and "@" not in t:
                texts.append(t)
        for t in texts:
            m = NAME_RE.match(t)
            if not m: continue
            words = t.split()
            if not (2 <= len(words) <= 6): continue
            low = [w.lower().strip(".,") for w in words]
            if any(w in NM.STOP for w in low): continue
            first = low[0] if low[0] not in ("dr","dra","dr.","dra.","adv","adv.","me","me.","mr","mr.","ms","ms.") else (low[1] if len(low) > 1 else "")
            if first in NM.FEMALE or first in NM.MALE: return t
            if len(words) >= 3 and all(w[:1].isupper() for w in words if w.lower() not in ("de","da","do","dos","das","e","y","van","von","del","della","di","la","le","du","des")): return t
        node = node.parent
    return ""

def fetch(session, url, maxbytes=2_000_000):
    r = session.get(url, timeout=(8, 15), stream=True, allow_redirects=True, verify=CA, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,es;q=0.7,it;q=0.6"})
    ct = r.headers.get("content-type", "")
    if "html" not in ct and "xml" not in ct and ct: r.close(); return r.url, r.status_code, ""
    data = b""
    for chunk in r.iter_content(65536):
        data += chunk
        if len(data) > maxbytes: break
    r.close()
    head = data[:6000].decode("ascii", "ignore")
    m = re.search(r'<meta[^>]+charset=["\']?\s*([A-Za-z0-9_\-]+)', head, re.I)
    hdr_cs = re.search(r"charset=([A-Za-z0-9_\-]+)", ct or "", re.I)
    enc = (m.group(1) if m else (hdr_cs.group(1) if hdr_cs else "utf-8")).lower()
    if enc in ("iso-8859-1", "latin-1", "latin1", "windows-1252", "cp1252"): enc = "cp1252"
    try: txt = data.decode(enc, "ignore")
    except Exception: txt = data.decode("utf-8", "ignore")
    if enc == "utf-8" and "\ufffd" in txt[:20000] and txt.count("\ufffd") > 5:
        txt = data.decode("cp1252", "ignore")
    return r.url, r.status_code, txt

def crawl_domain(item):
    domain = item["domain"]; res = {"domain": domain, "cc": item.get("cc"), "city": item.get("city"), "uf": item.get("uf"), "emails": [], "pages": 0, "status": "", "title": "", "desc": "", "lang": "", "areas": [], "phones": [], "final_url": "", "city_in_text": False}
    session = requests.Session(); session.max_redirects = 6
    t0 = time.time()
    base = None; home = None
    for cand in (f"https://{domain}", f"https://www.{domain}", f"http://{domain}", f"http://www.{domain}"):
        try:
            url, st, txt = fetch(session, cand)
            if st < 400 and txt: base, home = url, txt; break
            res["status"] = f"http{st}"
        except Exception as e:
            res["status"] = type(e).__name__
    if home is None: return res
    res["final_url"] = base; res["status"] = "ok"
    rp = urllib.robotparser.RobotFileParser()
    try:
        robots_url = urllib.parse.urljoin(base, "/robots.txt")
        r = session.get(robots_url, timeout=(5, 8), verify=CA, headers={"User-Agent": UA})
        rp.parse(r.text.splitlines() if r.status_code == 200 else [])
    except Exception: rp.parse([])
    def allowed(u):
        try: return rp.can_fetch("*", u)
        except Exception: return True
    found = {}; texts = []
    def harvest(url, txt):
        soup = BeautifulSoup(txt, "lxml")
        for s in soup(["script", "style", "noscript"]): s.decompose()
        if not res["title"]:
            res["title"] = (soup.title.string.strip() if soup.title and soup.title.string else "")[:200]
            md = soup.find("meta", attrs={"name": re.compile("description", re.I)})
            res["desc"] = (md.get("content", "") if md else "")[:300]
            res["lang"] = (soup.html.get("lang", "") if soup.html else "")[:10]
        for a in soup.select("a[href^='mailto:']"):
            e = clean_email(html.unescape(a.get("href", "")))
            if e and e not in found: found[e] = {"email": e, "page": url, "name": guess_name(a), "via": "mailto"}
        for cf in soup.select("[data-cfemail]"):
            e = decode_cfemail(cf.get("data-cfemail", "")); e = clean_email(e) if e else None
            if e and e not in found: found[e] = {"email": e, "page": url, "name": guess_name(cf), "via": "cfemail"}
        text = soup.get_text(" ")
        for e in EMAIL_RE.findall(deobf(html.unescape(text))):
            e = clean_email(e)
            if e and e not in found: found[e] = {"email": e, "page": url, "name": "", "via": "text"}
        for e in EMAIL_RE.findall(urllib.parse.unquote(html.unescape(txt))):  # raw html (json-ld, hidden fields)
            e = clean_email(e)
            if e and e not in found: found[e] = {"email": e, "page": url, "name": "", "via": "html"}
        texts.append(text.lower())
        return soup
    soup = harvest(base, home); res["pages"] = 1
    # candidate internal pages
    cands = []
    bhost = urllib.parse.urlparse(base).netloc.lower().replace("www.", "")
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")): continue
        u = urllib.parse.urljoin(base, href)
        pu = urllib.parse.urlparse(u)
        if pu.netloc.lower().replace("www.", "") != bhost: continue
        key = (pu.path or "/").lower() + " " + a.get_text(" ", strip=True).lower()
        score = sum(2 if w in (pu.path or "").lower() else 1 for w in CONTACT_WORDS if w in key)
        if score: cands.append((score, u.split("#")[0]))
    cands.sort(key=lambda x: -x[0])
    seen = {base.rstrip("/")}; n = 0
    TEAMPATH = re.compile(r"/(equipe|team|our-team|nossa-equipe|people|our-people|profissionais|advogados|lawyers|attorneys|solicitors|socios|s%C3%B3cios|partners|staff|membros|integrantes|corpo-juridico|professionals|abogados|avvocati|avocats|consultants|agents|quem-somos|about|sobre)", re.I)
    profile_links = []
    for sc, u in cands:
        if n >= 7 or time.time() - t0 > 70: break
        if u.rstrip("/") in seen or not allowed(u): continue
        seen.add(u.rstrip("/"))
        try:
            url, st, txt = fetch(session, u)
            if st < 400 and txt:
                sp = harvest(url, txt); res["pages"] += 1
                if TEAMPATH.search(urllib.parse.urlparse(url).path or ""):
                    pdepth = (urllib.parse.urlparse(url).path or "/").rstrip("/").count("/")
                    for a in sp.find_all("a", href=True):
                        pu = urllib.parse.urlparse(urllib.parse.urljoin(url, a["href"].strip()))
                        if pu.netloc.lower().replace("www.", "") != bhost: continue
                        path = (pu.path or "/").rstrip("/")
                        if path.count("/") > pdepth and TEAMPATH.search(path) and not re.search(r"\.(pdf|jpg|png|jpeg|gif|webp)$", path, re.I):
                            profile_links.append(pu.scheme + "://" + pu.netloc + path)
        except Exception: pass
        n += 1; time.sleep(0.3)
    m = 0
    for u in dict.fromkeys(profile_links):
        if m >= 12 or time.time() - t0 > 110: break
        if u.rstrip("/") in seen or not allowed(u): continue
        seen.add(u.rstrip("/"))
        try:
            url, st, txt = fetch(session, u)
            if st < 400 and txt: harvest(url, txt); res["pages"] += 1
        except Exception: pass
        m += 1; time.sleep(0.25)
    alltext = " ".join(texts)
    res["law_hits"] = len(LAW_RE.findall(alltext[:200000]))
    res["pt_hits"] = len(re.findall(r"portugu|brasil|brazil", alltext[:200000]))
    res["areas"] = [k for k, ws in AREAS.items() if any(w in alltext for w in ws)][:8]
    phones = BR_PHONE.findall(home) if item.get("cc") == "BR" else INT_PHONE.findall(BeautifulSoup(home, "lxml").get_text(" "))
    res["phones"] = list(dict.fromkeys(p.strip() for p in phones if 8 <= len(re.sub(r"\D", "", p)) <= 15))[:3]
    city = (item.get("city") or "").lower().split(" ")[0]
    res["city_in_text"] = bool(city) and city in alltext
    res["emails"] = list(found.values())[:40]
    return res

if __name__ == "__main__":
    inp, tag, workers = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20
    items = [json.loads(l) for l in open(inp, encoding="utf-8") if l.strip()]
    outp = f"crawl_{tag}.jsonl"
    done = set()
    if os.path.exists(outp):
        for l in open(outp, encoding="utf-8"):
            try: done.add(json.loads(l)["domain"])
            except Exception: pass
    items = [i for i in items if i["domain"] not in done]
    print("domínios a rastrear:", len(items), "| já feitos:", len(done), flush=True)
    out = open(outp, "a", encoding="utf-8"); n = 0; ne = 0; t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(crawl_domain, it) for it in items]
        for f in as_completed(futs):
            try: r = f.result()
            except Exception as e: continue
            with lock:
                out.write(json.dumps(r, ensure_ascii=False) + "\n"); out.flush(); n += 1; ne += len(r["emails"])
                if n % 100 == 0: print(time.strftime("%H:%M:%S"), "feitos:", n, "e-mails brutos:", ne, "ritmo/min:", round(n / ((time.time() - t0) / 60), 1), flush=True)
    print("FIM", n, ne, flush=True)
