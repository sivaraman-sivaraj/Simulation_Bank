import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import base64  
#################################################################
################# Background image selection ####################
#################################################################
### Function to convert local image to base64 string
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

### Provide your local image path (e.g., Indian flag)
local_image_path = "ZF_01.jpg"  # or "flag.png"

### Get base64 string
base64_img = get_base64_image(local_image_path)

### Inject custom CSS with base64-encoded image

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: white !important;
    }}

    h1 {{
        color: white !important;
        text-shadow: 2px 2px 4px black !important;
    }}

    html, body, [class*="css"], .stChatMessage, .stMarkdown {{
        color: white !important;
        text-shadow: 1px 1px 3px black !important;
    }}

    input, textarea {{
        color: white !important;
        background-color: rgba(0, 0, 0, 0.4) !important;
    }}

    .stChatMessage {{
        background-color: rgba(0, 0, 0, 0.4) !important;
        padding: 8px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
#################################################################
################################################################# 
### Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧮 ZF Maintenance Chatbot 🧮")  
#################################################################
################################################################# 
## Show previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## Get user input
user_prompt = st.chat_input("Ask me anything or type 'quit' to exit")

if user_prompt:
    ## If user types 'quit' or 'exit', shut down the app
    if user_prompt.strip().lower() in ["quit", "exit"]:
        st.stop()  # Stops execution gracefully (Streamlit will freeze)
        # Alternatively, use os._exit(0) or sys.exit() for hard exit (not recommended for Streamlit)
    
    ## Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    ## Dummy response logic (replace this with your real model call)
    response = f"Echo: {user_prompt}"

    ## Append bot response
    st.session_state.chat_history.append({"role": "assistant", "content": response})

    ## Display latest response
    with st.chat_message("assistant"):
        st.markdown(response)




