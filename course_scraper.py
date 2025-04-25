import scrapy
from scrapy.crawler import CrawlerProcess


class NmtCoursesSpider(scrapy.Spider):
    name = "nmt_courses"
    allowed_domains = ["banweb7.nmt.edu"]
    start_urls = ["https://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"]

    def parse(self, response):
        terms = response.css('select[name="p_term"] option::attr(value)').getall()
        subjects = response.css('select[name="p_subj"] option::attr(value)').getall()

        for term in terms:
            for subject in subjects:
                # self.logger.info(f"Submitting form with term={term}, subject={subject}")
                yield scrapy.FormRequest(
                    url="https://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff",
                    formdata={"p_term": term, "p_subj": subject},
                    callback=self.parse_courses,
                    meta={"term": term, "subject": subject}
                )

    def parse_courses(self, response):
        rows = response.css("table[border] tr")
        for row in rows:
            cells = row.css("td")
            if len(cells) < 17:
                continue

            yield {
                "term": response.meta["term"],
                "subject": response.meta["subject"],
                "crn": cells[0].css("::text").get(),
                "course_code": cells[1].css("::text").get(),
                "campus": cells[2].css("::text").get(),
                "days": cells[3].css("::text").get(),
                "date_range": cells[4].css("::text").get(),
                "time": cells[5].css("::text").get(),
                "location": cells[6].css("::text").get(),
                "credit_hours": cells[7].css("::text").get(),
                "type": cells[8].css("::text").get(),
                "title": cells[9].css("::text").get(),
                "instructor": cells[10].css("::text").get(),
                "seats": cells[11].css("::text").get(),
                "limit": cells[12].css("::text").get(),
                "enrolled": cells[13].css("::text").get(),
                "waitlist": cells[14].css("::text").get(),
                "fees": cells[15].css("::text").get(),
                "bookstore_link": cells[16].css("a::attr(href)").get()
            }


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "nmt_courses.csv": {"format": "csv", "overwrite": True}
        },
        "LOG_LEVEL": "INFO"
    })
    process.crawl(NmtCoursesSpider)
    process.start()