from bs4 import BeautifulSoup
import os

data = []

for file in os.listdir():
    if file.endswith(".html"):
        print(f"Lecture de {file}...")
        with open(file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            tables = soup.find_all("table", class_="wr")
            if len(tables) < 2:
                print(f"Pas assez de tables dans {file}")
                continue
            table = tables[1]
            rows = table.find_all("tr")[1:]
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 10:
                    continue
                img = cells[3].find("img")
                if img and img.get("alt"):
                    nationality = img["alt"].split()[0]
                else:
                    nationality = ""
                course_name = file.replace(".html", "").replace("display.php?track=", "")
                course_name = course_name.replace("+", " ")
                data.append({
                    "course": course_name,
                    "time": cells[1].text.strip(),
                    "nationality": nationality,
                    "lap 1": cells[5].text.strip(),
                    "lap 2": cells[6].text.strip(),
                    "lap 3": cells[7].text.strip(),
                    "character": cells[10].text.strip(),
                    "kart": cells[11].text.strip(),
                    "tires": cells[12].text.strip(),
                    "glider": cells[13].text.strip(),
                })
print(f"\nExtraction terminée : {len(data)} records trouvés")
print("\nAperçu des données :")
for i in range(min(5, len(data))):
    print(f"\n{i+1}. {data[i]["course"]}")
    print(f"   Temps: {data[i]["time"]}")
    print(f"   Pays: {data[i]["nationality"]}")
    print(f"   Lap 1, 2, 3: {data[i]["lap 1"]} / {data[i]["lap 2"]} / {data[i]["lap 3"]}")
    print(f"   Setup: {data[i]["character"]} / {data[i]["kart"]} / {data[i]["tires"]} / {data[i]["glider"]}")
