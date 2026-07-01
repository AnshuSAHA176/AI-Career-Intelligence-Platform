from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://www.python.org/jobs/",
              wait_until='networkidle')
    try:
        jobs=page.locator('ol.list-recent-jobs > li')
        print(jobs.count())
        job_list=[]
        for i in range(jobs.count()):
            
            job=jobs.nth(i)
            job_card=job.locator("h2.listing-company span.listing-company-name a")
            title=job_card.text_content()
            link=job_card.get_attribute('href')
            company_text=job.locator('.listing-company-name').inner_text().strip()
            company=[line.strip() for line in company_text.splitlines() if line.strip()][-1]
            location=job.locator('.listing-location').text_content()
            posted_date=job.locator('.listing-posted time').text_content()
            category=job.locator(".listing-company-category ").text_content()
            job_list.append(
                {
                    "Title":title,
                   " Company":company,
                   " Location":location,
                    "Posted Date":posted_date,
                    "Category":category,
                    "Link":"https://www.python.org"+link,
                }
            )
        print(job_list)



        
        
    finally:
        browser.close()