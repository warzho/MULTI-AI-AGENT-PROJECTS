#Claude-proposed ui.py
import streamlit as st
import requests
import time

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout="centered")
st.title("Multi AI Agent using Groq and Tavily New")

# Add backend status check
API_URL = "http://127.0.0.1:9999"
CHAT_URL = f"{API_URL}/chat"


def check_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_URL}/", timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False


def test_backend_connection():
    """Test backend connection with detailed error info"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        st.success(f"✅ Backend is running! Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is the backend server running?")
        return False
    except requests.exceptions.Timeout:
        st.error("❌ Backend connection timeout")
        return False
    except Exception as e:
        st.error(f"❌ Backend connection error: {str(e)}")
        return False


# Add a backend status indicator
with st.sidebar:
    st.subheader("Backend Status")
    if st.button("Check Backend"):
        test_backend_connection()

    backend_running = check_backend_status()
    if backend_running:
        st.success("🟢 Backend Online")
    else:
        st.error("🔴 Backend Offline")

system_prompt = st.text_area("Define your AI Agent:", height=70)
selected_model = st.selectbox("Select your AI model:", settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("Allow web search")
user_query = st.text_area("Enter your query:", height=150)

if st.button("Ask Agent") and user_query.strip():
    # Check backend status first
    if not check_backend_status():
        st.error("❌ Backend is not running. Please start the backend server first.")
        st.info("Run: `python app/main.py` to start the backend")
        st.stop()

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }

    try:
        logger.info("Sending request to backend")

        # Add loading indicator
        with st.spinner("Getting response from AI agent..."):
            response = requests.post(CHAT_URL, json=payload, timeout=30)

        logger.info(f"Received response with status code: {response.status_code}")

        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")

            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)

        else:
            # Show detailed error information
            logger.error(f"Backend error: {response.status_code}")

            try:
                error_detail = response.json()
                st.error(f"❌ Backend Error ({response.status_code}): {error_detail.get('detail', 'Unknown error')}")
            except:
                st.error(f"❌ Backend Error ({response.status_code}): {response.text}")

            # Show the raw response in an expander for debugging
            with st.expander("Debug Info"):
                st.write("Status Code:", response.status_code)
                st.write("Response Headers:", dict(response.headers))
                st.write("Response Text:", response.text)

    except requests.exceptions.ConnectionError as e:
        error_msg = f"Cannot connect to backend server at {CHAT_URL}. Is the backend running?"
        logger.error(error_msg)
        st.error(f"❌ Connection Error: {error_msg}")
        st.info("💡 Try running: `python app/main.py` to start the backend")

    except requests.exceptions.Timeout as e:
        error_msg = "Request to backend timed out (30s)"
        logger.error(error_msg)
        st.error(f"❌ Timeout Error: {error_msg}")

    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ Request Error: {error_msg}")

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(f"Error occurred while sending request to backend: {error_msg}")
        st.error(f"❌ Failed to communicate with backend: {error_msg}")

        # Show detailed error info
        with st.expander("Error Details"):
            st.write("Exception type:", type(e).__name__)
            st.write("Exception message:", str(e))

# import streamlit as st
# import requests
#
# from app.config.settings import settings
# from app.common.logger import get_logger
# from app.common.custom_exception import CustomException
#
# logger = get_logger(__name__)
#
# st.set_page_config(page_title="Multi AI Agent" , layout="centered")
# st.title("Multi AI Agent using Groq and Tavily New")
#
# system_prompt = st.text_area("Define your AI Agent: " , height=70)
# selected_model = st.selectbox("Select your AI model: ", settings.ALLOWED_MODEL_NAMES)
#
# allow_web_search = st.checkbox("Allow web search")
#
# user_query = st.text_area("Enter your query : " , height=150)
#
# API_URL = "http://127.0.0.1:9999/chat"
#
# if st.button("Ask Agent") and user_query.strip():
#
#     payload = {
#         "model_name" : selected_model,
#         "system_prompt" : system_prompt,
#         "messages" : [user_query],
#         "allow_search" : allow_web_search
#     }
#
#     try:
#         logger.info("Sending request to backend")
#
#         response = requests.post(API_URL , json=payload)
#
#         if response.status_code==200:
#             agent_response = response.json().get("response","")
#             logger.info("Successfully received response from backend")
#
#             st.subheader("Agent Response")
#             st.markdown(agent_response.replace("\n","<br>"), unsafe_allow_html=True)
#
#         else:
#             logger.error("Backend error")
#             st.error("Error with backend")
#
#     except Exception as e:
#         logger.error("Error occurred while sending request to backend")
#         st.error(str(CustomException("Failed to communicate to backend")))
#
#
#
