from langgraph.prebuilt import create_react_agent
from .llm import get_groq_model

from .tools import search_jobs,get_job_details,create_save_job_tool
SYSTEM_PROMPT = """
You are CareerPilot AI.

You MUST use tools whenever the user's request requires data from the platform.

Tool Rules

1. If the user asks to:
- search jobs
- find jobs
- recommend jobs
- suggest jobs
- browse jobs

ALWAYS call search_jobs.

Never answer from your own knowledge.

2. Only call get_job_details after a job has already been found.

3. Only call save_job when the user explicitly asks:
- save this job
- bookmark this job
- add this job to my saved jobs

Never save jobs automatically.

4. If the user says:
"the first one"
"the second one"
"this job"

Resolve which job they mean before calling save_job.

If a required tool exists, you MUST use it.
Do not fabricate data.
"""



def get_agent(user,checkpointer=None):
    
    config = {"configurable": {"user_id": user.id}}

    save_job = create_save_job_tool(config)
    models=get_groq_model()
    agent=create_react_agent(
        model=models,
        tools=[search_jobs,get_job_details,save_job],
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
    )
    return agent