from bs4 import BeautifulSoup
import os
import re
import main
import main2
import get_track_page


def extract_data_from_directory(directory="."):
    data = []
    course_to_ignore = "display.php?track=GCN+Baby+Park.html"
    for file in os.listdir():
        if file.endswith(".html"):
            if course_to_ignore in file:
                print(f"IGNORÉ : Le fichier {file} correspond à la course {course_to_ignore}.")
                continue
            print(f"Lecture de {file}...")
            filepath = os.path.join(directory, file)
            records = parse_html_file(filepath)
            data.extend(records)
    print(f"\nExtraction terminée : {len(data)} records trouvés")
    return data


def parse_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        tables = soup.find_all("table", class_="wr")
        if len(tables) < 2:
            print(f"Pas assez de tables dans {filepath}")
            return []
        table = tables[1]
        rows = table.find_all("tr")[1:]
        course_name = os.path.basename(filepath).replace(".html", "").replace("display.php?track=", "").replace("+", " ")
        records = []
        for row in rows:
            record = extract_row_data(row, course_name)
            if record:
                records.append(record)
        return records


def extract_row_data(row, course_name):
    cells = row.find_all("td")
    if len(cells) < 14:
        return None
    img = cells[3].find("img")
    nationality = img["alt"].split()[0] if img and img.get("alt") else ""
    return {
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
    }


def display_preview(data, n=5):
    print("\nAperçu des données :")
    for i in range(min(n, len(data))):
        print(f"\n{i+1}. {data[i]['course']}")
        print(f"   Temps: {data[i]['time']}")
        print(f"   Pays: {data[i]['nationality']}")
        print(f"   Lap 1, 2, 3: {data[i]['lap 1']} / {data[i]['lap 2']} / {data[i]['lap 3']}")
        print(f"   Setup: {data[i]['character']} / {data[i]['kart']} / {data[i]['tires']} / {data[i]['glider']}")


# Nettoyage des données


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


def normalize_str(character_name, tires_name):
    normalized_char = character_name
    normalized_tires = tires_name
    if character_name.startswith("Heavy Mii"):
        normalized_char = "Heavy Mii"
    elif character_name.startswith("Medium Mii"):
        normalized_char = "Medium Mii"
    elif character_name.startswith("Light Mii"):
        normalized_char = "Light Mii"
    elif character_name.endswith("Yoshi"):
        normalized_char = "Yoshi"
    elif character_name.startswith("Birdo"):
        normalized_char = "Birdo"
    if tires_name.endswith("Roller"):
        normalized_tires = "Roller"
    return normalized_char, normalized_tires


def clean_data(data):
    print("\nNettoyage des données en cours...")
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
        record["character"], record["tires"] = normalize_str(record["character"], record["tires"])
    print("Nettoyage terminé !")
    return data


def display_cleaned_preview(data, n=3):
    print("\nAperçu des données NETTOYÉES :")
    for i in range(min(n, len(data))):
        print(f"\n{i+1}. {data[i]["course"]}")
        print(f"   Temps brut: {data[i]["time"]}")
        print(f"   Temps (ms): {data[i]["time_ms"]}")
        print(f"   Lap 1, 2, 3 : {data[i].get("lap1_ms")} / {data[i].get("lap2_ms")} / {data[i].get("lap3_ms")}")


def save_to_csv(data, filename="Test.csv"):
    with open("Test.csv", "w") as file:
        file.write("Course;")
        file.write("Temps;")
        file.write("Pays;")
        file.write("Tour 1;")
        file.write("Tour 2;")
        file.write("Tour 3;")
        file.write("Personnage;")
        file.write("Véhicule;")
        file.write("Roues;")
        file.write("Deltaplane;\n")
        for i in range(len(data)):
            file.write(f"{data[i]["course"]};")
            file.write(f"{data[i]["time_ms"]};")
            file.write(f"{data[i]["nationality"]};")
            file.write(f"{data[i]["lap1_ms"]};")
            file.write(f"{data[i]["lap2_ms"]};")
            file.write(f"{data[i]["lap3_ms"]};")
            file.write(f"{data[i]["character"]};")
            file.write(f"{data[i]["kart"]};")
            file.write(f"{data[i]["tires"]};")
            file.write(f"{data[i]["glider"]};\n")


def all_fonctions():
    data = extract_data_from_directory()
    display_preview(data)
    data = clean_data(data)
    display_cleaned_preview(data)
    save_to_csv(data)


if __name__ == "__main__":
    main
    main2
    get_track_page
    all_fonctions()
