import streamlit as st
import google.generativeai as genai

# --- Configure Gemini API ---
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Session state ---
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

# --- Gemini call ---
def get_roast(user_text, spice_level):
    """
    Ask Gemini to roast the user input based on the spice level.
    """
    prompt = f"""
    You are RoastBot, a witty comedian.
    Roast the following message in a fun, lighthearted way.
    Spice level: {spice_level}/10 (1 = super mild, 10 = savage but still friendly).
    User message: "{user_text}"
    """
    response = model.generate_content(prompt)
    return response.text.strip()

# --- App main ---
def main():
    st.title("🔥 RoastBot")
    st.caption("Type anything and get roasted! Adjust the spice slider for mild → savage burns.")
    
    initialize_session_state()

    # Spice slider (1–10)
    spice = st.slider("Spice level", 1, 10, 5)

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Say something to RoastBot"):
        # Show user message
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get roast
        roast = get_roast(prompt, spice)

        # Show roast
        with st.chat_message("assistant"):
            st.write(roast)
        st.session_state.messages.append({"role": "assistant", "content": roast})

if __name__ == "__main__":
    main()
