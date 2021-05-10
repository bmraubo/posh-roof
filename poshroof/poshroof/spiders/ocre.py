import scrapy, time
#from scrapy.crawler import CrawlerProcess #eventually want this to run as a single script
#img pipeline is holding that up


def picture_check(y, records):
    pic_frame = records[y].xpath( \
        './/div[@class="col-md-5 col-lg-4 pull-right"]/a').get()
    if pic_frame is None:
        return True
    else: 
        return False


class OcreSpider(scrapy.Spider):
    name = 'OCRE Spider'
    base_url = 'http://numismatics.org/ocre/'
    start_urls =[base_url + 'results']


    def parse(self, response):
        base_url = OcreSpider.base_url
        #Navigate to http://numismatics.org/ocre/results
        #get all the records displayed (20) into a list
        records = response.xpath('/html/body/div[2]/div[1]/div[1]/div\
            [contains(@class,"row result-doc")]')
        #iterate through list
        for y in range(0, len(records)):
            #exclude records without picture
            picture = picture_check(y, records)
            if picture is True:
                #figure out record url
                record_id = records[y].xpath('//h4/a/@href').get()
                record_url = base_url + '/' + record_id
                #parse record
                yield scrapy.Request(record_url, callback=self.parse_record)
            else:
                pass
        #sleep for a minute to prevent pressure on server
        time.sleep(60)
        #navigate to the next page
        next_page = response.xpath('//a[contains(@class, \
            "btn btn-default pagingBtn")]/@href').get()
        next_page_url = base_url + next_page
        yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_record(self, response):
        pass
        #grab info
        typological_data = response.xpath('//div[@class="metadata_section"]')
            #grab date range
        date_range = \
            typological_data.xpath('.//ul/li/text()').get().strip()
        #grab manufacture
        manufacture = \
            typological_data.xpath('.//ul/li[3]/a/text()').get().strip()
        #grab denomination
        denom = \
            typological_data.xpath('.//ul/li[4]/a/text()').get().strip()
        #grab material
        material = \
            typological_data.xpath('.//ul/li[5]/a/text()').get().strip()
        #grab authority and issuer
        authority = typological_data.xpath('.//ul/li[6]/ul/li/a/text()').get().strip()
        issuer = typological_data.xpath('.//ul/li[6]/ul/li[3]/a/text()').get().strip()
        #grab mint and region
        mint = typological_data.xpath('.//ul/li[7]/ul/li/a/text()').get()
        region = typological_data.xpath('.//ul/li[7]/ul/li[2]/a/text()').get()
        #grab obverse data
        o_legend = typological_data.xpath('.//ul/li[8]/ul/li/a/text()').get()
        o_type = typological_data.xpath('.//ul/li[8]/ul/li/text()').get()
        o_portrait = typological_data.xpath('.//ul/li[8]/ul/li/a/text()').get()
        #grab reverse data
        r_legend = typological_data.xpath('.//ul/li[9]/ul/li/span/text()').get()
        r_type = typological_data.xpath('.//ul/li[9]/ul/li/text()').get()
        diety = typological_data.xpath('.//ul/li[9]/ul/li/a/text()').get()
        #grab pictures
        thumbnail_url = response.xpath('//a[@href="#iiif-window"/@id]').get()
        yield scrapy.Request(thumbnail_url, callback=self.parse_img)
        #save data
        #the data will be contained within a csv file.
        #the links to the pictures will be included within the csv
        #so first save the images
        #then save the typological information

    def parse_img(self, response):
        images = []
        #get links to full resolution images
        full_res_links = response.xpath('//a[@title="Full resolution image"]/@href')
        #navigate to img and download
        for link in full_res_links:
            images.append(link.extract_first())
            

            




