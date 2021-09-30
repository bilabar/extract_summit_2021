import scrapy


class ContestSpider(scrapy.Spider):
    name = 'contest'
    allowed_domains = ['contest-646508-5umjfyjn4a-ue.a.run.app']
    start_urls = ['https://contest-646508-5umjfyjn4a-ue.a.run.app/listing']

    def parse(self, response):
        links = response.css('div.col-md-4').css('a::attr(href)')
        item_pages = links[:-2]
        yield from response.follow_all(item_pages, self.parse_item)

        next_page = links[-1]
        yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        left = response.css('div.second-content').css('div.left-content')
        right = response.css('div.second-content').css('img::attr(src)')

        yield {
            'item_id': left.css('span#uuid::text').get(),
            'name': left.css('h2::text').get(),
            'image_id': right.get().replace('/gen/', '').replace('.jpg', '') if len(right) else None,
            'flavor': left.css('span::text')[-1].get(),
        }
