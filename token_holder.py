import scrapy
from scrapy.shell import inspect_response
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TokenHolderSpider(scrapy.Spider):
    name = 'token_holder'
    # allowed_domains = ['bscscan.com']
    # start_urls = ['https://bscscan.com/tokens?sort=holders']

    def start_requests(self):
        yield SeleniumRequest(url='https://bscscan.com/tokens?sort=holders', callback=self.parse_item)

    def parse_item(self, response):
        # inspect_response(response, self)

        response = response.selector
        rows = response.xpath('//table/parent::div/following-sibling::div/table//tr')
        for row in rows[1:]:
            token = row.xpath('.//h3/a/@href').get().replace('/token/', '')
            holder_num = row.xpath('.//td[last()]/text()').get()
            yield {
                'token': token,
                'holders': holder_num 
            }
        if response.xpath('(//li[@class="page-item"]/a[@aria-label="Next"])[last()]/@href').get():
            yield SeleniumRequest(url='https://bscscan.com/' + response.xpath('(//li[@class="page-item"]/a[@aria-label="Next"])[last()]/@href').get(),
            wait_time=3,
            callback=self.parse_item,
            wait_until=EC.presence_of_all_elements_located((By.XPATH, '//table/parent::div/following-sibling::div/table//tr')))
