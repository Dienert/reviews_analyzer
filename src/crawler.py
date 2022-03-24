import scrapy

class AmazonSpider(scrapy.Spider):
    name = 'amazonspider'
    start_urls = ['https://www.amazon.com.br/Outliers-Story-Success-Malcolm-Gladwell/product-reviews/0316017930/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews']

    def parse(self, response):
        for review in response.css('*[data-hook=review]'):
            review_text = review.css('*[data-hook="review-body"] span::text').get()
            yield {'reviewer': review.css('.a-profile-name::text').get(),
                   'stars': review.css('span.a-icon-alt::text').get().split(',')[0],
                   'title': review.css('*[data-hook="review-title"] span::text').get(),
                   'review': review_text.strip() if review_text else "",
                   'date': review.css('*[data-hook="review-date"]::text').get(),
                }
        next_page_link = response.css('li.a-last a::attr(href)').get()
        if next_page_link:
            yield response.follow()