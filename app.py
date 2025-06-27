import streamlit as st
import os
os.system("python -m spacy download en_core_web_sm")

from utils.resume_parser import extract_text_from_pdf
from utils.skill_matcher import load_skill_list, match_skills, calculate_score
from utils.ner_extractor import extract_entities


def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
    st.title("📄 AI Resume Analyzer")
    st.write("Upload your resume and compare it with job skills and job description using AI.")

    uploaded_file = st.file_uploader("📤 Upload Resume (PDF only)", type=["pdf"])

    if uploaded_file:
        with st.spinner("📄 Reading and analyzing resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            skill_list = load_skill_list()

            matched_skills, missing_skills = match_skills(resume_text, skill_list)
            ats_score = calculate_score(matched_skills, len(skill_list))

            st.subheader("✅ ATS Match Score")
            st.progress(ats_score / 100)
            st.success(f"🎯 Your Resume Score: {ats_score}% match with target skills")

            st.subheader("🧠 Skills Found in Resume")
            if matched_skills:
                st.info(", ".join(sorted(matched_skills)))
            else:
                st.warning("No key skills found in your resume!")

            st.subheader("❌ Missing Important Skills")
            if missing_skills:
                st.error(", ".join(sorted(missing_skills)))
            else:
                st.success("Your resume covers all important skills!")

            st.subheader("🔍 Resume Key Information (NER)")
            entities = extract_entities(resume_text)
            st.markdown(f"**👤 Names:** {', '.join(set(entities['PERSON'])) or 'Not found'}")
            st.markdown(f"**🏢 Organizations:** {', '.join(set(entities['ORG'])) or 'Not found'}")
            st.markdown(f"**🌍 Locations:** {', '.join(set(entities['GPE'])) or 'Not found'}")
            st.markdown(f"**📅 Dates:** {', '.join(set(entities['DATE'])) or 'Not found'}")

            st.subheader("📌 Optional: Paste a Job Description")
            jd_input = st.text_area("Paste job description here...")

            if jd_input:
                jd_text = jd_input.lower()
                jd_keywords = [word for word in jd_text.split() if word in skill_list]
                jd_matched, jd_missing = match_skills(resume_text, jd_keywords)
                jd_score = calculate_score(jd_matched, len(jd_keywords))

                st.subheader("📊 JD Match Score")
                st.progress(jd_score / 100)
                st.success(f"🔍 Job-Relevance Score: {jd_score}%")

                st.subheader("✅ Matched JD Keywords")
                st.info(", ".join(jd_matched) if jd_matched else "None")

                st.subheader("❌ Missing JD Keywords")
                st.error(", ".join(jd_missing) if jd_missing else "None")

            st.caption("📝 Tip: Improve your resume by adding missing keywords relevant to your target job.")


if __name__ == "__main__":
    main()
