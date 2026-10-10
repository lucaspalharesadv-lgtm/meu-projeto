# -*- coding: utf-8 -*-
import csv, re, sys, os
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perfil as PFL
from fixenc import fix
SP = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(SP, 'estado')
ENR = json.load(open(os.path.join(SP, 'enrich_cache.json'))) if os.path.exists(os.path.join(SP, 'enrich_cache.json')) else {}
LOTE = 8      # lote desta rodada: na proxima rodada, troque so este numero (e o texto do LEIA-ME abaixo)
LOTES = {}   # e-mail -> numero do lote anterior; quem nao esta em nenhum e do lote novo
for _n in range(1, LOTE):
    _f = os.path.join(EST, f'lote{_n}_emails.json')
    if os.path.exists(_f):
        for _e in json.load(open(_f)):
            LOTES.setdefault(_e.strip().lower(), str(_n))
LOTE_NOVO = f'{LOTE} (novo)'

BASE = "/home/user/meu-projeto/prospeccao_juridica"
SRC = f"{BASE}/PARCERIAS_ASSOCIADO_500.csv"
OUTROS = f"{BASE}/outros_emails_capturados.csv"
OUT = f"{BASE}/PARCERIAS_ASSOCIADO_500.xlsx"

# Colunas de personalizacao ja calculadas nas rodadas anteriores (o enrich_cache antigo nao veio para o repositorio):
# reaproveita o que esta na planilha atual para nao apagar nada dos lotes 1 a 6.
PREV = {}
if os.path.exists(OUT):
    from openpyxl import load_workbook
    _ws = load_workbook(OUT, read_only=True)['Contatos']
    _rows = list(_ws.iter_rows(values_only=True)); _h = [str(x or '') for x in _rows[0]]
    _ie, _il = _h.index('E-mail'), _h.index('Lote')
    for _r in _rows[1:]:
        if _r and _r[_ie]:
            PREV[str(_r[_ie]).strip().lower()] = ['' if x is None else str(x) for x in _r[_il:_il + 8]]

rows = list(csv.reader(open(SRC, encoding="utf-8-sig")))
hdr, body = rows[0], rows[1:]
pord = {"Alta": 0, "Media": 1, "Baixa": 2}
body.sort(key=lambda r: (1 if r[10] in ("BR", "") else 0, r[10], pord.get(r[14], 9), r[1].lower()))
for i, r in enumerate(body, 1):
    r[0] = f"{i:03d}"
with open(SRC + ".tmp", "w", newline="", encoding="utf-8-sig") as fh:
    csv.writer(fh).writerows([hdr] + body)
os.replace(SRC + ".tmp", SRC)

def extra(r):
    e = ENR.get(r[3]) or {}
    p = e.get('perfil')
    vaga = r[12] if re.search(r'CONTRATANDO|vaga', r[16], re.I) and r[12] else ''
    lote = LOTES.get(r[3].strip().lower(), LOTE_NOVO)
    if not p and r[3].strip().lower() in PREV and lote != LOTE_NOVO:
        return [lote] + PREV[r[3].strip().lower()][1:]
    if not p:
        return [lote, '', '', '', '', ('Vaga anunciada: ' + vaga + '.') if vaga else '', PFL.abordagem(None, r[6], r[12]), e.get('alerta', '')]
    sinais = '; '.join(x for x in [
        "Trabalhe conosco" if p.get('carreiras') else '', "Cita correspondentes/parceiros" if p.get('parceria') else '',
        "Contencioso de massa" if p.get('volume') else '', "Atua em todo o Brasil" if p.get('nacional') else '',
        ("Desde " + p['desde']) if p.get('desde') else ''] if x)
    return [lote, fix(p.get('frase', '')), ', '.join(p.get('areas', [])), ', '.join(p.get('cidades', [])[:3]), sinais,
            PFL.gancho(p, vaga), PFL.abordagem(p, r[6], r[12]), e.get('alerta', '')]

COLS = ["ID", "Escritório / Empresa", "Nome do contato", "E-mail", "Confirmação", "Tipo de e-mail", "Modelo de ganho",
        "Atuação remota", "Área(s) de atuação", "Cidade", "Estado", "Região", "Tipo de oportunidade", "Fonte (link)",
        "Prioridade", "Domínio válido (MX)", "Observação", "Lote", "Frase do site (literal)", "Áreas citadas no site",
        "Cidades citadas no site", "Sinais do site", "Gancho para personalizar", "Abordagem sugerida", "Alerta"]
W = [6, 34, 24, 36, 12, 20, 26, 12, 36, 16, 7, 12, 40, 42, 11, 16, 70, 12, 60, 36, 28, 34, 70, 30, 40]

HF = PatternFill("solid", fgColor="1F3864"); HFONT = Font(bold=True, color="FFFFFF", size=10)
thin = Side(style="thin", color="BFBFBF"); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
PF = {"Alta": PatternFill("solid", fgColor="C6EFCE"), "Media": PatternFill("solid", fgColor="FFEB9C"), "Baixa": PatternFill("solid", fgColor="F2F2F2")}
PFONT = {"Alta": Font(bold=True, color="006100", size=10), "Media": Font(color="9C5700", size=10), "Baixa": Font(color="808080", size=10)}
REMF = PatternFill("solid", fgColor="DDEBF7")


def sheet(ws, cols, widths, data, prio_col=None, link_col=None, wrap=()):
    ws.append(cols)
    for c in range(1, len(cols) + 1):
        x = ws.cell(row=1, column=c); x.fill = HF; x.font = HFONT; x.border = BD
        x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 32
    for r in data:
        ws.append([ILLEGAL_CHARACTERS_RE.sub('', x) if isinstance(x, str) else x for x in r]); i = ws.max_row
        for c in range(1, len(cols) + 1):
            x = ws.cell(row=i, column=c); x.border = BD; x.font = Font(size=10)
            x.alignment = Alignment(vertical="top", wrap_text=(c in wrap))
        if prio_col:
            p = r[prio_col - 1]; x = ws.cell(row=i, column=prio_col)
            x.fill = PF.get(p, PF["Baixa"]); x.font = PFONT.get(p, PFONT["Baixa"]); x.alignment = Alignment(horizontal="center", vertical="center")
        if link_col:
            ws.cell(row=i, column=link_col).font = Font(size=10, color="0563C1", underline="single")
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(row=1, column=k).column_letter].width = w
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = f"A1:{ws.cell(row=1, column=len(cols)).column_letter}{ws.max_row}"


wb = Workbook()
ws = wb.active; ws.title = "Contatos"
full = [[fix(x) for x in r] + extra(r) for r in body]
sheet(ws, COLS, W, full, prio_col=15, link_col=4, wrap=(2, 9, 13, 14, 17, 19, 23, 25))
for i in range(2, ws.max_row + 1):
    if ws.cell(row=i, column=8).value == "Sim":
        ws.cell(row=i, column=8).fill = REMF; ws.cell(row=i, column=8).font = Font(size=10, bold=True, color="1F4E78")
    for c in (1, 11, 12, 15):
        ws.cell(row=i, column=c).alignment = Alignment(horizontal="center", vertical="top")

# --- LOTE NOVO: so os contatos desta rodada, mesmas colunas ---
novos = [x for x in full if x[17] == LOTE_NOVO]
if novos:
    wn = wb.create_sheet(f"Lote {LOTE} (novos)")
    sheet(wn, COLS, W, novos, prio_col=15, link_col=4, wrap=(2, 9, 13, 14, 17, 19, 23, 25))
# o lote anterior tambem ganha aba propria (quem ainda esta trabalhando nele nao perde a aba)
ant = [x for x in full if x[17] == str(LOTE - 1)]
if ant:
    wa = wb.create_sheet(f"Lote {LOTE - 1}")
    sheet(wa, COLS, W, ant, prio_col=15, link_col=4, wrap=(2, 9, 13, 14, 17, 19, 23, 25))

# --- COMECE POR AQUI: Alta, ranqueado ---
def score(r):
    t = " ".join(r).lower(); s = 0
    if r[10] == "RO": s += 50
    if r[11] == "Norte": s += 15
    if r[7] == "Sim": s += 25
    if r[7] == "Hibrido": s += 8
    if re.search(r"previdenci", t): s += 20
    if re.search(r"sa[uú]de suplementar|plano de sa[uú]de|tea|autismo", t): s += 18
    if re.search(r"banc[aá]ri|recupera[cç][aã]o de cr[eé]dito|execu", t): s += 10
    if re.search(r"associad|parceri|correspond|participa[cç][aã]o|s[oó]cio de servi|comiss", t): s += 15
    if re.search(r"recrutador", r[6].lower()): s += 12
    if re.search(r"massa|volume|rede de correspondentes|filiais|nacional", t): s += 10
    if re.search(r"anuncio de 20(1|2[0-4])", t): s -= 30
    return s
top = sorted([r for r in body if r[14] == "Alta"], key=score, reverse=True)[:60]
N_NOVO = sum(1 for r in body if LOTES.get(r[3].strip().lower(), LOTE_NOVO) == LOTE_NOVO)
ws2 = wb.create_sheet("Comece por aqui")
sheet(ws2, ["#", "Escritório / Empresa", "E-mail", "Modelo de ganho", "Remoto", "Cidade/UF", "Abordagem sugerida", "Gancho para personalizar", "Por que está aqui"],
      [5, 36, 36, 26, 10, 22, 30, 70, 90],
      [[n, fix(r[1]), r[3], r[6], r[7], f"{r[9]}/{r[10]}", extra(r)[6], extra(r)[5], fix(r[16])[:300]] for n, r in enumerate(top, 1)], link_col=3, wrap=(2, 8, 9))

# --- RESUMO ---
s = wb.create_sheet("Resumo")
def bloco(t, pares, r0):
    s.cell(row=r0, column=1, value=t).font = Font(bold=True, size=11, color="1F3864"); r = r0 + 1
    for k, v in pares:
        s.cell(row=r, column=1, value=k); s.cell(row=r, column=2, value=v); r += 1
    return r + 1
s.cell(row=1, column=1, value="PARCERIAS / ASSOCIADO / CORRESPONDÊNCIA — RESUMO").font = Font(bold=True, size=14, color="1F3864")
s.cell(row=2, column=1, value=f"Total de contatos (e-mails únicos, todos com domínio validado por MX): {len(body)}").font = Font(bold=True, size=11)
n = 4
n = bloco("POR REGIÃO", [(k, v) for k, v in Counter(r[11] for r in body).most_common()], n)
n = bloco("POR PRIORIDADE", [(k, Counter(r[14] for r in body)[k]) for k in ("Alta", "Media", "Baixa")], n)
n = bloco("ATUAÇÃO REMOTA", Counter(r[7] for r in body).most_common(), n)
n = bloco("MODELO DE GANHO", Counter(r[6] for r in body).most_common(), n)
n = bloco("POR ESTADO", sorted(Counter(r[10] for r in body).items(), key=lambda x: (-x[1], x[0])), n)
s.column_dimensions["A"].width = 52; s.column_dimensions["B"].width = 10

# --- LEIA-ME ---
m = wb.create_sheet("LEIA-ME")
txt = [
 ("O QUE É ESTA PLANILHA", f"{len(body)} e-mails NOVOS (nenhum repete a planilha anterior de 400) de quem pode te pagar: escritórios contratando associado/PJ/remoto, escritórios de volume que usam correspondente, recrutadoras jurídicas, plataformas e parcerias."),
 ("", ""),
 ("COMO COMEÇAR", "Aba 'Comece por aqui': as 60 melhores, ranqueadas por: Rondônia/Norte, remoto, previdenciário, saúde suplementar, bancário/massa, modelo associado/parceria/correspondência, recrutadoras."),
 ("", ""),
 ("Prioridade Alta", "Vaga ou parceria ativa e aderente: associado/PJ/remoto, correspondência, volume (massa), sua área (previdenciário, saúde, bancário), ou recrutadora que atende vários escritórios."),
 ("Prioridade Média", "Escritório contratando, mas presencial/área menos aderente, ou contato institucional de escritório relevante."),
 ("Prioridade Baixa", "Vaga de estágio/apoio, ou anúncio ANTIGO (o aviso aparece na Observação) - use como contato de parceria, não como vaga aberta."),
 ("", ""),
 ("Coluna 'Domínio válido (MX)'", "Validação técnica feita SEM enviar nada: consulta ao DNS confirmando que o domínio do e-mail tem servidor de e-mail. Todos passaram. E-mails cujo domínio não existe mais foram RETIRADOS (estão na aba 'Fora da lista')."),
 ("Coluna 'Confirmação'", "Todos 'Confirmado': o e-mail foi lido literalmente na página indicada em 'Fonte'. Nesta planilha NÃO há e-mail inferido/deduzido."),
 ("Coluna 'Lote'", f"1 = primeira entrega (359); 2 = segunda rodada (681); 3 = terceira rodada (680); 4 = quarta rodada (1.077, sites .adv.br); 5 = quinta rodada (1.552, sites .com.br); 6 = sexta rodada (700: nova tentativa, .com.br ampliado, sites .com brasileiros e e-mails em domínio diferente conferidos); 7 = sétima rodada (6.449: escritórios achados pelo grafo de links do Common Crawl, que lista também sites nunca rastreados pelo índice; .adv.br, .com.br, .com e outros .br); 8 = os novos desta rodada ({N_NOVO}: sites .com de escritórios brasileiros em mais 17 edições do grafo e sites de advogados em subdomínio de plataformas como Jusfy, site.adv.br e jur.adv.br). A aba 'Lote 8 (novos)' mostra só eles. Filtre por aqui para não repetir quem você já contatou."),
 ("Colunas de PERSONALIZAÇÃO", "Frase do site (copiada literalmente do site oficial), Áreas e Cidades citadas no site, Sinais (trabalhe conosco, correspondentes, contencioso de massa, atuação nacional, ano de fundação). Tudo foi lido no site do escritório - nada inventado."),
 ("Coluna 'Gancho para personalizar'", "Resumo pronto dos fatos acima para o Claude/Cowork usar na primeira frase do e-mail (ex.: citar a área forte do escritório ou a vaga anunciada)."),
 ("Coluna 'Abordagem sugerida'", "A = candidato (vaga/associado/banco de talentos); B = fornecedor (correspondência para escritório de volume); C = proposta de parceria com divisão de honorários."),
 ("Coluna 'Alerta'", "Quando a cidade da planilha não bate com as cidades citadas no site. Confira antes de enviar."),
 ("Coluna 'Atuação remota'", "Sim = a vaga/escritório declara home office/remoto; Híbrido = misto; Não informado = o anúncio não diz (não significa presencial)."),
 ("", ""),
 ("COMO FOI FEITO", ""),
 ("Fontes", "Sites oficiais dos escritórios (páginas de contato, carreira, equipe), murais de vagas de subseções da OAB, portal Rota Jurídica, agregador Juris Vagas, portal de vagas do Grupo Nunchi, Gupy, BNE, InfoJobs, Indeed, o índice público Common Crawl (lista de sites com domínio .adv.br e sites .com.br cujo nome indica advocacia) e, nos Lotes 7 e 8, o grafo público de links do Common Crawl (listas de domínios e de hosts citados por outros sites, 2023 a 2026), sempre visitando o site oficial (como radar de quem está contratando; o e-mail sempre vem do site oficial)."),
 ("Verificação de identidade", "Quando o site foi encontrado pelo nome do escritório, só foi aceito se a própria página trouxesse o nome do escritório e termos jurídicos. Casos que falharam (gravadora, loja de móveis, clínica dentária, instituto religioso, software) foram descartados."),
 ("Regras respeitadas", "robots.txt de cada site respeitado; nenhuma página com CAPTCHA/anti-robô contornada; nenhum login; e-mail ofuscado (Cloudflare, [arroba]) NÃO decodificado; intervalo mínimo entre acessos ao mesmo site; nenhuma mensagem enviada."),
 ("", ""),
 ("ANTES DE DISPARAR", ""),
 ("Assunto exigido", "Vários anúncios exigem assunto específico - está na Observação. Sem ele, o currículo é descartado na triagem."),
 ("Fornecedor, não candidato", "Para escritório de volume/correspondência: ofereça cobertura de comarca (Ji-Paraná e região, JEF, TRT14) e tabela de valores - não peça emprego."),
 ("Volume", "Lotes de 15 a 20 e-mails por dia, personalizados (nome do escritório no corpo). Disparo em massa idêntico derruba a reputação do seu domínio."),
]
m.cell(row=1, column=1, value="PARCERIAS / ASSOCIADO / CORRESPONDÊNCIA — LEIA-ME").font = Font(bold=True, size=14, color="1F3864")
for i, (a, b) in enumerate(txt, 3):
    x = m.cell(row=i, column=1, value=a); y = m.cell(row=i, column=2, value=b)
    x.font = Font(bold=True, size=10); y.font = Font(size=10)
    x.alignment = Alignment(vertical="top", wrap_text=True); y.alignment = Alignment(vertical="top", wrap_text=True)
m.column_dimensions["A"].width = 30; m.column_dimensions["B"].width = 110

# --- FORA DA LISTA ---
if os.path.exists(OUTROS):
    o = list(csv.reader(open(OUTROS, encoding="utf-8-sig")))
    w5 = wb.create_sheet("Fora da lista")
    sheet(w5, o[0], [36, 30, 50, 14, 7, 40, 50], o[1:], wrap=(2, 3, 6, 7))

wb.save(OUT)
print("OK", OUT, len(body), "contatos |", Counter(r[14] for r in body), "| top:", len(top))
