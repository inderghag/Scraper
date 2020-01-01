from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from filemanagement import *

class Scraper:
    FILENAME = "datafile.json"

    def search_bestbuy(page_source):
        html = page_source

        soup = BeautifulSoup(html, "html.parser")
        item_array = []

        for item in soup.findAll('div', attrs={"class": "col-xs-12_1GBy8 col-sm-4_NwItf col-lg-3_2V2hX x-productListItem productLine_2N9kG"}):
            try:
                item_object = {
                "item": item.find('div', attrs={"itemprop": "name"}).text,
                "price": item.find('span', attrs={"class": "screenReaderOnly_3anTj large_3aP7Z"}).text,
                "rating": item.find('meta', attrs={"itemprop": "ratingValue"})['content'],
                "#ofRatings": item.find('span', attrs={"itemprop": "ratingCount"}).text,
                "link": "https://www.bestbuy.ca/" + item.find('a', attrs={"itemprop": "url"})['href']
                }
        #Exception thrown for ratings that are equal to '0'
            except:
                item_object = {
                    "item": item.find('div', attrs={"itemprop": "name"}).text,
                    "price": item.find('span', attrs={"class": "screenReaderOnly_3anTj large_3aP7Z"}).text,
                    "rating": "0",
                    "#ofRatings": "(0)",
                    "link": "https://www.bestbuy.ca/" + item.find('a', attrs={"itemprop": "url"})['href']
                }
            item_array.append(item_object)

        write_file(item_array, Scraper.FILENAME)

    def search_amazon(page_source):
        html = page_source

        soup = BeautifulSoup(html, "html.parser")
        item_array = []

        for item in soup.findAll('div', attrs={"class": "a-section a-spacing-medium"}):

            #Mulitple try/catch needed because of amazons different formatting styles
            try:
                item_name = item.find('span', attrs={"class": "a-size-medium a-color-base a-text-normal"}).text
            except:
                item_name = item.find('span', attrs={"class": "a-size-base-plus a-color-base a-text-normal"}).text

            try:
                price = item.find('span', attrs={"class": "a-price-whole"}).text + item.find('span', attrs={"class": "a-price-fraction"}).text
            except:
                price = 0

            try:
                rating = item.find('span', attrs={"class": "a-icon-alt"}).text
            except:
                rating = 0

            try:
                num_ratings = item.find('span', attrs={"class": "a-size-base"}).text
            except:
                num_ratings = 0

            try:
                link = "amazon.ca" + item.find('a', attrs={"class": "a-link-normal a-text-normal"})['href']
            except:
                link = "N/A"


            item_object = {
                "item": item_name,
                "price": price,
                "rating": rating,
                "#ofRatings": num_ratings,
                "link": link
            }
            item_array.append(item_object)

        write_file(item_array, Scraper.FILENAME)

    def navigate_bestbuy(search):
        driver = webdriver.Chrome()
        driver.get("https://www.bestbuy.ca/en-ca/category/appliances/26517")

        driver.find_element_by_tag_name("input").send_keys(search + Keys.ENTER)
        driver.get(driver.current_url)
        Scraper.search_bestbuy(driver.page_source)


    def navigate_amazon(search):
        driver = webdriver.Chrome()
        driver.get("https://www.amazon.ca/")

        driver.find_element_by_id("twotabsearchtextbox").send_keys(search + Keys.ENTER)
        driver.get(driver.current_url)

        Scraper.search_amazon(driver.page_source)



search = input("What would you like to find: ")
Scraper.navigate_amazon(search)
Scraper.navigate_bestbuy(search)