from bs4 import BeautifulSoup
import os

data = []
for file in os.listdir():
    if file.endswith(".html"):
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
            tables = soup.find_all("table", class_="wr")
            if len(tables) < 2:
                continue
            table = tables[1]
            rows = table.find_all("tr")[1:]
            for row in rows:
                cols = [td.text.strip() for td in row.find_all("td")]
                if len(cols) > 0:
                    data.append({
                        "course": file.replace(".html", ""),
                        "time": cols[1] if len(cols) > 1 else "",
                        "character": cols[10] if len(cols) > 2 else "",
                        "kart": cols[11] if len(cols) > 3 else "",
                        "wheels": cols[12] if len(cols) > 4 else "",
                        "glider": cols[13] if len(cols) > 5 else "",
                    })

print(f"Extraction terminée : {len(data)} lignes récupérées")
