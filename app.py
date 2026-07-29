
import streamlit as st

from utils.resume_parser import parse_resume
from utils.jd_parser import parse_job_description
from utils.rank_candidates import rank_candidates
from utils.skill_extractor import compare_skills
from utils.ai_feedback import generate_feedback

from utils.improvement_generator import generate_improvements
from utils.recruiter_ai import recruiter_analysis
import json
from utils.llm import client
from utils.json_parser import parse_llm_json
import json
from utils.llm import client
from utils.hiring_decision import generate_hiring_decision
from utils.json_parser import parse_llm_json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from utils.llm_scoring import llm_resume_score
from utils.optimized_ats import calculate_optimized_score
from utils.resume_validator import validate_resume
from utils.pdf_export import export_resume_pdf
from utils.resume_export import export_resume_docx
from utils.resume_optimizer import optimize_resume
from utils.resume_report_generator import generate_resume_report
from utils.resume_rewriter import rewrite_resume
from utils.latex_generator import generate_latex_resume
from utils.latex_export import save_latex_file
from utils.latex_export import compile_latex_to_pdf
from utils.advanced_ats_engine import calculate_advanced_ats
from utils.recruiter_decision import recruiter_decision


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "rankings" not in st.session_state:
    st.session_state.rankings = None

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

if "resume_data" not in st.session_state:
    st.session_state.resume_data = []


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:42px;
    font-weight:800;
    color:#4F8BF9;
}

.subtitle{
    font-size:18px;
    color:#8A8A8A;
}

.upload-box{
    border:1px solid #444;
    border-radius:12px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    "<div class='main-title'>🤖 AI Resume Screener</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>LLM-powered Resume Ranking • Semantic Search • ATS Analysis • Recruiter Dashboard</div>",
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Upload Section
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📄 Job Description")

    job_description = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx", "txt"]
    )

with right:

    st.subheader("👨‍💼 Candidate Resumes")

    candidate_resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

st.divider()

analyze = st.button(
    "🚀 Analyze Candidates",
    use_container_width=True
   
)
# --------------------------------------------------
# Analysis
# --------------------------------------------------
if analyze:

    if job_description is None:
        st.warning("⚠️ Please upload a Job Description.")
        st.stop()

    if not candidate_resumes:
        st.warning("⚠️ Please upload at least one Resume.")
        st.stop()

    with st.spinner("Parsing Job Description..."):
        jd_text = parse_job_description(job_description)

    resume_data = []
    with st.spinner("Parsing Candidate Resumes..."):

        for resume in candidate_resumes:

            resume_text = parse_resume(resume)

            resume_data.append({
                "name": resume.name,
                "text": resume_text
            })

    rankings = rank_candidates(
        jd_text,
        resume_data
    )

    st.session_state.analysis_done = True
    st.session_state.rankings = rankings
    st.session_state.jd_text = jd_text
    st.session_state.resume_data = resume_data

# --------------------------------------------------
# Restore Analysis from Session State
# --------------------------------------------------

if st.session_state.analysis_done:

    rankings = st.session_state.rankings
    jd_text = st.session_state.jd_text
    resume_data = st.session_state.resume_data

    st.success("✅ Resume Analysis Completed")

    st.divider()

    # --------------------------------------------------
    # Recruiter Dashboard
    # --------------------------------------------------

    st.header("📊 Recruiter Dashboard")

    total_candidates = len(rankings)

    scores = []

    for candidate in rankings:

        ats = calculate_advanced_ats(
            candidate["text"],
            jd_text
        )

        professional_score = ats["final_score"]

        scores.append(professional_score)

    highest_score = max(scores)

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍💼 Candidates",
            total_candidates
        )

    with col2:
        st.metric(
            "🏆 Highest Match",
            f"{highest_score:.2f}%"
        )

    with col3:
        st.metric(
            "📈 Average Match",
            f"{average_score:.2f}%"
        )

    st.divider()

    st.header("🏆 Candidate Leaderboard")

    for index, candidate in enumerate(rankings, start=1):

        score = float(round(candidate["score"], 2))

        ats = calculate_advanced_ats(
            candidate["text"],
            jd_text
        )

        rule_score = ats["final_score"]

        keyword_score = ats["keyword_score"]

        skill_score = ats["skill_score"]

        resume_score = ats["section_score"]

        format_score = ats["format_score"]

        action_score = ats["action_score"]

        impact_score = ats["impact_score"]

        llm_score = ats["llm_score"]

        section_scores = ats["section_scores"]

        missing_keywords = ats["missing_keywords"]

        formatting_feedback = ats["formatting_feedback"]

        experience_score = ats["experience_score"]

        education_score = section_scores["Education"]

        project_score = section_scores["Projects"]

        final_score = ats["final_score"]
        
        if final_score >= 90 and experience_score >= 70:
            grade = "A+"
            decision = "Hire"

        elif final_score >= 80:
            grade = "A"
            decision = "Hire"

        elif final_score >= 70:
            grade = "B"
            decision = "Strong Consider"

        elif final_score >= 60:
            grade = "C"
            decision = "Consider"

        else:
            grade = "D"
            decision = "Reject"

        if index == 1:
            medal = "🥇"

        elif index == 2:
            medal = "🥈"

        elif index == 3:
            medal = "🥉"

        else:
            medal = "🏅"

        if final_score >= 85:
            badge = "🟢 Excellent Match"
        elif final_score >= 70:
            badge = "🟡 Strong Match"
        elif final_score >= 50:
            badge = "🟠 Moderate Match"
        else:
            badge = "🔴 Weak Match"

        with st.container(border=True):

            left, right = st.columns([4, 1])

            with left:

                st.subheader(f"{medal} {candidate['name']}")

                st.progress(float(final_score) / 100)

                st.markdown(
                  f"### 🎯 ATS Match Score: **{final_score:.2f}%**"
)
                st.markdown(f"**Status:** {badge}")

            with right:

                st.metric("Rank", index)

                st.metric("Score", f"{final_score:.2f}%")

            st.divider()
            recruiter = recruiter_analysis(
                candidate["text"],
                jd_text,
                final_score,
                grade,
                decision
            )
           
            # --------------------------------------------
# Professional Final ATS Score
# --------------------------------------------

            # --------------------------------------------
            # Recruiter Recommendation
            # --------------------------------------------

            colA, colB = st.columns(2)

            with colA:

                st.markdown("### 💼 Recruiter Recommendation")
                st.info(recruiter["recommendation"])

                

            with colB:

                st.markdown("### ⭐ ATS Grade")
                grade = recruiter["grade"]
                st.metric(
                    "Grade",
                    recruiter["grade"]
                )   
                
            st.divider()

            # --------------------------------------------
            # Resume Evaluation
            # --------------------------------------------

            col_left, col_right = st.columns(2)

            with col_left:

                for item in recruiter["strengths"]:
                  st.success(item)

            

            with col_right:

                for item in recruiter["weaknesses"]:
                  st.warning(item)

                

            st.divider()

            # --------------------------------------------
            # AI Recruiter Notes
            # --------------------------------------------

            st.markdown("### 🤖 AI Recruiter Notes")

            st.info(recruiter["notes"])
            st.divider()

            # --------------------------------------------
            # Skill Match Dashboard
            # --------------------------------------------

            # --------------------------------------------
            # Skill Match Analysis
            # --------------------------------------------

            st.subheader("🧠 Skill Match Analysis")

            skills = compare_skills(
                candidate["text"],
                jd_text
            )
           

            matched_skills = skills["matched"]
            missing_skills = skills["missing"]
            resume_skill_count = len(skills["resume_skills"])
            jd_skill_count = len(skills["jd_skills"])
            matched_count = len(matched_skills)
            missing_count = len(missing_skills)

            coverage = 0

            if jd_skill_count > 0:
                coverage = round((matched_count / jd_skill_count) * 100, 1)

            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.metric("Resume Skills", resume_skill_count)

            with c2:
                st.metric("JD Skills", jd_skill_count)

            with c3:
                st.metric("Matched", matched_count)

            with c4:
                st.metric("Missing", missing_count)

            with c5:
                st.metric("Coverage", f"{coverage}%")
            
            chart = pd.DataFrame({
            "Category": ["Matched", "Missing"],
            "Count": [matched_count, missing_count]
        })

            fig = px.pie(
                chart,
                values="Count",
                names="Category",
                hole=0.45,
                title="Skill Match Distribution"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📈 Skill Coverage")

            st.progress(coverage / 100)

            st.write(f"Overall Skill Coverage : **{coverage}%**")

            st.divider()

            st.subheader("🎯 Skill Domain Analysis")

            categories = [
                "Programming",
                "Web",
                "Database",
                "Cloud",
                "AI/ML",
                "DevOps"
            ]

            resume = skills["resume_skills"]

            programming = len([
                s for s in resume
                if s in [
                    "Python",
                    "Java",
                    "C",
                    "C++",
                    "Go",
                    "Rust"
                ]
            ])

            web = len([
                s for s in resume
                if s in [
                    "HTML",
                    "CSS",
                    "React",
                    "Angular",
                    "Vue",
                    "Next.js",
                    "Node.js",
                    "Express"
                ]
            ])

            database = len([
                s for s in resume
                if s in [
                    "SQL",
                    "MySQL",
                    "PostgreSQL",
                    "MongoDB",
                    "SQLite"
                ]
            ])

            cloud = len([
                s for s in resume
                if s in [
                    "AWS",
                    "Azure",
                    "GCP",
                    "Firebase"
                ]
            ])

            ai = len([
                s for s in resume
                if s in [
                    "Machine Learning",
                    "Deep Learning",
                    "TensorFlow",
                    "PyTorch",
                    "OpenCV",
                    "NLP"
                ]
            ])

            devops = len([
                s for s in resume
                if s in [
                    "Docker",
                    "Kubernetes",
                    "Git",
                    "GitHub",
                    "Jenkins"
                ]
            ])

            values = [
                programming,
                web,
                database,
                cloud,
                ai,
                devops
            ]   

            fig = go.Figure()

            fig.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill="toself",
                    name="Candidate"
                )
            )

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True
                    )
                ),
                showlegend=False,
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )           

            left, right = st.columns(2)

            with left:

                st.markdown("### ✅ Matched Skills")

                if matched_skills:

                    for skill in matched_skills:
                        st.success(skill)

                else:

                    st.info("No matched skills found.")

            with right:

                st.markdown("### ❌ Missing Skills")

                if missing_skills:

                    for skill in missing_skills:
                        st.error(skill)

                else:

                    st.success("No missing skills.")

            st.divider()
            feedback = generate_feedback(
                candidate["text"],
                jd_text,
                matched_skills,
                missing_skills
            )
            

            st.subheader("🤖 AI Resume Feedback")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### 💪 Strengths")
                for item in feedback["strengths"]:
                    st.success(item)

            with col2:
                st.markdown("### ⚠️ Weaknesses")
                for item in feedback["weaknesses"]:
                    st.warning(item)

            with col3:
                st.markdown("### 💡 Recommendations")
                for item in feedback["recommendations"]:
                    st.info(item)

            st.divider()
            # --------------------------------------------
            # Candidate Comparison Summary
            # --------------------------------------------

            st.subheader("📋 Candidate Summary")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Overall Match",
                    f"{final_score:.2f}%"
                )

            with col2:
                st.metric(
                    "ATS Grade",
                    recruiter["grade"]
                )

            with col3:
                st.metric(
                    "Hiring Decision",
                    recruiter["decision"]
                )

            st.divider()
            # --------------------------------------------
            # AI Suggestions
            # --------------------------------------------

            st.subheader("💡 AI Suggestions")

            improvements = generate_improvements(
            candidate["text"],
            jd_text
        )

            for tip in improvements["improvements"]:
                st.info(f"• {tip}")

            st.divider()
           # --------------------------------------------
            # Professional ATS Dashboard
            # --------------------------------------------

            st.subheader("📊 Professional ATS Dashboard")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Technical Skills",
                    f"{skill_score:.2f}%"
                )

                st.progress(skill_score / 100)

                st.metric(
                    "Keyword Match",
                    f"{keyword_score:.2f}%"
                )

                st.progress(keyword_score / 100)

                st.metric(
                    "Experience Match",
                    f"{experience_score:.2f}%"
                )

                st.progress(experience_score / 100)

                st.metric(
                    "Project Relevance",
                    f"{project_score:.2f}%"
                )

                st.progress(project_score / 100)

            with col2:

                st.metric(
                    "Resume Quality",
                    f"{resume_score:.2f}%"
                )

                st.progress(resume_score / 100)

                st.metric(
                    "Education Match",
                    f"{education_score:.2f}%"
                )

                st.progress(education_score / 100)

                st.metric(
                    "Formatting",
                    f"{format_score:.2f}%"
                )

                st.progress(format_score / 100)

                st.metric(
                    "Action Verbs",
                    f"{action_score:.2f}%"
                )

                st.progress(action_score / 100)

            st.divider()

            st.metric(
                "Overall ATS Score",
                f"{final_score:.2f}%"
            )

            st.progress(final_score / 100)

            st.divider()

            st.subheader("❌ Missing Job Description Keywords")

            if missing_keywords:

                for keyword in missing_keywords:

                    st.warning(keyword)

            else:

                st.success(
                    "No important keywords are missing."
                )

            st.divider()

            st.subheader("📄 Resume Formatting Feedback")

            if formatting_feedback:

                for item in formatting_feedback:

                    st.info(item)

            else:

                st.success(
                    "Formatting looks professional."
                )

            st.divider()
            # --------------------------------------------
            # AI Resume Optimizer
            # --------------------------------------------

            st.subheader("✨ AI Resume Optimizer")

            if st.button(
                "🚀 Generate ATS Optimized Resume",
                key=f"optimize_{index}"
            ):

                with st.spinner("Optimizing Resume..."):

                    optimized = optimize_resume(
                        candidate["text"],
                        jd_text
                    )

                    if "error" in optimized:
                        st.error("❌ LLM returned invalid JSON.")
                        st.code(optimized["raw_output"])
                        st.stop()

                    validation = validate_resume(
                        candidate["text"],
                        optimized["optimized_resume"]
                    )

                    optimized_score = calculate_optimized_score(
                        optimized["optimized_resume"],
                        jd_text
                    )

                    rewritten = rewrite_resume(
                        optimized["optimized_resume"]
                    )

                    rewritten_resume = rewritten["rewritten_resume"]

                    latex_resume = generate_latex_resume(
                        candidate["name"],
                        rewritten_resume
                    )

                    tex_file = (
                        f"optimized_resume_{index}.tex"
                    )

                    save_latex_file(
                        latex_resume,
                        tex_file
                    )

                    pdf_file = compile_latex_to_pdf(
                        tex_file
                    )

                    

                    st.session_state[f"optimized_{index}"] = {
                        "optimized": optimized,
                        "validation": validation,
                        "optimized_score": optimized_score,
                        "rewritten_resume": rewritten_resume,
                        "latex_resume": latex_resume,
                        "pdf_file": pdf_file
                    }

            if f"optimized_{index}" in st.session_state:

                data = st.session_state[f"optimized_{index}"]

                optimized = data["optimized"]
                validation = data["validation"]
                optimized_score = data["optimized_score"]
                rewritten_resume = data["rewritten_resume"]
                latex_resume = data["latex_resume"]
                pdf_file = data["pdf_file"]

                original_final = float(final_score)
                optimized_final = float(
                    optimized_score["final_score"]
                )

                improvement = round(
                    optimized_final - original_final,
                    2
                )

                st.success("✅ Resume Optimized Successfully!")
                st.balloons()

                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "📄 Rewritten Resume",
                        "📝 Overleaf Source",
                        "📊 Recruiter Report",
                        "⬇ Downloads"
                    ]
                )
                with tab3:

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Original ATS",
                            f"{final_score:.2f}%"
                        )

                    with col2:
                        st.metric(
                            "Optimized ATS",
                            f"{optimized_score['final_score']:.2f}%"
                        )

                    with col3:
                        st.metric(
                            "Improvement",
                            f"+{improvement:.2f}%"
                        )

                    st.divider()

                    st.subheader("📈 ATS Score Improvement")

                    comparison = {
                        "Resume": ["Original", "Optimized"],
                        "ATS Score": [
                            final_score,
                            optimized_score["final_score"]
                        ]
                    }

                    fig = go.Figure()

                    fig.add_trace(
                        go.Bar(
                            x=comparison["Resume"],
                            y=comparison["ATS Score"],
                            text=[
                                f"{final_score:.2f}%",
                                f"{optimized_score['final_score']:.2f}%"
                            ],
                            textposition="outside"
                        )
                    )

                    fig.update_layout(
                        title="ATS Score Improvement",
                        height=400,
                        yaxis_title="ATS Score"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    st.divider()

                    st.subheader("🛡 Resume Validation")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Truthfulness Score",
                            f"{validation['truthfulness_score']}%"
                        )

                    with col2:
                        st.metric(
                            "Hallucination",
                            validation["hallucination_detected"]
                        )

                    st.success(
                        validation["summary"]
                    )

                    st.markdown("### ✅ Verified Sections")

                    for section in validation.get(
                        "verified_sections",
                        []
                    ):
                        st.success(section)

                    if validation.get("warnings"):

                        st.markdown("### ⚠ Warnings")

                        for warning in validation["warnings"]:
                            st.warning(warning)

                    st.divider()

                    st.subheader("👨‍💼 Recruiter Verdict")

                    if optimized_score["final_score"] >= 90:
                        st.success("🌟 Strong Hire")

                    elif optimized_score["final_score"] >= 80:
                        st.info("✅ Hire")

                    elif optimized_score["final_score"] >= 70:
                        st.warning("⚠️ Consider")

                    else:
                        st.error("❌ Reject")

                    st.divider()

                    st.markdown("### 📝 Optimization Summary")
                    st.success(
                        optimized.get("summary", "")
                    )

                    st.markdown("### 🎯 JD Keywords Added")

                    for keyword in optimized.get(
                        "keywords_added",
                        []
                    ):
                        st.success(keyword)

                    st.metric(
                        "Keywords Added",
                        optimized.get("keyword_count", 0)
                    )

                    st.divider()

                    st.markdown("### 🔧 Resume Changes")

                    for change in optimized.get(
                        "changes",
                        []
                    ):
                        st.info(change)

                    st.markdown("### 📈 ATS Improvements")

                    for item in optimized.get(
                        "ats_improvements",
                        []
                    ):
                        st.success(item)

                    st.divider()
                    with tab1:

                        st.markdown("### ✍ Recruiter-Ready Rewritten Resume")

                        st.text_area(
                            "Rewritten Resume",
                            rewritten_resume,
                            height=600,
                    key=f"rewritten_resume_{index}"
                        )

                with tab2:

                    st.markdown("### 📝 Overleaf LaTeX Source")

                    st.code(
                        latex_resume,
                        language="latex"
                    )

                    with open(
                        f"optimized_resume_{index}.tex",
                        "r",
                        encoding="utf-8"
                    ) as file:

                        st.download_button(
                            "📥 Download Overleaf (.tex)",
                            data=file.read(),
                            file_name="Professional_Resume.tex",
                            mime="text/plain",
                            key=f"latex_download_{index}"
                        )

                    # --------------------------------------------
                    # Generate Professional PDF from LaTeX
                    # --------------------------------------------

                    pdf_file = compile_latex_to_pdf(
                        f"optimized_resume_{index}.tex"
                    )

                    if pdf_file:

                        with open(
                            pdf_file,
                            "rb"
                        ) as file:

                            st.download_button(
                                "📄 Download Professional Resume (PDF)",
                                data=file,
                                file_name="Professional_Resume.pdf",
                                mime="application/pdf",
                                key=f"latex_pdf_{index}"
                            )

                    else:

                        st.info(
                            "📄 A professional LaTeX resume has been generated successfully.\n\n"
                            "• On your local machine (MiKTeX/TeX Live installed), you can compile it directly to a PDF.\n"
                            "• On Streamlit Cloud, LaTeX compilers are not available, so only the .tex file is provided.\n"
                            "• You can also upload the .tex file to Overleaf to edit and generate a high-quality PDF."
                        )

                    st.divider()

                with tab4:

                    export_resume_docx(
                        rewritten_resume,
                        f"rewritten_resume_{index}.docx"
                    )

                    export_resume_pdf(
                        rewritten_resume,
                        f"rewritten_resume_{index}.pdf"
                    )

                    export_resume_docx(
                        optimized["optimized_resume"],
                        f"optimized_resume_{index}.docx"
                    )

                    export_resume_pdf(
                        optimized["optimized_resume"],
                        f"optimized_resume_{index}.pdf"
                    )

                    generate_resume_report(
                        candidate_name=candidate["name"],
                        final_score=final_score,
                        optimized_score=optimized_score,
                        optimized=optimized,
                        validation=validation,
                        recruiter=recruiter,
                        output_path=f"resume_report_{index}.docx"
                    )

                    st.subheader("⬇ Download Files")

                    with open(
                        f"rewritten_resume_{index}.docx",
                        "rb"
                    ) as file:

                        st.download_button(
                            "📄 Recruiter Ready Resume (DOCX)",
                            data=file,
                            file_name="Recruiter_Ready_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"rewritten_docx_{index}"
                        )

                    with open(
                        f"rewritten_resume_{index}.pdf",
                        "rb"
                    ) as file:

                        st.download_button(
                            "📄 Recruiter Ready Resume (PDF)",
                            data=file,
                            file_name="Recruiter_Ready_Resume.pdf",
                            mime="application/pdf",
                            key=f"rewritten_pdf_{index}"
                        )

                    with open(
                        f"optimized_resume_{index}.docx",
                        "rb"
                    ) as file:

                        st.download_button(
                            "🚀 ATS Optimized Resume (DOCX)",
                            data=file,
                            file_name="ATS_Optimized_Resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"optimized_docx_{index}"
                        )

                    with open(
                        f"optimized_resume_{index}.pdf",
                        "rb"
                    ) as file:

                        st.download_button(
                            "🚀 ATS Optimized Resume (PDF)",
                            data=file,
                            file_name="ATS_Optimized_Resume.pdf",
                            mime="application/pdf",
                            key=f"optimized_pdf_{index}"
                        )
                        st.divider()

                    st.subheader(
                        "🌟 Professional Resume"
                    )

                    if pdf_file:

                        with open(
                            pdf_file,
                            "rb"
                        ) as file:

                            st.download_button(
                                "📄 Download Professional Resume (LaTeX PDF)",
                                data=file,
                                file_name="Professional_Resume.pdf",
                                mime="application/pdf",
                                key=f"professional_pdf_{index}"
                            )

                    else:

                        st.warning(
                            "Professional Resume could not be generated."
                        )

                    with open(
                        f"resume_report_{index}.docx",
                        "rb"
                    ) as file:

                        st.download_button(
                            "📊 Recruiter Report",
                            data=file,
                            file_name="Recruiter_Report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"report_{index}"
                        )

                st.divider()

                st.markdown("## 📄 Before vs After Resume")

                left, right = st.columns(2)

                with left:

                    st.markdown("### Original Resume")

                    st.text_area(
                        "Original",
                        candidate["text"],
                        height=550,
                        key=f"before_resume_{index}"
                    )

                with right:

                    st.markdown("### ATS Optimized Resume")

                    st.text_area(
                        "Optimized",
                        optimized["optimized_resume"],
                        height=550,
                        key=f"after_resume_{index}"
                    )

                st.divider()

            # --------------------------------------------
            # Recruiter Decision
            # --------------------------------------------

            st.subheader("✅ Final Hiring Recommendation")

            if final_score >= 85:

                st.success(
                    "🟢 Strong Hire — Candidate is highly suitable for this position."
                )

            elif final_score >= 70:

                st.info(
                    "🟡 Hire — Good candidate. Recommended for interview."
                )

            elif final_score >= 50:

                st.warning(
                    "🟠 Hold — Manual recruiter review recommended."
                )

            else:

                st.error(
                    "🔴 Reject — Candidate does not sufficiently match the role."
                )

            st.divider()

            # --------------------------------------------
            # Export Section
            # --------------------------------------------

            st.subheader("📥 Export")

            st.download_button(
                label="Download Candidate Summary",
                data=f"""
Candidate: {candidate['name']}
ATS Score: {final_score:.2f}%
Grade: {recruiter["grade"]}
Recommendation: {recruiter["decision"]}
""",
                file_name=f"{candidate['name']}_summary.txt",
                mime="text/plain",
                key=f"download_{index}"
            )
            st.divider()

    # ==================================================
    # Analysis Completed Banner
    # ==================================================

    st.success("🎉 Resume Screening Completed Successfully!")

    st.balloons()

    st.markdown(
        """
### 📌 Analysis Summary

✅ Job Description Parsed Successfully

✅ Resume Parsing Completed

✅ Candidate Ranking Generated

✅ ATS Match Scores Calculated

✅ Recruiter Dashboard Generated

✅ AI Hiring Recommendations Prepared
"""
    )

    st.divider()

    # ==================================================
    # Footer Statistics
    # ==================================================

    footer1, footer2, footer3 = st.columns(3)

    with footer1:
        st.metric(
            "Candidates Processed",
            total_candidates
        )

    with footer2:
        st.metric(
            "Average ATS Score",
            f"{average_score:.2f}%"
        )

    with footer3:
        st.metric(
            "Top Candidate",
            rankings[0]["name"]
        )

    st.divider()

    # ==================================================
    # Footer
    # ==================================================

    st.markdown(
        """
---
### 🚀 AI Resume Screener

Built using:

- 🤖 Large Language Models (LLM Ready)
- 🔍 Semantic Resume Matching
- 📄 Resume Parsing
- 📊 Recruiter Analytics Dashboard
- 🎯 ATS Score Evaluation
- 💼 AI Hiring Recommendation Engine

**Tech Stack**

Python • Streamlit • NLP • Semantic Search • AI • Resume Intelligence

Version **1.0**
"""
    )