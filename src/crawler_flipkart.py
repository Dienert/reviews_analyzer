import scrapy

class FlipkartSpider(scrapy.Spider):
    name = 'flipkartspider'
    start_urls = ['https://www.flipkart.com/outliers/product-reviews/itmfc4z8jfyhcxby?pid=9780141036250&lid=LSTBOK9780141036250O7N8L3&marketplace=FLIPKART']

    def parse(self, response):
        for review in response.css('._27M-vq'):
            review_text = review.css('._27M-vq .t-ZTKy div div::text').get()
            yield {
                   'reviewer': review.css('p._2sc7ZR._2V5EHH::text').get(),
                   'stars': review.css('._3LWZlK::text').get(),
                   'title': review.css('._2-N8zT::text').get(),
                   'review': review_text.strip() if review_text else "",
                   'date': review.xpath('//*[@class="_2a1p_T"]/../*/text()')[-1].get() if review_text else ""
                }

        next_page_link = response.xpath('//*[@class="yFHi8N"]/*/@href')[-1].get()
        print(next_page_link)
        if next_page_link:
            yield response.follow(next_page_link)
