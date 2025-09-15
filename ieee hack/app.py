import streamlit as st
from gtts import gTTS
import PyPDF2

st.set_page_config(page_title="AI Health Companion", page_icon="🩺")
st.title("🩺 AI Health Companion for Elderly")
st.write("Upload a prescription PDF to automatically generate a daily health plan.")

# --- User Input Form ---
with st.form("health_form"):
    name = st.text_input("Name (optional)")
    age = st.number_input("Age", min_value=40, max_value=120, value=70)
    condition = st.text_input("Health Condition (e.g., Diabetes, Hypertension)")
    sleep_time = st.text_input("Sleep Time (e.g., 10:00 PM)")
    pdf_file = st.file_uploader("Upload Prescription PDF", type=["pdf"])
    submitted = st.form_submit_button("Generate Plan")

if submitted:
    # --- Extract Medications from PDF ---
    meds_list = []
    if pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        # Simple extraction: find lines with common medication patterns
        # For simplicity, assume each line with capitalized words is a medicine
        for line in text.split("\n"):
            line = line.strip()
            if line and line[0].isupper():
                meds_list.append(line)
    else:
        st.warning("No PDF uploaded. You can manually enter medications in future versions.")

    # --- Rule-based daily plan ---
    plan = "🗓️ Your Daily Health Plan:\n\n"

    if meds_list:
        plan += "💊 Medication Reminders:\n"
        for med in meds_list:
            plan += f"- Take {med} in the morning and evening.\n"
    else:
        plan += "💊 Medication Reminders:\n- No medications detected. Enter manually in future.\n"

    plan += "\n💧 Hydration:\n- Drink 6-8 glasses of water throughout the day.\n"
    plan += "\n🏃 Light Exercise:\n- 10 min walk in morning, 5 min stretching in evening.\n"

    plan += "\n🥗 Diet Tips:\n- Eat balanced meals with fruits and vegetables.\n"
    if "Diabetes" in condition or "diabetic" in condition.lower():
        plan += "- Limit sugar and high-carb foods.\n"
    if "Hypertension" in condition or "blood pressure" in condition.lower():
        plan += "- Reduce salt intake.\n"

    st.subheader("🗓️ Your Daily Health Plan")
    st.write(plan)

    # --- Convert Plan to Audio ---
    if st.button("🔊 Listen to Plan"):
        tts = gTTS(text=plan, lang="en")
        tts.save("health_plan.mp3")
        audio_file = open("health_plan.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

    # --- Download Plan as Text ---
    st.download_button("📥 Download Plan as Text", data=plan, file_name="health_plan.txt")
