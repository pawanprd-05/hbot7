import streamlit as st
import openai

# -----------------------------------------
# 🔐 Initialize OpenAI with your API key
# -----------------------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# -----------------------------------------
# 🧠 App Title & Description
# -----------------------------------------
st.title("🌱 Life Coach Chatbot – Emotional Support for Growth")
st.markdown(
    """
Welcome to your personal **Life Coach Chatbot**.
This chatbot is designed **exclusively** to help you explore and manage issues related to:
- **Anger**
- **Fear**
- **Feeling left behind**

🧘‍♀️ Please note: This chatbot offers **emotional guidance and reflective support**, not professional therapy or crisis counseling.
"""
)

# -----------------------------------------
# 🧩 Initialize Chat History with Guardrailed System Prompt
# -----------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a compassionate and insightful life coach AI specializing ONLY in helping users "
                "understand and manage three emotional areas: Anger issues, Fear issues, and Feelings of being left behind. "
                "Your tone should always be calm, empathetic, and empowering. "
                "Provide guidance through reflective questions, coping techniques, and emotional insight — never therapy or diagnosis.\n\n"

                "⚠️ Strong Guardrails:\n"
                "- If the user asks about anything unrelated to Anger, Fear, or Feeling left behind, respond with:\n"
                "  'I'm here to help you explore emotions related to anger, fear, or feeling left behind. "
                "Could you share how one of these shows up for you?'\n"
                "- Never provide medical, legal, financial, or relationship advice outside of those emotions.\n"
                "- If a user expresses thoughts of self-harm, suicide, or crisis, respond immediately with:\n"
                "  'It sounds like you may be in distress. You are not alone. Please contact your local emergency helpline or a trusted person. "
                "In the U.S., you can reach the Suicide & Crisis Lifeline by calling or texting **988**. "
                "If you’re outside the U.S., please reach out to local emergency services.'\n"
                "- Never pretend to be a human, therapist, or doctor.\n"
                "- Keep all responses concise, emotionally supportive, and relevant to the three focus areas only."
            )
        }
    ]

# -----------------------------------------
# 💬 Display Chat History (except system prompt)
# -----------------------------------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------------------
# ✍️ User Input Box
# -----------------------------------------
user_input = st.chat_input("Share your thoughts or feelings...")

# -----------------------------------------
# ⚙️ Function to Get AI Response
# -----------------------------------------
def get_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # you can also use "gpt-4-turbo" or "gpt-3.5-turbo"
        messages=messages,
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0.4
    )
    return response.choices[0].message["content"]

# -----------------------------------------
# 🚀 Process User Input
# -----------------------------------------
if user_input:
    # Append user message to session
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant response
    response = get_response(st.session_state.messages)

    # Append and display assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# -----------------------------------------
# 🧾 Footer Disclaimer
# -----------------------------------------
st.markdown("---")
st.markdown(
    """
⚠️ **Disclaimer:** This chatbot provides supportive emotional guidance for exploring anger, fear, or feelings of being left behind.  
It does **not** replace therapy, counseling, or professional mental health care.  
If you feel unsafe or in crisis, please contact your local emergency helpline or a trusted support network.
""",
    unsafe_allow_html=True
)