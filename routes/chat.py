from fastapi import APIRouter, HTTPException
from schemas.chat_schema import ChatRequest, ChatResponse
from services.ai_service import generate_reply
from core.exceptions import OpenAIAPIError, ConfigurationError

router = APIRouter()

@router.get("/")
def root():
    return {"status": "running"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = generate_reply(request.message)
        return ChatResponse(reply=reply)
    except ConfigurationError:
        raise HTTPException(status_code=500, detail="Service configuration error")
    except OpenAIAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print("Route Error:", type(e).__name__)
        raise HTTPException(status_code=500, detail="Internal server error")
