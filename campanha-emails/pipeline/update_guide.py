# -*- coding: utf-8 -*-
"""Insert the mass-list paragraphs (with final counts from out/stats.json) into the campaign guide."""
import json, re, sys
st = json.load(open("out/stats.json", encoding="utf-8"))
tot = st["total"]; aba = st["por_aba"]; mod = st["por_modelo"]; tipo = st["por_tipo"]
g = open("../emails/Guia_campanha_internacional_531_contatos.md", encoding="utf-8").read()
fmt = lambda n: f"{n:,}".replace(",", ".")
p5 = (f"5. Listas em massa ({fmt(tot)} e-mails, entregues em arquivo e com amostra na planilha): BR_PT com {fmt(aba.get('BR_PT',0))} escritórios brasileiros (quinto modelo: advogado remoto e correspondente), "
      f"INT_EN com {fmt(aba.get('INT_EN',0))} escritórios no exterior que recebem o e-mail em inglês (modelos EN e OPS_EN) e INT_PT com {fmt(aba.get('INT_PT',0))} escritórios em Portugal ou de língua portuguesa (modelos PT e OPS_PT). "
      f"Por modelo: BR_PT {fmt(mod.get('BR_PT',0))}, EN {fmt(mod.get('EN',0))}, OPS_EN {fmt(mod.get('OPS_EN',0))}, PT {fmt(mod.get('PT',0))}, OPS_PT {fmt(mod.get('OPS_PT',0))}. "
      f"Por tipo: {fmt(tipo.get('pessoal',0))} e-mails de pessoa nomeada, {fmt(tipo.get('geral',0))} e-mails gerais do escritório e {fmt(tipo.get('rh',0))} de RH. "
      "Como foram montadas: busca por cidade e área (cerca de 660 cidades brasileiras e 600 cidades em 17 países), leitura das páginas de contato e equipe do site de cada escritório, só e-mails publicados pelo próprio escritório (nenhum deduzido por padrão), "
      "exclusão de diretórios, portais, órgãos públicos e sites que não são de advocacia, no máximo 5 e-mails por escritório no Brasil e 4 no exterior, verificação de sintaxe e de DNS (MX ou A) do domínio, e sem repetir nenhum contato da lista curada. "
      "Saudação, modelo e frase de personalização foram gerados automaticamente a partir do site; quando o título do site é só propaganda (por exemplo \"Advogado em Curitiba\"), a linha usa saudação e frase genéricas e a coluna observacoes avisa que o nome do escritório foi deduzido do domínio. "
      "Essas listas se destinam ao envio em volume da seção 13 (domínio separado e ferramenta com aquecimento), não ao Gmail pessoal.")
if "5. Listas em massa (" in g:
    g = re.sub(r"5\. Listas em massa \(.*?\n", p5 + "\n", g, count=1, flags=re.S)
else:
    g = g.replace("4. Os textos de follow-up (seção 7) e o roteiro da ligação de 20 minutos (seção 9).\n", "4. Os textos de follow-up (seção 7) e o roteiro da ligação de 20 minutos (seção 9).\n" + p5 + "\n", 1)
files = ("Listas em massa (arquivos enviados no chat e guardados no repositório GitHub meu-projeto, pasta campanha-emails/listas-massa): Lista_massa_10k.xlsx (abas Resumo, BR_PT, INT_EN, INT_PT), Lista_massa_completa.csv, Lista_massa_BR_PT.csv, Lista_massa_INT_EN.csv, Lista_massa_INT_PT.csv, "
         "Instantly_BR_PT.csv, Instantly_EN.csv, Instantly_OPS_EN.csv, Instantly_PT.csv, Instantly_OPS_PT.csv (prontos para importar no Instantly ou Smartlead, um por campanha) e rejeitados_dns.csv (e-mails descartados por domínio sem DNS).\n"
         "Currículo em português para o modelo BR_PT: Lucas_Palhares_Curriculo_Advogado_Remoto.pdf (Drive).\n")
if "Listas em massa (arquivos" not in g:
    g = g.replace("Este guia: também no Google Drive como documento.\n", files + "Este guia: também no Google Drive como documento.\n", 1)
open("../emails/Guia_campanha_internacional_531_contatos.md", "w", encoding="utf-8").write(g)
print("guia atualizado", tot)
