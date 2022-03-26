import scrapy
from scrapy.http.request import Request
from scrapy.selector import Selector
import os

class GoodReadersSpider(scrapy.Spider):
    name = 'goodreadsspider'
    
    product_id = '3228917-outliers'

    front_url = 'https://www.goodreads.com/book/show/{}'

    api_url = 'https://www.goodreads.com/book/reviews/3228917-outliers\
?hide_last_page=true\
&language_code=en\
&page={}\
&authenticity_token={}'

    page = 0 

    def start_requests(self):
        # yield scrapy.Request(url=self.front_url.format(self.product_id), callback=self.get_token)
        yield scrapy.Request(url=self.front_url.format(self.product_id))

    def get_token(self, response):
        # <meta name="csrf-token" content="bF1Bi77f7utYi63ZXiMYfIIhNGd4ohD5HvauysHZKw1zbkqQdzxf5+cuFqsa1f3WpZVzvb17pMSLYvNF4T12cQ==">
        next_page_code = response.css('.next_page::attr(onclick)').get()
        token = next_page_code.split('encodeURIComponent(\'')[1].split('\')}); return false;')[0]
        print(f"First token: {token}")
        parameters = ','.join(next_page_code.split(',')[1:]).split('); return false;')[0].strip()
        print(f"Parameters: {parameters}")


        # r = requests.get(self.api_url.format(0, token), json=parameters)
        # yield Request(self.api_url.format(0, token), self.parse, method="GET", body=parameters)
        curl_command = f'curl -X GET -H "Content-type: application/json" -H "Accept: application/json" -d \'{parameters}\' "{self.api_url.format(0, token)}\"'
        print(curl_command)
        result = os.system(curl_command)
        print(result)

    def parse(self, response):
        # ajax_page_text = response.text[26:-2]
        # response = Selector(text=ajax_page_text)

        stars_dict = {'it was amazing': 5, 'really liked it': 4, 'liked it': 3, 'it was ok': 2, 'did not like it': 1}

        for review in response.css('.friendReviews'):
            review_text = review.css('.reviewText span span::text').get()
            yield {'reviewer': review.css('*[itemprop="author"] a::attr(name)').get(),
                   'stars': stars_dict.get(review.css('.staticStars::attr(title)').get(), None),
                   'title': '',
                   'review': review_text.strip() if review_text else "",
                   'date': review.css('.reviewDate::text').get(),
                }
        # next_page_link = response.css('.next_page::attr(onclick)').get()

        # treating_request_parts = next_page_link.split('{')
        # url = treating_request_parts[0].split('\'')[1]    
        # print(url)
        # body = treating_request_parts[1].split('}')[0]



        
        # self.page+=1 
        # print(self.page)
        # # print(next_page_link)
        # if next_page_link:
        #     yield  response.follow(url, method = "GET",body=('{' + body + '}'))
            

