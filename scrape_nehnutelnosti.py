from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


if __name__ == "__main__":
    ls_prices = []
    ls_prices_m2 = []
    ls_ads = []
    ads_n=0
    URL = "https://www.nehnutelnosti.sk/3-izbove-byty/predaj/?p%5Blocation%5D=t9.t7.t8"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    a = soup.find_all("a",{"class":"component-pagination__arrow-color d-flex align-items-center"})
    next_page_href = a[0]["href"]
    print(0)
    ads = soup.find_all("div", 
                        {"class": [
                            "advertisement-item default-perex-rows is-dev-project mx-auto mb-4",
                            "advertisement-item default-perex-rows package--profi is-dev-project mx-auto mb-4",
                            "advertisement-item default-perex-rows perex-rows-3 is-dev-project mx-auto mb-4",
                            "advertisement-item default-perex-rows perex-rows-3 package--profi is-dev-project mx-auto mb-4",
                            
                        ]})
    print(len(ads))
    ads_n +=len(ads)
    for item in ads:
        href = item.find("a", {"class": "advertisement-item--content__title d-block text-truncate"})["href"]
        prices = item.find("div", {"class": "advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end"})

        try:
            price, price_m2, _ = prices.text.replace(" ", "").replace(",", ".").replace("\n", "").split("€")
            ls_prices.append(int(price))
            ls_prices_m2.append(int(np.round(float(price_m2), 0)))
            ls_ads.append(href)
        except ValueError as e:
            print(prices)
            pass  

    i=1
    while next_page_href:
        print(i)
        print(next_page_href)
        
        page = requests.get(next_page_href)
        soup = BeautifulSoup(page.content, "html.parser")
        a = soup.find_all("a",{"class":"component-pagination__arrow-color d-flex align-items-center"})
        
        i+=1
        ads = soup.find_all("div", 
                            {"class": [
                                "advertisement-item default-perex-rows is-dev-project mx-auto mb-4",
                                "advertisement-item default-perex-rows package--profi is-dev-project mx-auto mb-4",
                                "advertisement-item default-perex-rows perex-rows-3 is-dev-project mx-auto mb-4",
                                "advertisement-item default-perex-rows perex-rows-3 package--profi is-dev-project mx-auto mb-4"
                            ]})
        print(len(ads))
        ads_n+=len(ads)
        for item in ads:
            href = item.find("a", {"class": "advertisement-item--content__title d-block text-truncate"})["href"]
            prices = item.find("div", {"class": "advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end"})
            
            try:
                price, price_m2, _ = prices.text.replace(" ", "").replace(",", ".").replace("\n", "").split("€")
                ls_prices.append(int(price))
                ls_prices_m2.append(int(np.round(float(price_m2), 0)))
                ls_ads.append(href)
            except ValueError as e:
                print(prices)
                pass
        try:
            next_page_href = a[1]["href"]
        except IndexError as e:
            next_page_href = None
    

    pd_nehnutelnosti = pd.DataFrame({"price": ls_prices, "price_m2":ls_prices_m2, "ads": ls_ads})
    pd_nehnutelnosti["date"] = datetime.today().strftime('%Y-%m-%d')
    pdf_previous = pd.read_csv("nehnutelosti_lamac_dubravka_karlovka.csv")
    pdf_merged = pd_nehnutelnosti = pd.concat([pdf_previous, pd_nehnutelnosti], axis=0).reset_index(drop=True).drop_duplicates()
    pdf_merged.to_csv("nehnutelosti_lamac_dubravka_karlovka.csv", index=False)