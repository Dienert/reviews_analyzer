cd src
@REM scrapy runspider crawler_readbooks.py -o ../dataset/test_crawler_readbooks.csv -s LOG_ENABLED=False
scrapy runspider crawler_flipkart.py -O ../dataset/test_crawler_flipkart.csv 
cd ..