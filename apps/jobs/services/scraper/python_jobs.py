from playwright.sync_api import sync_playwright
from .base import BaseScraper
# python3 apps/jobs/services/scraper/python_jobs.py



class PythonJobsScraper(BaseScraper):

    BASE_URL = "https://www.python.org/jobs/"

    def scrape(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            self.page = browser.new_page()

            self.page.goto(
                self.BASE_URL,
                wait_until="networkidle"
            )
            try:

                jobs = self.page.locator("ol.list-recent-jobs > li")

                job_list = []

                for i in range(jobs.count()):

                    job = jobs.nth(i)

                    job_data = self.scrape_job_card(job)

                    job_list.append(job_data)
                for job in job_list:
                    description,requirement=self.scrape_detail_page(job['url'])
                    job["description"] = description
                    job["requirements"] = requirement
                    
                
                    

            except Exception as e:
                print(e)
    

            finally:

                browser.close()
                

                return job_list

    def scrape_job_card(self, job):

        job_card = job.locator(
            "h2.listing-company span.listing-company-name a"
        )

        title = job_card.text_content().strip()

        href = job_card.get_attribute("href")

        company_text = job.locator(
            ".listing-company-name"
        ).inner_text()

        lines = [
            line.strip()
            for line in company_text.splitlines()
            if line.strip()
        ]

        company = lines[-1]

        location = job.locator(
            ".listing-location"
        ).text_content().strip()

        posted_date = job.locator(
            ".listing-posted time"
        ).text_content().strip()
        
        category = job.locator(
            ".listing-company-category"
        ).text_content().strip()
        
        
        return {
            "title": title,
            "company": company,
            "location": location,
            "posted_date": posted_date,
            "category": category,
            "url": "https://www.python.org" + href,
            "source": "python.org",
        }
    def scrape_detail_page(self, url):
        
            try:
                self.page.goto(url)
                
                
                detail_page=self.page.locator(".job-description")
                paragraphs = detail_page.locator("p")

                count = min(3, paragraphs.count())

                paragraphs_text = []
                requirment=[]
                for i in range(count):
                    paragraphs_text.append(
                    paragraphs.nth(i).text_content().strip())

                description = "\n\n".join(paragraphs_text)
                requirment_ul=self.page.locator("xpath=//h2[text()='Requirements']/following-sibling::ul[1]")
                requirment_li=requirment_ul.locator('li')
                for i in range(requirment_li.count()):
                    requirment.append(
                         requirment_li.nth(i).text_content().strip()
                         )
                
                filtered = []

                for item in requirment:
                    if item.startswith("Contact:"):
                            continue
                    if item.startswith("E-mail"):
                        continue
                    if item.startswith("Web:"):
                        continue

                    filtered.append(item)
                return description,filtered 
            except Exception as e:
                print(f"failing url is {url}\nsomthing wrong")

               
