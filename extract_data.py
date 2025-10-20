from bs4 import BeautifulSoup
import os
import re

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
                if len(cells) < 14:
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

# Nettoyage des données
print("\nNettoyage des données en cours...")


def convert_time_to_ms(time_str):
    if not time_str:
        return None
    match = re.match(r"(\d+)'(\d+)\"(\d+)", time_str)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        milliseconds = int(match.group(3))
        total_ms = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
        return total_ms
    else:
        return None


def convert_lap_to_ms(lap_float):
    if not lap_float or lap_float == "":
        return None
    try:
        lap_seconds = float(lap_float)
        lap_ms = int(lap_seconds * 1000)
        return lap_ms
    except ValueError:
        return None


for record in data:
    record["time_ms"] = convert_time_to_ms(record["time"])
    if "lap 1" in record:
        record["lap1_ms"] = convert_lap_to_ms(record["lap 1"])
    if "lap 2" in record:
        record["lap2_ms"] = convert_lap_to_ms(record["lap 2"])
    if "lap 3" in record:
        record["lap3_ms"] = convert_lap_to_ms(record["lap 3"])
    if record["nationality"]:
        record["nationality"] = record["nationality"].split()[0]

print("Nettoyage terminé !")
print("\nAperçu des données NETTOYÉES :")
for i in range(min(3, len(data))):
    print(f"\n{i+1}. {data[i]["course"]}")
    print(f"   Temps brut: {data[i]["time"]}")
    print(f"   Temps (ms): {data[i]["time_ms"]}")
    print(f"   Lap 1, 2, 3 : {data[i].get("lap1_ms")} / {data[i].get("lap2_ms")} / {data[i].get("lap3_ms")}")
