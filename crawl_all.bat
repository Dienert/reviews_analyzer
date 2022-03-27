cd src
scrapy runspider crawler_amazon.py -O ../dataset/amazon.csv
scrapy runspider crawler_barnesandnoble.py -O ../dataset/barnesandnoble.csv
scrapy runspider crawler_flipkart.py -O ../dataset/flipkart.csv 
scrapy runspider crawler_goodreads.py -O ../dataset/goodreads.csv
scrapy runspider crawler_audible.py -O ../dataset/audible.csv
cd ..