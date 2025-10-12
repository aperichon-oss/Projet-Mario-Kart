import requests
from bs4 import BeautifulSoup

response = requests.get("https://mkwrs.com/mk8dx/")
content_html = response.text
soup = BeautifulSoup(content_html, "html.parser")
# with open("test.html", "w") as file:
#     file.write(response.text)


def all_track_links(content):
    track_links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "track" in href and "=200" not in href:
            track_links.add(href)
    track_links = list(track_links)
    return track_links


track_links = all_track_links(all_track_links)
print(f"Nombre de liens : {len(track_links)}")
print(f"Liste de liens : {track_links}")
