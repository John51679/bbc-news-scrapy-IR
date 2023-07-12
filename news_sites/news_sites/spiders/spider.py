import scrapy

class SpiderSpider(scrapy.Spider):

    name = 'spider'
    start_urls = ['http://www.bbc.com/news']
    domain = ['https://www.bbc.com']
    download_delay = 0.5 #Input a delay of 0.5 seconds per html download request.

    #Input: response which contains the html code of the start_urls variable
    #Output: Does not return anything but it creates a callback on method parse_page
    #Functionality: Parses through all news categories and creates a request to visit those urls
    def parse(self, response):
        
        main_categories_xpath = response.xpath('//*[@id="top-navigation"]/nav/ul')
        hrefs = []
        unique_hrefs = []
        

        for h in main_categories_xpath:

            href = h.xpath(".//li/a/@href").extract()
            
            hrefs.append(href)
        
        for i in range(len(hrefs)):
            for j in hrefs[i]:
                if unique_hrefs.count(j) == 0 and j != []:
                    unique_hrefs.append(j)

        unique_hrefs.pop(0)

        for i in range(len(unique_hrefs)):
        #for i in range(1):
            yield scrapy.Request(self.domain[0] + unique_hrefs[i], callback=self.parse_page, errback=self.error)
        
    #Input: response which contains the html code of the visited url category
    #Output: Does not return anything, but creates a callback on method parse_page_content
    #Functionality: Creates a request to visit each news url within a category. 
    def parse_page(self, response):

        href_content_main_path = response.xpath('//*[@id="top-stories"]/../div/div/div[3]/div/div')
        headline_href = response.xpath('//*[@id="topos-component"]/div[3]/div[1]/div/div[1]/div/div[2]/div[1]/a')
        href_to_content = []

        href_to_content.append(headline_href.xpath('.//@href').extract_first())
        for i in href_content_main_path:
            href_to_content.append(i.xpath(".//div/a/@href").extract_first())
            
        for i in href_to_content:
            yield scrapy.Request(self.domain[0] + i, callback=self.parse_page_content, errback=self.error)

    #Input: response which contains the html code of the news url
    #Output: Does not return anything, but it creates the json file
    #Functionality: Isolates the main content and saves it within the json file with tags 'content' and 'url'
    def parse_page_content(self, response):
        
        content_main_path = response.xpath('//*[@id="main-content"]/div[5]/div/div[1]/article/div')
        all_content = []
        all_content_concat = ''

        for i in content_main_path:
            content = i.xpath('.//div/p/text()').extract_first()
            content_bold = i.xpath('.//div/p/b/text()').extract_first()
            if content_bold != None:
                all_content.append(content_bold)
            if content != None:
                all_content.append(content)
        
        for i in all_content:
            all_content_concat = all_content_concat + ' ' + i
        
        if len(all_content) != 0:
            yield {
                'content' : all_content_concat,
                'url' : response.url
            }


    def error(self,failure):
        pass