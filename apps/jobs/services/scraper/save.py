from apps.jobs.models import Job
from .python_jobs import PythonJobsScraper
from datetime import datetime
from ..cetagory_base import ai_job_analyzer

def save_jobs():
    scraper=PythonJobsScraper()
    jobs=scraper.scrape()
    


    for index,job in enumerate(jobs) :
        print("analyze")
        analyze_job_data=ai_job_analyzer(job_data=job)
        print("analyze done")
        posted_date = datetime.strptime(
            job["posted_date"],
            "%d %B %Y"
        ).date()
        Job.objects.update_or_create(
        url=job["url"],
        defaults={
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "description": job["description"],
            "required_skills": job["requirements"],
            "category": job["category"],
            "posted_date": posted_date,
            "source": job["source"],

            "primary_role":analyze_job_data["primary_role"],
            "secondary_roles":analyze_job_data["secondary_roles"],
            "seniority":analyze_job_data["seniority"],
            "work_type":analyze_job_data["work_type"],
            "employment_type":analyze_job_data["employment_type"],
            "technologies":analyze_job_data["technologies"],
            "minimum_experience": analyze_job_data["experience"]["minimum_years"],
            "maximum_experience": analyze_job_data["experience"]["maximum_years"],
            
            "ai_summary":analyze_job_data["summary"],
        }
    )
        print(f"job {index} saved..")
        