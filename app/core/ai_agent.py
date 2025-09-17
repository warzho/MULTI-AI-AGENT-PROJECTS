# app/core/ai_agent.py
import os
from dotenv import load_dotenv
from app.common.logger import get_logger

logger = get_logger(__name__)
load_dotenv()


def get_response_from_ai_agents(model_name, messages, allow_search, system_prompt):
    try:
        logger.info(f"Processing request for model: {model_name}")  # ← model_name should be available here

        # Check API keys
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        if allow_search:
            tavily_api_key = os.getenv("TAVILY_API_KEY")
            if not tavily_api_key:
                logger.warning("TAVILY_API_KEY not set, disabling search")
                allow_search = False

        # Make sure all variables are properly referenced
        message_text = messages[0] if messages and len(messages) > 0 else "No message provided"

        # Create response using the passed parameters
        response = f"""AI Response from {model_name}:

Query: {message_text}
Web Search: {allow_search}
System Prompt: {system_prompt[:100] if system_prompt else 'None'}...

This is a test response to verify the backend is working.
"""

        logger.info(f"Successfully generated response for model: {model_name}")
        return response

    except Exception as e:
        logger.error(f"Error in get_response_from_ai_agents: {str(e)}")
        logger.error(f"Function called with: model_name={model_name}, messages={messages}, allow_search={allow_search}")
        raise e  # Re-raise the original exception

# from langchain_groq import ChatGroq
# # from langchain_community.tools.tavily_search import TavilySearchResults
# # from langchain_tavily import TavilySearchAPIWrapper
# # # Use the correct import
# # from langchain_tavily import TavilySearchResults
#
# # Use the correct import
# try:
#     from langchain_tavily import TavilySearchResults
#     TAVILY_AVAILABLE = True
# except ImportError:
#     try:
#         from langchain_community.tools.tavily_search import TavilySearchResults
#         TAVILY_AVAILABLE = True
#     except ImportError:
#         TAVILY_AVAILABLE = False
#         TavilySearchResults = None
#
# from app.common.logger import get_logger
# logger = get_logger(__name__)
#
# from dotenv import load_dotenv
# import os
# load_dotenv()
#
# from langgraph.prebuilt import create_react_agent
# from langchain_core.messages.ai import AIMessage
#
# from app.config.settings import settings
#
# def get_response_from_ai_agents(llm_id , query , allow_search ,system_prompt):
#     #Adding enhanced logging
#     try:
#         logger.info(f"Initializing AI agent with model: {model_name}")
#         logger.info(f"Search enabled: {allow_search}")
#
#         # Check API keys
#         groq_api_key = os.getenv("GROQ_API_KEY")
#         if not groq_api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")
#
#         if allow_search:
#             tavily_api_key = os.getenv("TAVILY_API_KEY")
#             if not tavily_api_key:
#                 raise ValueError("TAVILY_API_KEY environment variable is not set")
#
#
#         llm = ChatGroq(model=llm_id)
#
#         # Replace the old import
#         # from langchain_community.tools.tavily_search import TavilySearchResults
#
#         # Updated tools line
#         tools = [TavilySearchAPIWrapper(max_results=2)] if allow_search else []
#
#         # tools = [TavilySearchResults(max_results=2)] if allow_search else []
#
#         agent = create_react_agent(
#             model=llm,
#             tools=tools,
#             state_modifier=system_prompt
#         )
#
#         state = {"messages" : query}
#
#         response = agent.invoke(state)
#
#         messages = response.get("messages")
#
#         ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]
#
#         return ai_messages[-1]
#
#     #Exception block
#     except Exception as e:
#             logger.error(f"Error in get_response_from_ai_agents: {type(e).__name__}: {str(e)}")
#             raise e
#
#
#
#
#
#
#
#

# app/core/ai_agent.py - Debug version
# import os
# from dotenv import load_dotenv
# from app.common.logger import get_logger
#
# logger = get_logger(__name__)
# load_dotenv()
#
#
# def get_response_from_ai_agents(model_name, messages, allow_search, system_prompt):
#     try:
#         # Debug: Print all received parameters
#         logger.info("=== DEBUG: Function called with parameters ===")
#         logger.info(f"model_name type: {type(model_name)}, value: {model_name}")
#         logger.info(f"messages type: {type(messages)}, value: {messages}")
#         logger.info(f"allow_search type: {type(allow_search)}, value: {allow_search}")
#         logger.info(f"system_prompt type: {type(system_prompt)}, value: {system_prompt}")
#         logger.info("=== END DEBUG ===")
#
#         # Validate parameters
#         if not model_name:
#             raise ValueError("model_name parameter is None or empty")
#
#         if not isinstance(messages, list):
#             raise ValueError(f"messages should be a list, got {type(messages)}")
#
#         # Check API keys
#         groq_api_key = os.getenv("GROQ_API_KEY")
#         if not groq_api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")
#
#         # Safe message extraction
#         message_text = "No message provided"
#         if messages and len(messages) > 0 and messages[0]:
#             message_text = str(messages[0])
#
#         # Create response
#         response = f"""Debug Response:
# Model: {model_name}
# Message: {message_text}
# Search: {allow_search}
# System: {system_prompt[:50] if system_prompt else 'None'}
# API Key Set: {'Yes' if groq_api_key else 'No'}
# """
#
#         logger.info(f"Successfully created response for model: {model_name}")
#         return response
#
#     except Exception as e:
#         logger.error(f"Error in get_response_from_ai_agents: {type(e).__name__}: {str(e)}")
#         logger.error(f"Locals: {locals()}")
#         raise e

