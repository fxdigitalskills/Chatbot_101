# import streamlit as st
# import google.generativeai as genai

# # --- Configure Gemini API ---
# GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
# genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-1.5-flash')

# # --- Session state ---
# def initialize_session_state():
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

# # --- Gemini call ---
# def get_roast(user_text, spice_level):
#     """
#     Ask Gemini to roast the user input based on the spice level.
#     """
#     prompt = f"""
#     You are RoastBot, a witty comedian.
#     Roast the following message in a fun, lighthearted way.
#     Spice level: {spice_level}/10 (1 = super mild, 10 = savage but still friendly).
#     User message: "{user_text}"
#     """
#     response = model.generate_content(prompt)
#     return response.text.strip()

# # --- App main ---
# def main():
#     st.title("🔥 RoastBot")
#     st.caption("Type anything and get roasted! Adjust the spice slider for mild → savage burns.")
    
#     initialize_session_state()

#     # Spice slider (1–10)
#     spice = st.slider("Spice level", 1, 10, 5)

#     # Display previous messages
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.write(message["content"])

#     # Chat input
#     if prompt := st.chat_input("Say something to RoastBot"):
#         # Show user message
#         with st.chat_message("user"):
#             st.write(prompt)
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         # Get roast
#         roast = get_roast(prompt, spice)

#         # Show roast
#         with st.chat_message("assistant"):
#             st.write(roast)
#         st.session_state.messages.append({"role": "assistant", "content": roast})

# if __name__ == "__main__":
#     main()


import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
from datetime import datetime

# -------------------------
# GEMINI CONFIG
# -------------------------
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------
# SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_prefs" not in st.session_state:
    st.session_state.user_prefs = {}

# -------------------------
# SIDEBAR WIDGETS (Preferences)
# -------------------------
with st.sidebar:
    st.title("Chatbot Controls")

    # Basic profile
    name = st.text_input("Your name", value=st.session_state.user_prefs.get("name", "Guest"))
    age = st.number_input("Your age", min_value=0, max_value=120, value=st.session_state.user_prefs.get("age", 25))
    bio = st.text_area("Short bio (optional)", value=st.session_state.user_prefs.get("bio", ""))

    # Preferences
    tone = st.radio("Response tone", ["Friendly", "Formal", "Funny"], index=0)
    topics = st.multiselect("Topics you care about", ["Data", "Code", "Travel", "Food", "Sports"], default=["Data"])
    single_topic = st.selectbox("Primary topic", ["Data", "Code", "Travel", "Food", "Sports"], index=0)
    verbosity = st.slider("Verbosity (words)", min_value=1, max_value=200, value=60)
    mood_level = st.select_slider("Mood level", options=["Low", "Medium", "High"], value="Medium")

    # Date/time preferences
    meet_date = st.date_input("Pick a date", value=datetime.now().date())
    meet_time = st.time_input("Pick a time", value=datetime.now().time().replace(microsecond=0))

    # File upload & color picker
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv", "png", "jpg", "jpeg"])
    theme_color = st.color_picker("Pick a theme color", value="#4CAF50")

    # Save prefs
    if st.button("Save preferences"):
        st.session_state.user_prefs.update({"name": name, "age": age, "bio": bio})
        st.success("Preferences saved!")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------------
# HEADER
# -------------------------
st.markdown(f"<h1 style='color: {theme_color};'>Gemini + Streamlit Widgets Chatbot</h1>", unsafe_allow_html=True)
st.caption("Demo app: all Streamlit widgets + Gemini-powered responses.")

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# GEMINI PROMPT BUILDER
# -------------------------
def build_prompt(user_input):
    return f"""
    User message: {user_input}
    Name: {name}, Age: {age}, Bio: {bio}
    Tone: {tone}
    Topics: {', '.join(topics) if topics else 'general'}
    Primary topic: {single_topic}
    Mood level: {mood_level}
    Verbosity target: {verbosity} words
    Meeting prefs: {meet_date} at {meet_time}
    ---
    Please generate a {tone.lower()} response that fits these preferences.
    """

# -------------------------
# USER INPUT
# -------------------------
if prompt := st.chat_input("Chat with Gemini"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build structured prompt
    gemini_prompt = build_prompt(prompt)

    # Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            response = model.generate_content(gemini_prompt)
            reply = response.text
            st.markdown(reply)

    # Save response
    st.session_state.messages.append({"role": "assistant", "content": reply})

# -------------------------
# FILE PREVIEW TAB
# -------------------------
st.subheader("📂 Uploaded File Preview")
if uploaded_file:
    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file)
    elif uploaded_file.type == "text/plain":
        string_data = uploaded_file.read().decode("utf-8")
        st.text_area("File contents", value=string_data, height=300)
    elif uploaded_file.type in ("text/csv", "application/vnd.ms-excel"):
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
    else:
        st.warning("Unsupported file type for preview.")
else:
    st.info("Upload a file in the sidebar to preview it here.")

# -------------------------
# VISUAL DEMO TAB
# -------------------------
st.subheader("📊 Simple Visuals")
df = pd.DataFrame({"x": range(10), "y": [i**1.5 for i in range(10)]})
st.dataframe(df)

fig, ax = plt.subplots()
ax.plot(df["x"], df["y"], marker="o")
ax.set_title("Sample plot")
st.pyplot(fig)

# -------------------------
# EXTRA TOOLS
# -------------------------
st.subheader("⚡ Extras")

if st.checkbox("Show session state"):
    st.json({k: v for k, v in st.session_state.items() if k in ["messages", "user_prefs"]})

if st.button("Simulate long task"):
    with st.spinner("Running task..."):
        p = st.progress(0)
        for i in range(20):
            time.sleep(0.05)
            p.progress((i+1)/20)
    st.success("Done!")

if st.button("Download conversation as CSV"):
    df_export = pd.DataFrame(st.session_state.messages)
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="chat_history.csv", mime="text/csv")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("This demo includes: chat_input, chat_message, sidebar widgets, file_uploader, dataframes, charts, session_state, progress, spinners, and Gemini AI.")
