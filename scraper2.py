import os
import shutil
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


gender = ['men ', 'women ','kids ']
searches = ['sandal','sports shoes' ]
for g in gender:
    for search in searches:
        if g=='kids':
            search = 'shoes'
        if g=='men ' and search=='sandal':
            continue

        options = Options()
        options.headless = False
        driver = webdriver.Chrome(options=options)
        for page in range(0, 100, 48):
            url = 'https://www.adidas.co.in/search?q={}{}&start={}'.format(g,search,page)
            driver.get(url)
            time.sleep(4)
            element = driver.find_elements_by_xpath('//*[@data-auto-id="glass-hockeycard-link"]')
            all_shoes = [e.get_attribute("href") for e in element]

            with open("shoes_page_{}.txt".format(page), "w") as f:
                f.writelines('\n'.join(all_shoes))
                print(page)
            time.sleep(2)
            for shoe in all_shoes:
                print('{:<50} {}'.format(shoe.split("/")[-2], shoe))

        driver.close()

        with open("all_adidas_shoes.txt", "w") as file_to_merge_to:
            for file_to_read_from in [f"shoes_page_{p}.txt" for p in range(0, 100, 48)]:
                with open(file_to_read_from) as file:
                    shutil.copyfileobj(file, file_to_merge_to)
                os.remove(file_to_read_from)


        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "referer": 'https://www.adidas.co.in/search?q=mens%20sneakers',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
        }


        with open("all_adidas_shoes.txt") as f:
            shoes = f.readlines()
        l = []
        print('{:<30} {:<20} {:<50} {:<10} {:<100}'.format('Shoe Name', 'Shoe Model', 'Color', 'Price', 'image url'))
        for shoe in shoes:
            id_ = shoe.split("/")[-1].replace(".html", "")
            shoe_data = requests.get(f"https://www.adidas.co.in/api/search/product/{id_}?sitePath=en", headers=headers).json()
            # print(shoe_data)
            try:
                l.append('{}|{}|{}|{}|{}'.format(shoe.split("/")[-2], shoe_data['modelId'], shoe_data['color'], shoe_data['price'], shoe_data['image']['src']))
            except:
                continue

        with open(g+search, "w") as f:
            f.writelines('\n'.join(l))

# name -> model -> color -> price -> img url