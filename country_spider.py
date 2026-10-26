import scrapy

class CountrySpider(scrapy.Spider):
    name = "countries"
    start_urls = ["https://www.scrapethissite.com/pages/simple/"]

    def parse(self, response):
        for country in response.css("div.country"):
            # Fix: Extract ALL text nodes inside the h3 element (including after child tags)
            raw_name_list = country.css("h3.country-name ::text").getall()
            full_name = "".join(raw_name_list).strip()

            yield {
                "country_name": full_name,
                "capital": country.css("span.country-capital::text").get(),
                "population": country.css("span.country-population::text").get(),
                "area_sq_km": country.css("span.country-area::text").get()
            }
