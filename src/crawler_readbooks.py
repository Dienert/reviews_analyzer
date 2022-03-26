import scrapy
import json


class GoodReadersSpider(scrapy.Spider):
    name = 'goodreadsspider'
    start_urls = ['https://www.goodreads.com/book/show/3228917-outliers']
    page = 0 


    def parse(self, response):
        stars_dict = {'it was amazing': 5, 'really liked it': 4, 'liked it': 3, 'it was ok': 2, 'did not like it': 1}

        for review in response.css('.friendReviews'):
            review_text = review.css('.reviewText span span::text').get()
            yield {'reviewer': review.css('*[itemprop="author"] a::attr(name)').get(),
                   'stars': stars_dict.get(review.css('.staticStars::attr(title)').get(), None),
                   'title': '',
                   'review': review_text.strip() if review_text else "",
                   'date': review.css('.reviewDate::text').get(),
                }
        next_page_link = response.css('.next_page::attr(onclick)').get()

        treating_request_parts = next_page_link.split('{')
        url = treating_request_parts[0].split('\'')[1]    
        print(url)
        body = treating_request_parts[1].split('}')[0]



        
        self.page+=1 
        print(self.page)
        # print(next_page_link)
        if next_page_link:
            yield  response.follow(url, method = "GET",body=('{' + body + '}'))
            

