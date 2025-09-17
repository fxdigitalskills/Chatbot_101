# import streamlit as st
# import google.generativeai as genai

# # Configure Gemini API
# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash')

# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

# def get_gemini_response(prompt):
#     response = model.generate_content(prompt)
#     return response.text

# def main():
#     st.title("Gemini AI Chatbot")
    
#     initialize_session_state()

#     # Display chat messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # Chat input
#     if prompt := st.chat_input("Chat with Gemini"):
#         # Display user message
#         with st.chat_message("user"):
#             st.write(prompt)
        
#         # Add user message to history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         # Get Gemini response
#         response = get_gemini_response(prompt)
        
#         # Display assistant response
#         with st.chat_message("assistant"):
#             st.write(response)
        
#         # Add assistant response to history
#         st.session_state.messages.append({"role": "assistant", "content": response})

# if __name__ == "__main__":
#     main()



import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# ---------- Helpers ----------
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []


def get_gemini_response(prompt, image_bytes=None, image_type=None):
    """
    Send text + optional image to Gemini.
    """
    parts = [{"text": prompt}]
    if image_bytes:
        parts.append({
            "inline_data": {
                "mime_type": image_type or "image/jpeg",
                "data": image_bytes,
            }
        })
    response = model.generate_content(parts)
    return response.text


# ---------- Main App ----------
def main():
    st.title("Gemini AI Chatbot with Image Memory")
    initialize_session_state()

    # ---- Display history ----
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("image"):
                st.image(
                    message["image"],
                    caption="Uploaded Image",
                    use_container_width=True,
                )

    # ---- File uploader ----
    uploaded_image = st.file_uploader(
        "Upload an image (optional)", type=["jpg", "jpeg", "png"]
    )

    # ---- Chat input ----
    if prompt := st.chat_input("Chat with Gemini"):
        image_bytes = uploaded_image.read() if uploaded_image else None
        image_type = uploaded_image.type if uploaded_image else None

        # Show user message
        with st.chat_message("user"):
            st.write(prompt)
            if image_bytes:
                st.image(
                    image_bytes,
                    caption="Uploaded Image",
                    use_container_width=True,
                )

        # Save user message to history
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "image": image_bytes}
        )

        # Get Gemini response
        response_text = get_gemini_response(prompt, image_bytes, image_type)

        # Show assistant message
        with st.chat_message("assistant"):
            st.write(response_text)

        # Save assistant message to history
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )


# ---------- Run ----------
if __name__ == "__main__":
    main()

