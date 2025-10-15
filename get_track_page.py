import requests
import time
from main2 import track_links

for i, url in enumerate(track_links, start=1):
    print(f"Téléchargement {i}/{len(track_links)} : https://{url}")
    course_name = url.split("/")[-1]+".html"
    response = requests.get(f"https://mkwrs.com/mk8dx/{url}")
    with open(course_name, "w") as file:
        file.write(response.text)
    time.sleep(1)

print("Téléchargement terminer")
