import time
import scrapy
from playwright.sync_api import sync_playwright

class SenheiserSpider(scrapy.Spider):
    name = 'senheiser'

    def start_requests(self):
        with sync_playwright() as p:
            url = 'https://www.sennheiser-hearing.com/ko-KR/headphones/'
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)

            time.sleep(2)
            more_buttons = page.locator('button[data-state="closed"]').nth(0)
            print(more_buttons.text_content())
            more_buttons.click()
            
            time.sleep(3)
            cards = page.query_selector_all('ul#test > li.card')
            cards = [
                {
                    "name": card.query_selector('div[class^="CardGeneric_content"] a').text_content(),
                    "category": card.query_selector('span[class^="CardGeneric_category"]').text_content(),
                    "url": card.query_selector('div[class^="CardGeneric_content"] a').get_attribute('href'),
                    "price": card.query_selector('div[class^="CardGeneric_price"]').text_content()
                }
                for card in cards]
            print(cards)
            browser.close()
        