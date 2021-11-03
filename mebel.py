import requests
from decouple import config
from bs4 import BeautifulSoup
import csv


URL = "https://www.ikea.com/ru/ru/cat/divany-iz-kozhi-iskusstvennoy-kozhi-10662/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "accept": "*/*"
}
LINK = "https://www.ikea.com"
PATH = "mebel.csv"


def get_html(url, params=None):
    request = requests.get(url, headers=HEADERS, params=params)
    return request


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    mebels = soup.find_all("div", class_="range-revamp-product-compact")
    furniturs = []
    for divan in mebels:
        furniturs.append(
            {
            "Название": divan.find("div", class_="range-revamp-header-section__title--small notranslate").get_text().replace("\n", ""),
            "Описание": divan.find("span", class_="range-revamp-header-section__description-text").get_text().replace("\n", ""),
            "Цена": divan.find("span", class_="range-revamp-price__integer").get_text().replace("\n", ""),
            "Ссылка": "https://www.ikea.com"+divan.find("a",class_ = "range-revamp-product-compact__wrapper-link").get("href")
            }
        )
    return furniturs


def save_csv(mebels,path):
    with open(path, "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["","Name", "Description", "Price", "Link"])
        counter = 1
        for mebel in mebels:
            writer.writerow([counter, mebel["Название"], mebel["Описание"], mebel["Цена"],  mebel["Ссылка"]])
            counter += 1

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        divans = get_content(html.text)
        save_csv(divans, PATH)
        print(divans)
parse()
