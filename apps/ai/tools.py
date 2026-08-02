from langchain_core.tools import tool
from apps.jobs.models import Job,SaveJobs,ApplicationStatusHistory
from django.shortcuts import get_object_or_404
from langchain_core.runnables import RunnableConfig



import json
@tool
def search_jobs(role: str) -> list[dict]:

    """
    Search the platform's job database.

    Use this tool whenever the user asks to:

    - search jobs
    - find jobs
    - recommend jobs
    - suggest jobs
    - browse jobs

    Never answer from memory.
    """


    
    cleaned = role.lower().replace("jobs", "").replace("job", "").strip()

    jobs = Job.objects.filter(primary_role__icontains=cleaned)[:10]

    if not jobs.exists():
        return [{"message": f"No jobs found matching '{role}'. Try a broader or different search term."}]

    return [
        {"job_id": j.id, "title": j.title, "company": j.company, "location": j.location}
        for j in jobs
    ]

@tool
def get_job_details(job_id: int)->str:
   """
    Retrieve detailed information for a specific job.

    Args:
        job_id: Unique job identifier.
    """
   
   job=get_object_or_404(Job,
                         id=job_id
                         )
   
       
   return json.dumps({
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "primary_role": job.primary_role,
        "seniority": job.seniority,
        "work_type": job.work_type,
        "employment_type": job.employment_type,
        "minimum_experience": job.minimum_experience,
        "maximum_experience": job.maximum_experience,
        "required_skills": job.required_skills,
        "technologies": job.technologies,
        "description": job.description,
        "ai_summary": job.ai_summary,
        "posted_date": job.posted_date.isoformat() if job.posted_date else None,
        "source": job.source,
        "url": job.url,
    }, indent=2)
       
       


def create_save_job_tool(config:RunnableConfig):
    configurable=config.get("configurable") or config.get('metadata')
    user_id=configurable.get("user_id")
    @tool
    def save_job(job_id: int) -> dict:
        """
        Save a job for the current user.

        Use ONLY if the user explicitly asks
        to save or bookmark a job.
        """
        save_job_obj, created = SaveJobs.objects.get_or_create(
            user_id=user_id,
            job_id=job_id,
            defaults={"status":SaveJobs.Status.SAVED},
        )
        if created:
            ApplicationStatusHistory(
                save_job=save_job_obj,
                user_id=user_id,
            )
            message = "Job saved successfully."

        else:
            message = f"This job is already saved (status: {save_job_obj.status})."

        


        return json.dumps({
            "message": message,
            "title": save_job_obj.job.title,
            "company": save_job_obj.job.company,
        })

       
    return save_job
