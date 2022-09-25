import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://weaverauctions.com/allseach_item.php?querystr={}'

class WeaverSpider(scrapy.Spider):
    name = 'weaver'

    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):   

        links = response.css("div.g-mb-30 a::attr(href)")
        images = response.css("img.img-thumbnail::attr(src)").getall()
        counter = 0    
        for link in links:
            link_get = link.get()           
            url = link_get[1:]  
            image = images[counter]
            image_link = "https://weaverauctions.com"+image[1:]                  
            yield response.follow("https://weaverauctions.com"+url, callback=self.parse_item, cb_kwargs={'index':index, 'image':image_link})  
            counter = counter+1
        
    def parse_item(self, response, index, image): 
        print(".................")  
        product_url = response.url
        print(product_url)
        item_type=index.strip()
        print(item_type)
        image_link = image
        print(image_link)
        auction_date = response.xpath('//*[@id="AuctList"]/div/div[3]/em/text()').get()
        print(auction_date)
        location = response.xpath('//*[@id="AuctList"]/div/div[2]/em/text()').get()
        print(location)
        product_name = response.css('h2.h2.mb-0::text').get().strip()
        print(product_name)
        try:
            lot_number = response.xpath('//div/div[2]/div[2]/div/text()').extract()[1]
            print(lot_number)
        except:
            lot_number = ""    
        auctioner = response.css('a.u-link-v5.g-color-white ::text').extract()[1]
        print(auctioner)
        description = response.xpath("//div/div[1]/em/text()").get()
        print(description)

        yield{
            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : auctioner,
            'website' : "weaverauctions",
            'description' : description           
        }