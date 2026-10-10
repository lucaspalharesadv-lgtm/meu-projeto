# -*- coding: utf-8 -*-
"""Coletor web educado.

Regras (exigidas pelo usuario):
- respeita robots.txt de cada dominio (401/403/5xx no robots = nao coleta);
- nao contorna CAPTCHA, desafio anti-bot, login ou paywall: pagina de
  desafio e simplesmente descartada;
- NAO decodifica e-mail ofuscado (Cloudflare __cf_email__ / cdn-cgi,
  "[at]", "(arroba)" etc.) - so captura e-mail escrito em texto aberto;
- intervalo minimo entre requisicoes ao mesmo dominio.
"""
import hashlib, html, json, os, re, threading, time
import urllib.parse, urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; PesquisaJuridicaBot/1.0; pesquisa de vagas publicas)"
UA_TOKEN = "PesquisaJuridicaBot"
CA = os.environ.get("REQUESTS_CA_BUNDLE") or "/root/.ccr/ca-bundle.crt"
BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE, "cache")
os.makedirs(CACHE, exist_ok=True)
DELAY = 1.5

_S = requests.Session()
_S.headers.update({"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
_robots, _rlock = {}, threading.Lock()
_last, _llock = {}, threading.Lock()
LOG = {"robots_block": [], "challenge": [], "erro": []}

CHALLENGE = re.compile(r"cf-chl|just a moment|attention required|captcha|"
                       r"verifique que voc[eê] [eé] humano|are you a robot|ddos-guard", re.I)
EMAIL = re.compile(r"(?<![\w.%+-])([A-Za-z0-9][A-Za-z0-9._%+-]{0,63}@"
                   r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
                   r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.[A-Za-z]{2,24})")
JUNK_DOM = re.compile(r"(sentry|wixpress|example|exemplo|domain|dominio|seudominio|"
                      r"seuemail|email\.com$|test\.com|mysite|godaddy|wordpress\.com$|"
                      r"sentry-next|cloudflare|schema\.org|w3\.org|gstatic|googleapis|"
                      r"jquery|bootstrap|fontawesome|placeholder|website\.com$|yourdomain|seusite|mail\.com$|^teste\.com$|^contato\.com\.br$|^email\.com\.br$)", re.I)
JUNK_TLD = re.compile(r"\.(png|jpe?g|gif|webp|svg|css|js|ico|bmp|tiff?|woff2?|ttf|eot|mp4|pdf)$", re.I)


def _domain(u):
    return urllib.parse.urlsplit(u).netloc.lower()


def _cache_path(u):
    return os.path.join(CACHE, hashlib.sha1(u.encode()).hexdigest() + ".json")


import gzip as _gz
MAXHTML = 800_000      # paginas gigantes sao cortadas no cache (e-mails ficam no topo/rodape ja lidos)


def _cache_read(u):
    cp = _cache_path(u)
    if os.path.exists(cp + ".gz"):
        try:
            return json.loads(_gz.decompress(open(cp + ".gz", "rb").read()))
        except Exception:
            return None
    if os.path.exists(cp):
        return json.load(open(cp))
    return None


def _cache_write(u, d):
    cp = _cache_path(u)
    with open(cp + ".gz.tmp", "wb") as fh:
        fh.write(_gz.compress(json.dumps(d).encode(), 6))
    os.replace(cp + ".gz.tmp", cp + ".gz")


def _wait(dom):
    with _llock:
        now = time.time()
        t = max(now, _last.get(dom, 0) + DELAY)
        _last[dom] = t
    if t > now:
        time.sleep(t - now)


def _get_robots(u):
    p = urllib.parse.urlsplit(u)
    key = f"{p.scheme}://{p.netloc}"
    with _rlock:
        if key in _robots:
            return _robots[key]
    rp = urllib.robotparser.RobotFileParser()
    try:
        _wait(p.netloc.lower())
        r = _S.get(key + "/robots.txt", timeout=15, verify=CA, allow_redirects=True)
        if r.status_code in (401, 403) or r.status_code >= 500:
            rp.disallow_all = True
        elif r.status_code >= 400:
            rp.allow_all = True
        else:
            rp.parse(r.text.splitlines())
    except Exception:
        rp.disallow_all = True      # sem robots legivel = conservador
    with _rlock:
        _robots[key] = rp
    return rp


def allowed(u):
    rp = _get_robots(u)
    return rp.can_fetch(UA_TOKEN, u) and rp.can_fetch("*", u)


def fetch(u, use_cache=True):
    """Retorna dict {url,status,html,final} ou None (bloqueado/erro/desafio)."""
    if use_cache:
        c = _cache_read(u)
        if c is not None:
            return c
    if not allowed(u):
        LOG["robots_block"].append(u)
        return None
    try:
        _wait(_domain(u))
        r = _S.get(u, timeout=25, verify=CA, allow_redirects=True)
    except Exception as e:
        LOG["erro"].append((u, str(e)[:120]))
        return None
    body = r.text if "text" in r.headers.get("content-type", "") or "xml" in r.headers.get("content-type", "") else ""
    if r.status_code in (403, 429, 503) or (body and CHALLENGE.search(body[:20000]) and len(body) < 60000
                                             and r.status_code != 200):
        LOG["challenge"].append((u, r.status_code))
        return None
    if r.status_code >= 400:
        LOG["erro"].append((u, r.status_code))
        return None
    # pagina final pode ter redirecionado para outro dominio: checa robots dele tambem
    if _domain(r.url) != _domain(u) and not allowed(r.url):
        LOG["robots_block"].append(r.url)
        return None
    d = {"url": u, "final": r.url, "status": r.status_code, "html": body[:MAXHTML]}
    _cache_write(u, d)
    return d


def fetch_many(urls, workers=8):
    out = {}
    with ThreadPoolExecutor(workers) as ex:
        for u, d in zip(urls, ex.map(fetch, urls)):
            out[u] = d
    return out


import warnings as _warn
from functools import lru_cache
try:
    from bs4 import XMLParsedAsHTMLWarning as _XW
    _warn.filterwarnings("ignore", category=_XW)
except Exception:
    pass


@lru_cache(maxsize=256)
def _parse(htm):
    """Uma unica leitura do HTML por pagina (antes era lido 4 a 6 vezes). Mesmo resultado de antes:
    titulo e links lidos da pagina inteira; texto sem script/style/noscript/svg."""
    s = BeautifulSoup(htm, "lxml")
    title = (s.title.get_text(" ").strip() if s.title else "")[:160]
    anchors = tuple((a["href"], a.get_text(" ").strip()) for a in s.find_all("a", href=True))
    for t in s(["script", "style", "noscript", "svg"]):
        t.decompose()
    text = re.sub(r"[ \t\r\f\v]+", " ", s.get_text("\n")).strip()
    return text, title, anchors


def text_of(htm):
    return _parse(htm)[0]


def title_of(htm):
    return _parse(htm)[1]


def anchors_of(htm):
    return _parse(htm)[2]


def emails_in(htm):
    """E-mails em TEXTO ABERTO + mailto. Ignora ofuscacao (cdn-cgi, [at])."""
    found = []
    for h, _t in anchors_of(htm):
        if h.lower().startswith("mailto:"):
            e = urllib.parse.unquote(h[7:].split("?")[0]).strip()
            found.append(e)
    txt = html.unescape(text_of(htm))
    found += EMAIL.findall(txt)
    clean = []
    for e in found:
        e = e.strip().strip(".,;:()[]<>\"'").lower()
        if not EMAIL.fullmatch(e):
            continue
        dom = e.split("@", 1)[1]
        if JUNK_TLD.search(e) or JUNK_DOM.search(dom) or re.search(r"@\d+x\.", e):
            continue
        if e not in clean:
            clean.append(e)
    return clean


def contexts(htm, emails, width=260):
    txt = html.unescape(text_of(htm))
    low = txt.lower()
    out = {}
    for e in emails:
        i = low.find(e)
        if i < 0:
            out[e] = ""
            continue
        a, b = max(0, i - width), min(len(txt), i + len(e) + width // 2)
        out[e] = re.sub(r"\s+", " ", txt[a:b])
    return out


def sitemap_urls(root, must=None, limit=5000):
    """Le sitemap(s) do site (feito para robos) e devolve URLs (opcional: filtro regex)."""
    seen, urls, todo = set(), [], []
    for cand in (root.rstrip("/") + "/sitemap_index.xml", root.rstrip("/") + "/sitemap.xml",
                 root.rstrip("/") + "/wp-sitemap.xml"):
        todo.append(cand)
    rp = _get_robots(root)
    for sm in getattr(rp, "site_maps", lambda: None)() or []:
        todo.insert(0, sm)
    pat = re.compile(must, re.I) if must else None
    while todo and len(urls) < limit:
        sm = todo.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        d = fetch(sm)
        if not d or not d["html"]:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", d["html"])
        for l in locs:
            l = html.unescape(l)
            if l.endswith(".xml") or "sitemap" in l.lower():
                todo.append(l)
            elif not pat or pat.search(l):
                urls.append(l)
    return urls


KEYLINK = re.compile(r"contato|fale|trabalhe|carreira|vaga|talento|parceir|correspond|credenci|"
                     r"equipe|profission|socio|sócio|advogad|sobre|quem-somos|unidade|escritorio|"
                     r"seja|junte|faca-parte|faça|recrut|rh|curricul|people|careers|join", re.I)


def site_profile(home, max_pages=8):
    """Visita a home e ate max_pages links internos relevantes. Devolve
    {'home','title','pages':[(url,title,[emails])], 'ctx':{email:(url,contexto)}}"""
    d = fetch(home)
    if not d:
        return None
    base = urllib.parse.urlsplit(d["final"])
    links = []
    for href, atxt in anchors_of(d["html"]):
        h = urllib.parse.urljoin(d["final"], href.split("#")[0])
        p = urllib.parse.urlsplit(h)
        if p.scheme not in ("http", "https"):
            continue
        if p.netloc.lower().replace("www.", "") != base.netloc.lower().replace("www.", ""):
            continue
        txt = atxt
        if KEYLINK.search(p.path) or KEYLINK.search(txt):
            if h not in links and h.rstrip("/") != d["final"].rstrip("/"):
                links.append(h)
    # prioriza paginas de contato/carreira/parceria
    pri = re.compile(r"contato|trabalhe|carreira|vaga|talento|parceir|correspond|credenci|curricul|fale", re.I)
    links.sort(key=lambda u: 0 if pri.search(u) else 1)
    res = {"home": home, "final": d["final"], "title": title_of(d["html"]), "pages": [], "ctx": {}}
    for u, dd in [(d["final"], d)] + [(u, fetch(u)) for u in links[:max_pages]]:
        if not dd:
            continue
        em = emails_in(dd["html"])
        res["pages"].append((u, title_of(dd["html"])[:70], em))
        for e, c in contexts(dd["html"], em).items():
            if e not in res["ctx"] or pri.search(u):
                res["ctx"][e] = (u, c)
    return res


def profile_many(homes, workers=8, max_pages=8):
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(homes, ex.map(lambda h: site_profile(h, max_pages), homes)))


def show(profiles, ctxlen=230):
    for h, r in profiles.items():
        if not r:
            print(f"X  {h}")
            continue
        allem = sorted(r["ctx"])
        print(f"\n## {h} -> {r['final']} | {r['title'][:80]}")
        if not allem:
            print("   (sem e-mail em texto aberto)")
        for e in allem:
            u, c = r["ctx"][e]
            print(f"   {e}  [{u}]\n      {c[:ctxlen]}")


import unicodedata
STOP = {"advogados", "advogado", "advocacia", "associados", "associadas", "sociedade", "de", "da", "do", "das", "dos",
        "e", "and", "&", "s/s", "ss", "ltda", "me", "eireli", "escritorio", "consultoria", "juridica", "juridico",
        "assessoria", "individual", "law", "firm", "group", "grupo", "partners", "i", "the", "em", "a", "o",
        "brasil", "bank", "rh", "solucoes", "empresariais", "carreira", "gestao", "ativos", "servicos", "participacoes",
        "comunicacao", "tecnologia", "integrada", "estrategica", "especializada", "s", "cia", "associados", "simples"}


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s)


def domain_candidates(name):
    toks = [t for t in _norm(name).split() if t not in STOP and len(t) > 1]
    if not toks:
        return []
    joins = {"".join(toks), toks[0], "".join(toks[:2]), "".join(t[0] for t in toks) if len(toks) >= 2 else toks[0]}
    joins |= {toks[0] + "e" + toks[1]} if len(toks) >= 2 else set()
    sufs = ["", "adv", "advogados", "advocacia", "advogadosassociados", "law"]
    tlds = [".adv.br", ".com.br", ".com", ".law"]
    out = []
    for j in joins:
        if len(j) < 3:
            continue
        for s in sufs:
            for t in tlds:
                out.append(j + s + t)
    return list(dict.fromkeys(out)), toks


def find_site(name, extra=()):
    """Acha o site oficial pelo nome: candidato precisa (1) resolver DNS e
    (2) a pagina conter um token distintivo do nome + palavra juridica."""
    import dns.resolver
    cands, toks = domain_candidates(name) if domain_candidates(name) else ([], [])
    cands = list(extra) + cands
    distinct = [t for t in toks if len(t) >= 4] or toks
    hits = []
    for c in cands:
        try:
            dns.resolver.resolve(c, "A", lifetime=4)
        except Exception:
            continue
        for pre in ("https://www.", "https://"):
            d = fetch(pre + c)
            if not d or not d["html"]:
                continue
            t = _norm(title_of(d["html"]) + " " + text_of(d["html"])[:6000])
            ok_name = sum(1 for k in distinct if k in t) >= max(1, min(2, len(distinct)))
            ok_jur = re.search(r"advog|advoca|juridic|direito|oab", t)
            if ok_name and ok_jur:
                hits.append(pre + c)
                return hits
            break
    return hits


_dns_cache = {}
def _resolves(dom):
    import dns.resolver
    if dom in _dns_cache:
        return _dns_cache[dom]
    try:
        dns.resolver.resolve(dom, "A", lifetime=3)
        ok = True
    except Exception:
        ok = False
    _dns_cache[dom] = ok
    return ok


def find_site_fast(name, extra=()):
    dc = domain_candidates(name)
    cands, toks = dc if dc else ([], [])
    cands = list(dict.fromkeys(list(extra) + cands))
    if not cands:
        return []
    with ThreadPoolExecutor(24) as ex:
        live = [c for c, ok in zip(cands, ex.map(_resolves, cands)) if ok]
    distinct = [t for t in toks if len(t) >= 4] or toks
    for c in live:
        for pre in ("https://www.", "https://"):
            d = fetch(pre + c)
            if not d or not d["html"]:
                continue
            t = _norm(title_of(d["html"]) + " " + text_of(d["html"])[:6000])
            ok_name = sum(1 for k in distinct if k in t) >= max(1, min(2, len(distinct)))
            if ok_name and re.search(r"advog|advoca|juridic|direito|oab", t):
                return [pre + c]
            break
    return []
