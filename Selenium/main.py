# pip install beautifulsoup4 lxml requests wheel selenium

import csv
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


shop_url = 'https://tokiny.by/menyu/'


def get_menu_urls():
    r = requests.get(shop_url)
    soup = BeautifulSoup(r.text, 'lxml')

    menu_url = []

    for i in soup.find("div", class_="food-menu-items").findAll('a', href=True):
        link = str(i.get('href'))
        link = link.replace("menyu/", "")
        link = link.replace("/", "")
        menu_url.append(link)

    return menu_url


def get_source_html(url):
    service = Service(executable_path="Selenium/chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()

    try:
        for i in url:
            download_url = f"{shop_url}{i}"
            driver.get(url=download_url)
            time.sleep(3)
            print(f"[INFO] Загружаем страницу, {download_url}")

            with open(f"Selenium/html_data/page_{i}.html", "w", encoding="utf8") as file:
                file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def create_csv_file(url):
    for i in url:
        with open(f"Selenium/csv_data/{i}.csv", "w", encoding="utf8", newline='') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    "Наименование товара",
                    "Цена",
                )
            )


def get_product_name(item):
    product_name = item.find("div", class_="top-food-heading").text.strip()
    return product_name


def get_product_price(item):
    try:
        product_name = item.find("span", class_="new-price without-old ng-binding").text.strip()
    except AttributeError:
        product_name = item.find("span", class_="new-price ng-binding").text.strip()
    return product_name


def collect_data(url):

    data = []

    for page in url:
        with open(f"Selenium/html_data/page_{page}.html", "r", encoding="utf8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("div", class_="top-food-item")

        for item in items_cards:
            product_name = get_product_name(item)
            product_price = get_product_price(item)

            data.append(
                {"product_name": product_name,
                 "product_price": product_price,
                 }
            )

            with open(f"Selenium/csv_data/{page}.csv", "a", encoding="utf8", newline='') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_name,
                        product_price,
                    )
                )
        download_url = f"{shop_url}{page}"
        print(f"[INFO] Обрабатываем страницу {download_url}")


def main():
    url = get_menu_urls()
    print('Получено:', len(url), 'ссылок на меню!')
    get_source_html(url)
    create_csv_file(url)
    collect_data(url)


if __name__ == '__main__':
    main()
