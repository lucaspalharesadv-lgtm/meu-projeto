# -*- coding: utf-8 -*-
"""Search-engine helpers (Yahoo HTML and Bing HTML) returning result URLs. Polite: one request at a time per engine, delays, retries."""
import re, os, ssl, time, html, base64, random, urllib.parse, urllib.request, threading
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({"https": PROXY, "http": PROXY}), urllib.request.HTTPSHandler(context=CTX))
UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
       "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"]
_lock = {"yahoo": threading.Lock(), "bing": threading.Lock()}
_last = {"yahoo": 0.0, "bing": 0.0}
MIN_GAP = {"yahoo": 1.6, "bing": 1.6}

def _get(url, lang="pt-BR,pt;q=0.9,en;q=0.8"):
    req = urllib.request.Request(url, headers={"User-Agent": random.choice(UAS), "Accept-Language": lang, "Accept": "text/html,application/xhtml+xml"})
    with OPENER.open(req, timeout=45) as r:
        return r.status, r.read().decode("utf-8", "ignore")

def _throttle(engine):
    with _lock[engine]:
        gap = time.time() - _last[engine]
        if gap < MIN_GAP[engine]:
            time.sleep(MIN_GAP[engine] - gap + random.uniform(0, 0.6))
        _last[engine] = time.time()

def yahoo(q, page=1, lang="pt-BR,pt;q=0.9,en;q=0.8"):
    _throttle("yahoo")
    b = 1 + (page - 1) * 10
    st, s = _get("https://search.yahoo.com/search?p=" + urllib.parse.quote(q) + f"&b={b}&n=10", lang)
    urls = [urllib.parse.unquote(x) for x in re.findall(r'/RU=([^/]+)/RK=', s)]
    urls = [u for u in urls if u.startswith("http") and "yahoo.com" not in u]
    blocked = ("captcha" in s.lower() and len(urls) == 0)
    return urls, blocked

def bing(q, page=1, lang="pt-BR,pt;q=0.9,en;q=0.8", cc="BR"):
    _throttle("bing")
    first = 1 + (page - 1) * 10
    st, s = _get("https://www.bing.com/search?q=" + urllib.parse.quote(q) + f"&first={first}&count=10&cc={cc}", lang)
    s = html.unescape(s)
    out = []
    for u in re.findall(r'[?&]u=a1([A-Za-z0-9_\-]+)', s):
        try:
            d = base64.urlsafe_b64decode(u + "=" * (-len(u) % 4)).decode("utf-8", "ignore")
            if d.startswith("http"): out.append(d)
        except Exception: pass
    seen = set(); urls = [x for x in out if not (x in seen or seen.add(x))]
    return urls, (len(urls) == 0 and "b_algo" not in s)
