import scrapy
import json


class BarnesandnobleSpider(scrapy.Spider):
    name = 'barnesandnoblespider'
    start_urls = ['https://api.bazaarvoice.com/data/batch.json?passkey=caC2Xb0kazery1Vgcza74qqETLsDbclQWr3kbWiGXSvjI&apiversion=5.5&displaycode=19386_1_0-en_us&resource.q0=products&filter.q0=id:eq:9780316017930&stats.q0=reviews&filteredstats.q0=reviews&filter_reviews.q0=contentlocale:eq:en_US&filter_reviewcomments.q0=contentlocale:eq:en_US&resource.q1=reviews&filter.q1=isratingsonly:eq:false&filter.q1=productid:eq:9780316017930&filter.q1=contentlocale:eq:en_US&sort.q1=isfeatured:desc&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors,products,comments&filter_reviews.q1=contentlocale:eq:en_US&filter_reviewcomments.q1=contentlocale:eq:en_US&filter_comments.q1=contentlocale:eq:en_US&limit.q1=8&offset.q1=0&limit_comments.q1=3&callback=BV._internal.dataHandler0']
    # start_urls = ['https://www.barnesandnoble.com/w/outliers-malcolm-gladwell/1100030024?ean=9780316017930']
    page = 0 


    def parse(self, response):
        resp = response.text[26:-1]
        # print(resp)
        # print(type(resp))
        json_resp = json.loads(resp)

        #check new data type
        # print(type(json_resp))
        # print(json_resp)
            
            
        # stars_dict = {'it was amazing': 5, 'really liked it': 4, 'liked it': 3, 'it was ok': 2, 'did not like it': 1}

        for _, batchedResult in json_resp['BatchedResults'].items():#['q0']['Results']:
            for result in batchedResult['Results']:

                yield {'reviewer': result.get('UserNickname', ''),
                   'stars': result.get('Rating', ''),
                   'title': result.get('Title', ''),
                   'review': result.get('ReviewText', ''),
                   'date': result.get('SubmissionTime', ''),
                }
                
        # next_page_link = response.css('bv-content-pagination-buttons-item a::attr(href)').get()
        # if next_page_link:
        #     yield response.follow(next_page_link)

            

