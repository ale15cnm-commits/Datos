
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"

datos = []

for pagina in range(1, 11):

    if pagina == 1:
        url_pagina = url
    else:
        url_pagina = f"{url}page/{pagina}/"

    print("Procesando:", url_pagina)

    response = requests.get(url_pagina)
    response.encoding = "utf-8"

    texto = BeautifulSoup(response.text, "html.parser")

    frases = texto.find_all("div", class_="quote")

    for frase in frases:

        texto_tag = frase.find("span", class_="text")
        autor_tag = frase.find("small", class_="author")
        etiquetas_tag = frase.find_all("a", class_="tag")

        if texto_tag and autor_tag:

            etiquetas = ", ".join(
                [etiqueta.text.strip() for etiqueta in etiquetas_tag]
            )

            datos.append({
                "frase": texto_tag.text.strip(),
                "autor": autor_tag.text.strip(),
                "etiquetas": etiquetas
            })

df = pd.DataFrame(datos)

df = df.drop_duplicates()

df.to_csv(
    "catalogo_frases.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Scraping terminado.")
print("Total de frases:", len(df))
