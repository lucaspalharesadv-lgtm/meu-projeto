# -*- coding: utf-8 -*-
"""Vagas (Juris Vagas / Indeed) -> empregador -> site oficial verificado -> e-mails.
Gera candidatos JA classificados em jv_cands.json para revisao antes de gravar."""
import sys, re, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import web
from concurrent.futures import ThreadPoolExecutor

LAW = re.compile(r"advog|advocacia|sociedade|associad|law|jur[ií]d|legal|\bs/s\b", re.I)
RECR = re.compile(r"recrut|\brh\b|talent|hunting|sele[cç][aã]o|consultoria de pessoas|people", re.I)
MONEY = re.compile(r"associad|correspond|parceri|remot|home.?office|h[ií]brid|\bpj\b|aut[oô]nom|freela|previdenc|"
                   r"banc[aá]ri|massa|massific|audi[eê]ncia|pautista|dilig|execu|recupera[cç][aã]o de cr[eé]dito|"
                   r"cobran|controladoria|consumidor|sa[uú]de", re.I)
LOWJOB = re.compile(r"est[aá]gi|assistente|auxiliar|secret[aá]ri|recepcion|servi[cç]os gerais|analista de|negociador", re.I)
BADMAIL = re.compile(r"^(imprensa|press|dpo|lgpd|privacidade|privacy|ouvidoria|financeiro|cobranca|boleto|noreply|no-reply|"
                     r"webmaster|marketing|comunicacao|nfe|fiscal|compras|suporte|ti|sac)\b|@(qcomunicacao|agencia)", re.I)
ROLEMAIL = re.compile(r"^(rh|vagas?|curriculos?|carreiras?|talentos?|recrutamento|selecao|pessoas|trabalheconosco|jobs|people|bancodetalentos)", re.I)
INSTMAIL = re.compile(r"^(contato|atendimento|faleconosco|escritorio|secretaria|adm|administrativo|juridico|geral|info|recepcao|relacionamento)", re.I)
UF = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()


def jobs_by_employer(jv):
    E = {}
    for u, j in jv.items():
        emp = (j.get("empresa") or "").strip()
        if not emp or len(emp) < 3:
            continue
        E.setdefault(emp, []).append(dict(url=u, **{k: j.get(k, "") for k in ("cargo", "local", "area", "salario", "pub", "desc")}))
    return E


def pick(profile):
    """Escolhe ate 4 e-mails: RH > institucional > socio/coordenador > outros do mesmo dominio."""
    ctx = profile["ctx"]
    dom = re.sub(r"^www\.", "", re.sub(r"^https?://", "", profile["final"]).split("/")[0])
    out = []
    def add(e, tipo):
        if e not in [x[0] for x in out] and len(out) < 4:
            out.append((e, tipo, ctx[e][0], ctx[e][1]))
    em = [e for e in ctx if not BADMAIL.search(e)]
    for e in em:
        if ROLEMAIL.search(e): add(e, "RH / recrutamento")
    for e in em:
        if INSTMAIL.search(e): add(e, "institucional")
    for e in em:
        c = ctx[e][1]
        i = c.lower().find(e)
        near = c[max(0, i - 90): i]
        if re.search(r"s[óo]ci[oa]|fundador|coordenador|gestor|diretor|head|gerente", near, re.I):
            add(e, "direto (sócio/gestor)")
    if not out:   # site sem e-mail de funcao: aceita 1-2 do proprio dominio
        for e in em:
            if e.endswith("@" + dom) or e.split("@")[1] in dom:
                add(e, "direto")
            if len(out) >= 2:
                break
    if not out and len(em) == 1:
        add(em[0], "direto")
    return out


def run(jv_path="jv_out.json", done_path="jv_done.json", out_path="jv_cands.json", limit=None, workers=12):
    jv = json.load(open(jv_path))
    E = jobs_by_employer(jv)
    done = json.load(open(done_path)) if os.path.exists(done_path) else {}
    todo = [e for e in E if e not in done and (LAW.search(e) or RECR.search(e))]
    todo.sort(key=lambda e: -sum(bool(MONEY.search(j["cargo"] + " " + j["area"])) for j in E[e]))
    if limit:
        todo = todo[:limit]
    print("empregadores", len(E), "juridicos/recrutadores novos", len(todo), flush=True)

    def work(emp):
        try:
            site = web.find_site(emp)
            if not site:
                return emp, {"site": None}
            prof = web.site_profile(site[0], max_pages=7)
            if not prof:
                return emp, {"site": site[0], "picked": []}
            return emp, {"site": site[0], "title": prof["title"], "picked": pick(prof)}
        except Exception as ex:
            return emp, {"site": None, "err": str(ex)[:100]}

    cands = json.load(open(out_path)) if os.path.exists(out_path) else {}
    with ThreadPoolExecutor(workers) as ex:
        for n, (emp, r) in enumerate(ex.map(work, todo), 1):
            done[emp] = r.get("site")
            if r.get("picked"):
                cands[emp] = {"site": r["site"], "title": r.get("title", ""), "picked": r["picked"], "jobs": E[emp][:4]}
            if n % 20 == 0:
                json.dump(done, open(done_path, "w"), ensure_ascii=False)
                json.dump(cands, open(out_path, "w"), ensure_ascii=False)
                print(n, "processados |", len(cands), "com e-mail", flush=True)
    json.dump(done, open(done_path, "w"), ensure_ascii=False)
    json.dump(cands, open(out_path, "w"), ensure_ascii=False)
    print("FIM", len(cands), "empregadores com e-mail", flush=True)


def to_rows(cands, seen):
    """Converte candidatos em dicts para pros2.add()."""
    rows = []
    for emp, c in cands.items():
        jobs = c["jobs"]
        cargos = "; ".join(dict.fromkeys(j["cargo"] for j in jobs if j["cargo"]))[:160]
        areas = ", ".join(dict.fromkeys(j["area"] for j in jobs if j["area"]))[:120]
        loc = next((j["local"] for j in jobs if j["local"]), "")
        m = re.search(r"([^,]+),\s*([A-Z]{2})\b", loc)
        cidade, uf = (m.group(1).strip(), m.group(2)) if m and m.group(2) in UF else ("", "BR")
        alltxt = " ".join(j["cargo"] + " " + j["area"] + " " + j["desc"] for j in jobs)
        remoto = "Sim" if re.search(r"remot|home.?office", alltxt + loc, re.I) else (
            "Hibrido" if re.search(r"h[ií]brid", alltxt, re.I) else "Nao informado")
        money = bool(MONEY.search(alltxt))
        low = all(LOWJOB.search(j["cargo"]) for j in jobs if j["cargo"])
        recr = bool(RECR.search(emp))
        if "associad" in alltxt.lower() or "correspond" in alltxt.lower() or "parceri" in alltxt.lower():
            modelo = "Associado / parceria"
        elif recr:
            modelo = "Recrutador (varios escritorios)"
        else:
            modelo = "Vaga ativa / parceria"
        pubs = sorted({j["pub"] for j in jobs if j["pub"]})
        for e, tipo, page, ctx in c["picked"]:
            if e in seen:
                continue
            prior = "Alta" if (money or recr or remoto == "Sim") and not low else ("Baixa" if low else "Media")
            if tipo.startswith("direto (s") and prior == "Alta" and not ROLEMAIL.search(e):
                prior = "Media" if len([p for p in c["picked"]]) > 2 else prior
            trecho = re.sub(r"\s+", " ", ctx)[:170]
            u0 = jobs[0]['url']
            if 'indeed.com' in u0:
                src, ref = 'vaga no Indeed', 'Referencia: Indeed.'
            elif 'infojobs.com.br' in u0:
                src, ref = 'vaga no InfoJobs', f'Vaga: {u0} .'
            elif 'bne.com.br' in u0:
                src, ref = 'vaga no BNE', f'Pagina de vagas: {u0} .'
            elif u0.startswith('(lista dirigida'):
                src, ref = None, ''
            else:
                src, ref = 'Juris Vagas', f'Exemplo de vaga: {u0} .'
            head = (f"Escritorio CONTRATANDO em 2026 ({src}{', publicado ' + ', '.join(pubs[-2:]) if pubs else ''}): {cargos}. "
                    if src else f"ALVO DIRIGIDO ({cargos}). ")
            obs = (head + f"{ref} E-mail lido no site oficial ({c['site']}). "
                   f"Trecho: \"{trecho}\"")
            rows.append(dict(org=emp, email=e, tipo=tipo, modelo=modelo, remoto=remoto, areas=areas or "Juridico",
                             cidade=cidade, uf=uf, oport=cargos[:120], fonte=page, prior=prior, obs=obs))
    return rows


if __name__ == "__main__":
    run(limit=int(sys.argv[1]) if len(sys.argv) > 1 else None)
