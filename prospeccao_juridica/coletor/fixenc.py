import re
MOJI = re.compile(r'Ã[\u0080-¿]|â€|Â[ -¿]')
def fix(s):
    if not s or not MOJI.search(s): return s
    for enc in ('cp1252', 'latin-1'):
        try:
            t = s.encode(enc, errors='strict').decode('utf-8', errors='strict')
            if not MOJI.search(t): return t
        except Exception:
            pass
    # conserto parcial, trecho a trecho
    def rep(m):
        try: return m.group(0).encode('cp1252').decode('utf-8')
        except Exception: return m.group(0)
    return re.sub(r'(?:[ÃÂâ][\u0080-ÿ‐-›Œ-ƒ]{1,2})+', rep, s)
if __name__ == '__main__':
    print(fix('LFR Advocacia â Lisita, Fleury & Ribeiro. Conselheira estratÃ©gica em GoiÃ¢nia/GO. Nove Ã¡reas'))
    print(fix('PÃ¡gina inicial'), fix('ServiÃ§os'), fix('Já está ok'))
