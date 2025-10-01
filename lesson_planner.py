import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ✅ Try to load API key from .env (for local use)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ✅ If not found, try Streamlit Cloud Secrets
if not api_key and "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

if not api_key:
    st.error("❌ Gemini API Key not found. Please set it in .env (local) or Streamlit Secrets (cloud).")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    st.set_page_config(page_title="📘 Urdu Lesson Planner", layout="centered")
    st.title("📘 اردو Lesson Planner")
    st.write("یہ ایپ آپ کے دیے گئے موضوع اور کلاس کے مطابق اردو میں Lesson Plan تیار کرے گی۔")

    # User Inputs
    topic = st.text_input("سبق کا موضوع درج کریں:")
    class_level = st.text_input("کلاس درج کریں (مثلاً: کلاس 3):")

    lesson_plan = None

    if st.button("Lesson Plan تیار کریں"):
        if topic.strip() and class_level.strip():
            prompt = f"""
            آپ ایک پرائمری اسکول کے استاد ہیں۔
            آپ کو {class_level} کے لیے سبق کا موضوع دیا گیا ہے: {topic}
            براہ کرم اردو میں ایک مکمل Lesson Plan تیار کریں۔

            Lesson Plan میں یہ شامل ہوں:
            - سبق کا عنوان
            - کلاس لیول
            - سبق کے مقاصد
            - تدریسی طریقے
            - سرگرمیاں (طلبہ کے لیے)
            - سوالات و جوابات
            - ہوم ورک
            """
            response = model.generate_content(prompt)
            lesson_plan = response.text
        else:
            st.warning("براہ کرم Topic اور Class دونوں درج کریں۔")

    # Show Lesson Plan
    if lesson_plan:
        st.subheader("📖 تیار شدہ Lesson Plan")
        st.write(lesson_plan)

        st.download_button("⬇️ Lesson Plan Download کریں",
                           lesson_plan,
                           file_name="lesson_plan.txt")
