import scrapy 

class Html(scrapy.Spider): 
    name = "planszoPajak" 
    start_urls = 'https://boardgamegeek.com/browse/boardgame?sort=rank&amp;rankobjecttype=subtype&amp;rankobjectid=1'
    download_delay = 5 
    def parse(self, response): 
        zestaw=response.css(".collection_table").xpath(".//tr") 
        for item in zestaw: 
            i = {} 
            i['tytul'] = item.css(".collection_objectname a::text").extract_first() 
            i['url'] = item.css(".collection_objectname a::attr(href)").extract_first() 
            request = scrapy.Request("https://boardgamegeek.com"+str(i['url']), 
                             callback=self.parse_page2) 
            request.meta['i'] = i 
            yield request 
        next_page = response.xpath("//a[@title='next page']").css("a::attr(href)").extract_first() 
        if next_page and '3' not in str(next_page): 
            yield scrapy.Request( 
                response.urljoin(next_page), 
                callback=self.parse 
            )          
    def parse_page2(self, response): 
        i = response.meta['i'] 
        script = str(response.xpath("//html/head/script/text()").extract_first()) 
        x = script.find('"description":') 
        y = script.find('"wiki":') 
        i['overview'] = script[(x+15):(y-2)].replace(',','') 
        yield i


