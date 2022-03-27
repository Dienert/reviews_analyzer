import scrapy

class AudibleSpider(scrapy.Spider):
    name = 'audiblespider'
    page = 0
    totalPages = 100
    url = 'https://www.audible.com/pd/reviews?country=US&asin=B002UZDRK8&sort=MostHelpful&filter=allStars&page={}&pageSize=50&showPaging=false'
    start_urls = [url.format(page)]

    def parse(self, response):
        for review in response.css('.bc-row-responsive.bc-spacing-top-s4.bc-spacing-s5'):
            review_text = review.css('.bc-text.bc-spacing-small.bc-spacing-top-none.bc-size-body.bc-color-secondary::text').get()
            review_title = review.css('.bc-heading.bc-color-base.bc-pub-break-word.bc-spacing-base.bc-size-title1.bc-text-bold.bc-text-emphasis::text').get()
            review_date = review.css('.bc-list-item.bc-color-secondary::text').get()

            yield {
                   'reviewer': review.css('a.bc-link.bc-color-link.bc-text-ellipses::text').get(),
                   'stars': review.css('.bc-text.bc-pub-offscreen::text').get()[0],
                   'title': review_title.strip() if review_title else "",
                   'review': review_text.strip() if review_text else "",
                   'date': review_date.strip() if review_date else "",                
                   }
        if self.page < self.totalPages:      
            self.page += 1            
            yield response.follow(self.url.format(self.page))


