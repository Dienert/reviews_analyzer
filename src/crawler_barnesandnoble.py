import scrapy
import json
import math


class BarnesandnobleSpider(scrapy.Spider):
    name = 'barnesandnoblespider'
    totalResults = None
    offset = 0
    limit = 100
    page = 0
    totalPages = None
    # productId = '9780316017930' # ISBN-13 of product - Outliers: The Story of Success
    productId = '9780553381689' # ISBN-13 of product - A Game of Thrones (A Song of Ice and Fire #1)
    url = 'https://api.bazaarvoice.com/data/batch.json\
?passkey=caC2Xb0kazery1Vgcza74qqETLsDbclQWr3kbWiGXSvjI\
&apiversion=5.5\
&displaycode=19386_1_0-en_us\
&resource.q1=reviews\
&filter.q1=productid:eq:{}\
&filter.q1=contentlocale:eq:en_US\
&sort.q1=isfeatured:desc\
&stats.q1=reviews\
&filteredstats.q1=reviews\
&include.q1=authors\
&filter_reviews.q1=contentlocale:eq:en_US\
&filter_reviewcomments.q1=contentlocale:eq:en_US\
&filter_comments.q1=contentlocale:eq:en_US\
&limit.q1={}\
&offset.q1={}\
&callback=BV._internal.dataHandler0'

    start_urls = [url.format(productId, limit, offset)]


    def parse(self, response):
        resp = response.text[26:-1]
        json_resp = json.loads(resp)

        for _, batchedResult in json_resp['BatchedResults'].items():
            if not self.totalResults:
                self.totalResults = batchedResult['TotalResults']
                self.totalPages = math.ceil(self.totalResults/self.limit)

            for result in batchedResult['Results']:

                yield {'reviewer': result.get('UserNickname', ''),
                   'stars': result.get('Rating', ''),
                   'title': result.get('Title', ''),
                   'review': result.get('ReviewText', ''),
                   'date': result.get('SubmissionTime', ''),
                }
                
        if self.page < self.totalPages:
            self.offset += self.limit            
            self.page += 1            
            yield response.follow(self.url.format(self.productId,
                                                  self.limit, 
                                                  self.offset))

