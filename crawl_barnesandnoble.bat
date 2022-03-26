cd src
@REM scrapy runspider crawler_readbooks.py -o ../dataset/test_crawler_readbooks.csv -s LOG_ENABLED=False
scrapy runspider crawler_barnesandnoble.py -o ../dataset/test_crawler_barnesandnoble.csv 
cd ..