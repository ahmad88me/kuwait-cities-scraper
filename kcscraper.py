import requests
from bs4 import BeautifulSoup
import os

URL = "http://moc.gov.kw/English/postalcodes.html"

class_name = "HeadingWhite14B"

# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")
# results = soup.find_all(class_name)


fname_name_dict = {
    "ahmadi": "Ahmadi",
    "capital": "Capital",
    "farwaniyah": "Farwaniyah",
    "hawally": "Hawally",
    "mubarak": "Mubarak Al-Kabeer"
}


def clean_city_name(city_name):
    name = ''.join([i for i in city_name if not i.isdigit()])
    name = name.replace("OFFICE", "")
    name = name.strip()
    return name


def get_cities(fpath):
    with open(fpath) as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all("a", class_=class_name)
    cities = [clean_city_name(c.get_text()) for c in results]
    cities = list(set(cities))
    return cities


def get_all_cities():
    gov = dict()
    for fname in fname_name_dict:
        gov_name = fname_name_dict[fname]
        fpath = os.path.join("data", fname+".html")
        cities = get_cities(fpath)
        gov[gov_name] = cities
    return gov


def write_cities(cities, fname):
    lines = ["Governate,Area"]
    with open(fname, "w") as f:
        for gov in cities:
            for city in cities[gov]:
                line = f"{gov},{city}"
                lines.append(line)
        content = "\n".join(lines)
        f.write(content)
        print(f"\n{len(lines)-1} areas stored in {fname}\n")


def main():
    cities = get_all_cities()
    write_cities(cities, "areas.csv")


if __name__ == "__main__":
    main()