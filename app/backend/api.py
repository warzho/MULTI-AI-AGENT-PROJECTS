from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
import traceback
import time
import os


logger = get_logger(__name__)

app = FastAPI(title="MULTI AI AGENT")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search: bool

#Improved logging
import traceback
import time

#Additional health check
@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Backend is running"}

@app.get("/health")
def detailed_health():
    import os
    return {
        "status": "healthy",
        "groq_key_set": bool(os.getenv("GROQ_API_KEY")),
        "tavily_key_set": bool(os.getenv("TAVILY_API_KEY")),
        "allowed_models": settings.ALLOWED_MODEL_NAMES
    }

@app.post("/chat")
def chat_endpoint(request: RequestState):
    start_time = time.time()
    request_id = str(time.time())  # Simple request ID for tracking

    logger.info(f"[{request_id}] Received request for model: {request.model_name}")
    logger.info(
        f"[{request_id}] Request details - Messages count: {len(request.messages)}, Allow search: {request.allow_search}, System prompt length: {len(request.system_prompt) if request.system_prompt else 0}")

    # Log environment variables status
    groq_key_status = "SET" if os.getenv("GROQ_API_KEY") else "MISSING"
    tavily_key_status = "SET" if os.getenv("TAVILY_API_KEY") else "MISSING"
    logger.info(f"[{request_id}] Environment - GROQ_API_KEY: {groq_key_status}, TAVILY_API_KEY: {tavily_key_status}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(
            f"[{request_id}] Invalid model name: {request.model_name}. Allowed models: {settings.ALLOWED_MODEL_NAMES}")
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        logger.info(f"[{request_id}] Calling get_response_from_ai_agents...")

        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        execution_time = time.time() - start_time
        logger.info(
            f"[{request_id}] Successfully got response from AI Agent {request.model_name} in {execution_time:.2f}s")
        logger.info(f"[{request_id}] Response length: {len(response) if response else 0} characters")

        return {"response": response}

    except Exception as e:
        execution_time = time.time() - start_time

        # Log the specific exception type and message
        logger.error(f"[{request_id}] Exception type: {type(e).__name__}")
        logger.error(f"[{request_id}] Exception message: {str(e)}")

        # Log the full traceback
        logger.error(f"[{request_id}] Full traceback:\n{traceback.format_exc()}")

        # Log request details again for context
        logger.error(
            f"[{request_id}] Failed request details - Model: {request.model_name}, Messages: {request.messages}, Allow search: {request.allow_search}")

        # Log execution time even for failures
        logger.error(f"[{request_id}] Request failed after {execution_time:.2f}s")

        # Check for specific common errors
        if "API key" in str(e).lower():
            logger.error(f"[{request_id}] API key related error detected")
        elif "rate limit" in str(e).lower():
            logger.error(f"[{request_id}] Rate limit error detected")
        elif "connection" in str(e).lower():
            logger.error(f"[{request_id}] Connection error detected")

        raise HTTPException(
            status_code=500,
            detail=f"Failed to get AI response: {str(e)}"
        )

# @app.post("/chat")
# def chat_endpoint(request:RequestState):
#     logger.info(f"Received request for model : {request.model_name}")
#
#     if request.model_name not in settings.ALLOWED_MODEL_NAMES:
#         logger.warning("Invalid model name")
#         raise HTTPException(status_code=400 , detail="Invalid model name")
#
#     try:
#         response = get_response_from_ai_agents(
#             request.model_name,
#             request.messages,
#             request.allow_search,
#             request.system_prompt
#         )
#
#         logger.info(f"Successfully got response from AI Agent {request.model_name}")
#
#         return {"response" : response}
#
#     except Exception as e:
#         logger.error("Some error occurred during response generation")
#         raise HTTPException(
#             status_code=500 ,
#             detail=str(CustomException("Failed to get AI response" , error_detail=e))
#             )
    



