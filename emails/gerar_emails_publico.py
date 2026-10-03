#!/usr/bin/env python3
"""Gera assunto + corpo individualizados para cada contato de emails/publico/resultado_publico.csv.

Individualiza por: categoria do orgao, setor do destinatario (com artigo correto), cidade/UF e regra de Ji-Parana.
Quando a pagina de origem lista contatos de OUTROS orgaos (dominio do e-mail != dominio da fonte), o nome do orgao
vem do dominio do e-mail e a cidade nao e usada. Variacoes de redacao escolhidas por hash do e-mail.
Usa SOMENTE fatos confirmados pelo Lucas:
  - OAB/RO 11.037; 5+ anos de contencioso; 150+ processos ativos; estimativa de ~90% de exito
  - estagios na Justica Federal (2018-2019) e na AGU/Procuradoria Federal (2017-2018), em Ji-Parana
  - saude contra Estado e Municipio = experiencia ampla em Direito Administrativo (medicamentos de alto custo,
    tratamentos oncologicos, tutelas de urgencia com jurisprudencia do STJ e do STF)
  - automacao com IA na producao de pecas (~30% menos tempo em contestacoes em massa)
  NAO usa: aprovacoes em MPT/TRT/MPE, nomes de clientes, nem criticas a advocacia privada.
Uso: python3 gerar_emails_publico.py [CV_LINK]
"""
import csv, hashlib, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = f"{HERE}/publico"
CV_LINK = sys.argv[1] if len(sys.argv) > 1 else "[LINK DO CURRICULO]"
PREFS = ["Currículo", "Candidatura"]

def pick(key, opts):
    return opts[int(hashlib.md5(key.encode()).hexdigest(), 16) % len(opts)]

def root(host):
    p = host.lower().removeprefix("www.").split(".")
    return ".".join(p[-3:]) if len(p) >= 3 and p[-2] in ("gov", "jus", "leg", "mp", "def", "tc", "edu", "org", "com", "net") else ".".join(p[-2:])

FEM = ("câmara", "camara", "procuradoria", "defensoria", "assembleia", "secretaria", "universidade", "controladoria", "prefeitura",
       "superintendência", "autarquia", "fundação", "agência", "ordem", "empresa", "companhia", "caixa", "justiça", "corte", "presidência",
       "casa", "escola", "diretoria", "gerência", "coordenadoria", "subseção", "seção", "vara", "promotoria", "advocacia", "gestão")

def artigo(nome):
    w = re.split(r"[\s\-–]", nome.strip())[0].lower() if nome.strip() else ""
    return "da" if w in FEM else "do"

SETOR = {"RH/Pessoas": "gestão de pessoas", "Juridico/Procuradoria": "assessoria jurídica", "Gabinete/Chefia": "chefia de gabinete",
         "Secretaria/Protocolo": "secretaria", "Nominal (cargo)": ""}

def orgao_e_setor(r):
    """devolve (nome_do_orgao, setor_legivel, usar_cidade)"""
    em_dom = root(r["email"].split("@")[1])
    try: src_dom = root(urllib.parse.urlparse(r["fonte"]).netloc)
    except Exception: src_dom = ""
    orgao = re.split(r"\s[-–—]\s|\(|\s+lista de|\s+contatos", r["orgao"])[0].strip(" ,;:")
    usar_cidade = True
    if em_dom != src_dom:                                  # pagina lista contatos de outros orgaos
        lab = r["email"].split("@")[1].split(".")[0]
        orgao = lab.upper() if re.match(r"^(tj|trf|trt|tre|mp|dp|pge|pgm|tc|tce|cge|al|stj|stf|tst|tse|cnj|agu|cgu|dpe|dpu)[a-z0-9]{0,4}$", lab) else ""
        usar_cidade = False
    s = r["setor_cargo"].strip()
    setor = SETOR.get(s, "") or re.sub(r"\s*\([^)]*\)", "", s)
    if len(setor) > 60 or "contato" in setor.lower() or "/" in setor: setor = SETOR.get(r["tipo"], "")
    return orgao, setor.rstrip("."), usar_cidade

CAT = {
 "judiciario_federal": ["Acompanho com respeito o trabalho da Justiça federal e superior, onde dei meus primeiros passos na carreira, como estagiário.",
                        "A Justiça federal foi a minha escola: foi lá que aprendi a redigir decisões e a respeitar o rigor do processo."],
 "judiciario_estadual": ["Escrevo ao Poder Judiciário estadual, cuja rotina conheço de perto como advogado em varas e tribunais.",
                         "Conheço de perto a rotina do Judiciário estadual, onde atuo diariamente como advogado."],
 "mp_defensorias": ["Escrevo a uma instituição essencial à Justiça, cujo papel na defesa da sociedade e dos vulneráveis me inspira.",
                    "O papel da instituição na defesa da sociedade e dos mais vulneráveis é o tipo de missão em que quero trabalhar."],
 "procuradorias_controle": ["Conheço a atuação da advocacia pública e dos órgãos de controle desde os estágios que fiz na Procuradoria Federal e na Justiça Federal.",
                            "Minha formação prática veio da advocacia pública: estagiei na Procuradoria Federal (AGU) e na Justiça Federal."],
 "legislativo_federal_estadual": ["Escrevo ao Poder Legislativo, que demanda assessoria jurídica precisa em proposições, pareceres e atos administrativos.",
                                  "O trabalho jurídico no Legislativo exige precisão em proposições, pareceres e atos administrativos, e é nisso que quero contribuir."],
 "camaras_municipais": ["Escrevo à Câmara Municipal, onde a assessoria jurídica é peça-chave para a legalidade dos atos e das proposições.",
                        "Na Câmara Municipal, a assessoria jurídica garante a legalidade das proposições e dos atos da Casa, e é aí que posso ajudar."],
 "executivo_autarquias": ["Escrevo à administração pública, cujas demandas jurídicas conheço bem por atuar, justamente, contra Estados e Municípios.",
                          "Conheço as demandas jurídicas da administração pública porque atuo, há anos, do outro lado: contra Estados e Municípios."],
 "estatais_sistemas_conselhos": ["Escrevo a uma entidade de interesse público, que exige rigor jurídico e gestão eficiente de carteira de processos.",
                                 "Escrevo a uma entidade de interesse público, onde rigor jurídico e controle de prazos fazem toda a diferença."],
 "ji_parana_regiao": ["Sou de Ji-Paraná e conheço de perto a realidade jurídica local.",
                      "Moro em Ji-Paraná e acompanho de perto a realidade jurídica da nossa região."],
}
ASK = {
 "RH/Pessoas": ["Se houver processo seletivo, vaga de assessoria jurídica, cargo em comissão ou banco de currículos, peço a gentileza de registrar meu nome ou de encaminhar o currículo à área responsável.",
                "Caso haja processo seletivo, contratação ou banco de currículos para a área jurídica, agradeço se puder registrar meu nome ou me indicar o caminho correto."],
 "Juridico/Procuradoria": ["Se a equipe jurídica estiver precisando de reforço, ou se puder indicar o caminho correto para eu me candidatar, ficarei muito agradecido.",
                           "Se houver espaço para um advogado na equipe, ou se puder me indicar a quem enviar o currículo, agradeço desde já."],
 "Gabinete/Chefia": ["Se houver oportunidade em assessoria jurídica ou em cargo de livre nomeação, ou se puder encaminhar meu currículo a quem decide, ficarei muito agradecido.",
                     "Caso haja vaga em assessoria jurídica ou cargo de confiança, ou se puder encaminhar meu currículo a quem decide, serei muito grato."],
 "Secretaria/Protocolo": ["Peço a gentileza de encaminhar meu currículo à área de gestão de pessoas ou à assessoria jurídica, caso haja oportunidade.",
                          "Agradeço se puder encaminhar meu currículo ao setor de gestão de pessoas ou à assessoria jurídica."],
 "Nominal (cargo)": ["Se houver oportunidade na assessoria jurídica, ou se puder encaminhar meu currículo à área responsável, ficarei muito agradecido."],
}
CRED = [
 "Sou advogado (OAB/RO 11.037), com mais de 5 anos de contencioso judicial e administrativo e uma carteira de mais de 150 processos ativos, com taxa de êxito que estimo em torno de 90%.",
 "Atuo como advogado (OAB/RO 11.037) há mais de 5 anos, conduzo mais de 150 processos ativos e estimo meu índice de êxito em cerca de 90%.",
 "Sou Lucas Palhares, advogado (OAB/RO 11.037): mais de 5 anos de contencioso, mais de 150 processos ativos e êxito que estimo em torno de 90%.",
]
START = [
 "Comecei a carreira no serviço público, como estagiário da Procuradoria Federal (AGU) e da Justiça Federal, onde elaborei minutas de petições, despachos, decisões e sentenças. Foi ali que nasceu minha vocação pela vida pública.",
 "Minha trajetória começou no serviço público: estagiei na AGU/Procuradoria Federal e na Justiça Federal, redigindo minutas de decisões e sentenças. Desde então, a vida pública é a minha vocação.",
 "Fui estagiário da AGU (Procuradoria Federal) e da Justiça Federal, redigindo minutas de petições, decisões e sentenças, e dali tirei a certeza de que minha vocação é a vida pública.",
]
ADMIN = [
 "Minha atuação em saúde pública, contra Estados e Municípios (medicamentos de alto custo e tratamentos oncológicos, com tutelas de urgência fundamentadas na jurisprudência do STJ e do STF), me deu ampla experiência em Direito Administrativo.",
 "Atuo há anos em demandas de saúde contra Estados e Municípios, com tutelas de urgência embasadas no STJ e no STF; isso me deu sólida experiência em Direito Administrativo.",
]
TOOLS = ["Também aplico automação com IA à produção de peças, o que reduziu em cerca de 30% o tempo de elaboração de contestações em massa.",
         "Uso automação com IA na produção de peças e na gestão de prazos, o que me permite conduzir grande volume com controle."]
MOVE_YES = [
 "Moro em Ji-Paraná/RO e tenho total disponibilidade para me mudar {para}, ou para qualquer lugar do Brasil.",
 "Estou em Ji-Paraná/RO e, para servir ao órgão, mudo-me {para} ou para qualquer lugar do país.",
]
MOVE_GENERIC = ["Moro em Ji-Paraná/RO e tenho total disponibilidade para me mudar para qualquer lugar do Brasil.",
                "Estou em Ji-Paraná/RO e posso me mudar para qualquer cidade do país, imediatamente."]
MOVE_JI = "Estou à disposição para colaborar, presencialmente, com a equipe local."

def subject(r, key, usar_cidade, dest):
    PREF = pick(key + "p", PREFS)
    if r["ji_parana"] == "sim":
        return pick(key, ["Advogado de Ji-Paraná, ex-estagiário da Justiça Federal e da AGU, à disposição",
                          f"{PREF}: advogado de Ji-Paraná com 150+ processos e passagem pela AGU e Justiça Federal"])
    if usar_cidade and dest:
        base = [f"Advogado ex-estagiário da AGU e da Justiça Federal, 150+ processos e disponível para {dest}",
                f"Advogado com 5+ anos de contencioso e vocação pública: disponível para {dest}",
                f"{PREF}: advogado com experiência em Direito Administrativo, pronto para mudar para {dest}"]
    else:
        base = ["Advogado ex-estagiário da AGU e da Justiça Federal, 150+ processos e disponibilidade total para mudança",
                "Advogado com 5+ anos de contencioso e vocação pública: disponível para mudar para onde for preciso",
                f"{PREF}: advogado com experiência em Direito Administrativo e disponibilidade imediata"]
    return pick(key, base)

def body(r, key):
    orgao, setor, usar_cidade = orgao_e_setor(r)
    ji = r["ji_parana"] == "sim"
    cidade = r.get("cidade", "")
    dest = f"{cidade}/{r['uf']}" if (usar_cidade and cidade and r["uf"] and r["uf"] != "BR") else (cidade if usar_cidade and cidade else "")
    if setor and orgao and orgao.lower() in setor.lower(): saud = f"Prezada equipe de {setor},"
    elif setor and orgao: saud = f"Prezada equipe de {setor} {artigo(orgao)} {orgao},"
    elif setor: saud = f"Prezada equipe de {setor},"
    elif orgao: saud = f"Prezados {artigo(orgao)} {orgao},"
    else: saud = "Prezados senhores,"
    cat = pick(key + "k", CAT.get(r["categoria"], CAT["executivo_autarquias"]))
    if ji: mv = MOVE_JI
    elif dest: mv = pick(key + "m", MOVE_YES).format(para=f"para {dest}")
    else: mv = pick(key + "m", MOVE_GENERIC)
    ask = pick(key + "q", ASK.get(r["tipo"], ASK["Nominal (cargo)"]))
    partes = [saud, cat, pick(key + "c", CRED), pick(key + "s", START), pick(key + "a", ADMIN) + " " + pick(key + "t", TOOLS), mv, ask,
              (f"Meu currículo: {CV_LINK}" if CV_LINK.startswith("http") else pick(key + "l", ["Segue meu currículo em anexo.", "Meu currículo segue em anexo, para a sua apreciação.", "Encaminho, em anexo, o meu currículo."])),
              "Se preferirem não receber novas mensagens, basta responder e não voltarei a escrever.",
              "Atenciosamente,\nLucas Alexandre Horas Palhares\nAdvogado | OAB/RO 11.037\n(69) 99335-9788 | lucaspalharesadv@gmail.com"]
    return "\n\n".join(partes), subject(r, key, usar_cidade, dest)

def main():
    rows = list(csv.DictReader(open(f"{PUB}/resultado_publico.csv", encoding="utf8")))
    out = []
    for r in rows:
        k = r["email"]; corpo, assunto = body(r, k)
        out.append({"email": k, "orgao": r["orgao"], "categoria": r["categoria"], "tipo": r["tipo"], "ji_parana": r["ji_parana"],
                    "assunto": assunto, "corpo": corpo, "status": ""})
    dst = f"{PUB}/emails_prontos.csv"
    with open(dst, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
    words = sorted(len(o["corpo"].split()) for o in out)
    uniq = len({o["corpo"].split("\n\n", 1)[1] for o in out})
    print(f"{len(out)} e-mails em {dst} | palavras: min {words[0]}, mediana {words[len(words)//2]}, max {words[-1]} | corpos distintos (sem saudação): {uniq}")

if __name__ == "__main__":
    main()
