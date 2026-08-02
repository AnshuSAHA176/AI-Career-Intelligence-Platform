from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from.agent import get_agent
from rest_framework.response import Response
from groq import BadRequestError
import time
from langchain_core.messages import messages_to_dict,messages_from_dict
from .models import ChatSeasion,ChatMessage



def invoke_with_retry(agent, payload, max_retries=4):
    for attempt in range(max_retries + 1):
        try:
            return agent.invoke(payload)
        except BadRequestError as e:
            if "tool_use_failed" in str(e) and attempt < max_retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise



class chat_agent(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):

        message=request.data.get("message")
        
        session_id=request.data.get("session_id")

        if session_id:
            session=ChatSeasion.objects.get(user=request.user,id=session_id)
        else:
            session=ChatSeasion.objects.create(user=request.user)
        stored=session.messages.order_by("created_at")

        history_dicts=[ {
            "type":m.role,
            "data":{
                "content":m.content,
                "tool_call_id":m.tool_call_id,
                "name":m.name,
                "tool_calls":m.tool_calls

            }
        }
            for m in stored
            ]
        history=messages_from_dict(history_dicts) if history_dicts else []
        history.append(
            {
                "role": "user",
                "content": message,
            }
        )











        agent=get_agent(user=request.user)
      
       
        result=invoke_with_retry(agent,{
        "messages": history
    })
        perior_count=len(history)-1
        already_saved=stored.count()

        new_msgs=messages_to_dict(result['messages'])[already_saved:]
        for m in new_msgs:
            ChatMessage.objects.create(
                session=session,
                role=m["type"],
                content=m["data"].get("content") or "",
                tool_call_id=m["data"].get("tool_call_id"),
                name=m["data"].get("name"),
                tool_calls=m["data"].get("tool_calls"),
            )
        return Response({
            "answer": result["messages"][-1].content,
            "session_id": session.id,
        })

        

        


       
        



