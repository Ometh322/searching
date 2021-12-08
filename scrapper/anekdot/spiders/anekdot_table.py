import scrapy


def create_start_urls(startId):
    listUrls = []
    for pageId in range(startId, 1248793):
        newStartUrl = f'https://www.anekdot.ru/id/{pageId}/'
        listUrls.append(newStartUrl)
    return listUrls


class AnekdotTableSpider(scrapy.Spider):
    name = 'anekdot'
    allowed_domains = ['anekdot.ru']
    start_urls = create_start_urls(1048794)



    def parse(self, response):
        print("procesing:" + response.url)

        anekdot_text = response.css('.text::text').extract()
        anekdot_date = response.css('.rates::attr("data-id")').extract()
        anekdote_author = [response.xpath("//div[@class='info']/a/text()").extract_first()]

        row_data = zip(anekdot_date, anekdote_author, anekdot_text)
        for item in row_data:
            scrapped_info = {
                'page': response.url,
                'date': item[0],
                'author': item[1],
                'text': item[2]
            }
            yield scrapped_info
