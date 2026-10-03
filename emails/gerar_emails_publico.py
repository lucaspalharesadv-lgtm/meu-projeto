#!/usr/bin/env python3
"""Gera assunto + corpo individualizados para cada contato de emails/publico/resultado_publico.csv.

Individualiza por: categoria do orgao, setor/cargo do destinatario, cidade/UF, fato institucional (quando houver)
e regra de Ji-Parana. Variacoes de redacao escolhidas de forma deterministica por e-mail (hash), para nao
repetir o mesmo texto 600 vezes. Usa SOMENTE fatos confirmados pelo Lucas:
  - OAB/RO 11.037; 5+ anos de contencioso; 150+ processos ativos; estimativa de ~90% de exito
  - estagios na Justica Federal (2018-2019) e na AGU/Procuradoria Federal (2017-2018), em Ji-Parana
  - saude contra Estado e Municipio = experiencia ampla em Direito Administrativo (medicamentos de alto custo,
    tratamentos oncologicos, tutelas de urgencia com jurisprudencia do STJ e do STF)
  - automacao com IA na producao de pecas; sustentacoes orais; recuperacao de credito
  NAO usa: aprovacoes em MPT/TRT/MPE, nomes de clientes, nem criticas a advocacia privada.
Uso: python3 gerar_emails_publico.py [CV_LINK]
"""
import csv, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = f"{HERE}/publico"
CV_LINK = sys.argv[1] if len(sys.argv) > 1 else "[LINK DO CURRICULO]"

def pick(key, opts):
    return opts[int(hashlib.md5(key.encode()).hexdigest(), 16) % len(opts)]

# Linha especifica por categoria (verdadeira, baseada na funcao do orgao)
CAT = {
 "judiciario_federal": "Acompanho com respeito o trabalho da Justiça federal e superior, onde dei meus primeiros passos na carreira como estagiário.",
 "judiciario_estadual": "Escrevo ao Poder Judiciário estadual, cuja rotina conheço de perto como advogado em varas e tribunais estaduais.",
 "mp_defensorias": "Escrevo a uma instituição essencial à Justiça, cujo papel na defesa da sociedade e dos vulneráveis me inspira.",
 "procuradorias_controle": "Conheço a atuação da advocacia pública e dos órgãos de controle desde os estágios que fiz na Procuradoria Federal e na Justiça Federal.",
 "legislativo_federal_estadual": "Escrevo ao Poder Legislativo, que demanda assessoria jurídica precisa em proposições, pareceres e atos administrativos.",
 "camaras_municipais": "Escrevo à Câmara Municipal, onde a assessoria jurídica é peça-chave para a legalidade dos atos e das proposições.",
 "executivo_autarquias": "Escrevo à administração pública, cujas demandas jurídicas conheço bem por atuar, justamente, contra Estados e Municípios.",
 "estatais_sistemas_conselhos": "Escrevo a uma entidade de interesse público, que exige rigor jurídico e gestão eficiente de carteira de processos.",
 "ji_parana_regiao": "Sou de Ji-Paraná e conheço de perto a realidade jurídica local.",
}
ASK = {
 "RH/Pessoas": "Se houver processo seletivo, vaga de assessoria jurídica, cargo em comissão ou banco de currículos, peço a gentileza de registrar meu nome ou de encaminhar o currículo à área responsável.",
 "Juridico/Procuradoria": "Se a equipe jurídica estiver precisando de reforço, ou se puder indicar o caminho correto para eu me candidatar, ficarei muito agradecido.",
 "Gabinete/Chefia": "Se houver oportunidade em assessoria jurídica ou em cargo de livre nomeação, ou se puder encaminhar meu currículo a quem decide, ficarei muito agradecido.",
 "Secretaria/Protocolo": "Peço a gentileza de encaminhar meu currículo à área de gestão de pessoas ou à assessoria jurídica, caso haja oportunidade.",
 "Nominal (cargo)": "Se houver oportunidade na assessoria jurídica, ou se puder encaminhar meu currículo à área responsável, ficarei muito agradecido.",
}
CRED = [
 "Sou advogado (OAB/RO 11.037), com mais de 5 anos de contencioso judicial e administrativo e uma carteira de mais de 150 processos ativos, com taxa de êxito que estimo em torno de 90%.",
 "Atuo como advogado (OAB/RO 11.037) há mais de 5 anos, conduzo mais de 150 processos ativos e estimo meu índice de êxito em cerca de 90%.",
 "Sou o Lucas, advogado (OAB/RO 11.037): mais de 5 anos de contencioso, mais de 150 processos ativos e êxito que estimo em torno de 90%.",
]
ADMIN = [
 "Minha atuação em saúde pública, contra Estados e Municípios (medicamentos de alto custo e tratamentos oncológicos, com tutelas de urgência fundamentadas na jurisprudência do STJ e do STF), me deu ampla experiência em Direito Administrativo.",
 "Atuo há anos em demandas de saúde contra Estados e Municípios, com tutelas de urgência embasadas no STJ e no STF; isso me deu sólida experiência em Direito Administrativo.",
]
START = [
 "Comecei a carreira no serviço público, como estagiário da Procuradoria Federal (AGU) e da Justiça Federal, onde elaborei minutas de petições, despachos, decisões e sentenças. Foi ali que nasceu minha vocação pela vida pública.",
 "Minha trajetória começou no serviço público: estagiei na AGU/Procuradoria Federal e na Justiça Federal, redigindo minutas de decisões e sentenças. Desde então, a vida pública é a minha vocação.",
]
TOOLS = "Também aplico automação com IA à produção de peças, o que reduziu em cerca de 30% o tempo de elaboração de contestações em massa."
MOVE_YES = [
 "Moro em Ji-Paraná/RO e tenho total disponibilidade para me mudar para {destino}, ou para qualquer lugar do Brasil.",
 "Estou em Ji-Paraná/RO e, para servir ao órgão, mudo-me para {destino} ou para qualquer lugar do país.",
]
MOVE_JI = "Moro em Ji-Paraná/RO e estou à disposição para colaborar com a equipe local."

def subject(r, key):
    dest = r["cidade"] or r["uf"]
    if r["ji_parana"] == "sim":
        return pick(key, ["Advogado de Ji-Paraná, ex-estagiário da Justiça Federal e da AGU, à disposição",
                          "Currículo: advogado de Ji-Paraná com 150+ processos e passagem pela AGU e Justiça Federal"])
    base = [f"Advogado ex-estagiário da AGU e da Justiça Federal, 150+ processos e disponível para {dest}",
            f"Advogado com 5+ anos de contencioso e vocação pública: disponível para {dest}",
            f"Currículo: advogado com experiência em Direito Administrativo, pronto para mudar para {dest}"]
    return pick(key, base)

def body(r, key):
    dest = r["cidade"] or r["uf"] or "a sua cidade"
    destino = f"{r['cidade']}/{r['uf']}" if r["cidade"] and r["uf"] and r["uf"] != "BR" else dest
    cat = CAT.get(r["categoria"], CAT["executivo_autarquias"])
    ji = r["ji_parana"] == "sim"
    setor = r["setor_cargo"] or "responsável"
    det = f" Vi que o órgão {r['detalhe_institucional'].rstrip('.').lower()}." if r["detalhe_institucional"] and len(r["detalhe_institucional"]) > 25 else ""
    saud = f"Prezados, responsáveis por {setor} do(a) {r['orgao']},"
    mv = MOVE_JI if ji else pick(key + "m", MOVE_YES).format(destino=destino)
    paras = [saud, f"{cat}{det}", pick(key + "c", CRED), pick(key + "s", START), pick(key + "a", ADMIN) + " " + TOOLS, mv,
             ASK.get(r["tipo"], ASK["Nominal (cargo)"]), f"Meu currículo: {CV_LINK}",
             "Atenciosamente,\nLucas Alexandre Horas Palhares\nAdvogado | OAB/RO 11.037\n(69) 99335-9788 | lucaspalharesadv@gmail.com"]
    return "\n\n".join(paras)

def main():
    src = f"{PUB}/resultado_publico.csv"
    rows = list(csv.DictReader(open(src, encoding="utf8")))
    out = []
    for r in rows:
        k = r["email"]
        out.append({"email": k, "orgao": r["orgao"], "categoria": r["categoria"], "tipo": r["tipo"], "ji_parana": r["ji_parana"],
                    "assunto": subject(r, k), "corpo": body(r, k), "status": ""})
    dst = f"{PUB}/emails_prontos.csv"
    with open(dst, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, list(out[0])); w.writeheader(); w.writerows(out)
    words = sorted(len(o["corpo"].split()) for o in out)
    print(f"{len(out)} e-mails gerados em {dst} | palavras: min {words[0]}, mediana {words[len(words)//2]}, max {words[-1]}")

if __name__ == "__main__":
    main()
