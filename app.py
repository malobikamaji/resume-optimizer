import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import re


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Resume Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #687386;
        margin-bottom: 30px;
    }

    /* Section title */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #172033;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Score card */
    .score-card {
        background: linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

        color: white;
        padding: 30px;
        border-radius: 18px;
        text-align: center;
        margin: 25px 0;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.25);
    }

    .score-number {
        font-size: 55px;
        font-weight: 800;
        margin: 8px 0;
    }

    .score-label {
        font-size: 18px;
        opacity: 0.9;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #7b8494;
        font-size: 14px;
        margin-top: 50px;
        padding-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [
    # Programming
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "typescript",

    # Web
    "html",
    "css",
    "react",
    "angular",
    "vue",
    "node.js",
    "django",
    "flask",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",

    # Data / BI
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",

    # Machine Learning / AI
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "artificial intelligence",

    # DevOps / Cloud
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",

    # Soft skills
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
    "project management"
]


# =========================================================
# FUNCTION: FIND SKILLS
# =========================================================

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(found_skills)


# =========================================================
# FUNCTION: CREATE REPORT
# =========================================================

def create_report(
    final_score,
    text_score,
    skill_score,
    matched_skills,
    missing_skills,
    recommendations
):

    current_time = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    report = f"""
==================================================
              RESUME OPTIMIZER REPORT
==================================================

Generated: {current_time}

--------------------------------------------------
RESUME MATCH SCORE
--------------------------------------------------

Overall Match Score: {final_score}%

Text Similarity: {text_score}%

Skill Match: {skill_score}%


--------------------------------------------------
MATCHING SKILLS
--------------------------------------------------

"""

    if matched_skills:

        report += "\n".join(
            f"✓ {skill.title()}"
            for skill in matched_skills
        )

    else:

        report += "No matching skills detected."


    report += """

--------------------------------------------------
MISSING SKILLS
--------------------------------------------------

"""


    if missing_skills:

        report += "\n".join(
            f"✗ {skill.title()}"
            for skill in missing_skills
        )

    else:

        report += "No obvious missing skills detected."


    report += """

--------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------

"""


    for recommendation in recommendations:

        report += f"• {recommendation}\n"


    report += """

==================================================
              END OF REPORT
==================================================
"""

    return report


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📄 Resume Optimizer")

    st.write(
        "Analyze your resume against a job description "
        "and discover how well your skills match."
    )

    st.divider()

    st.markdown("### 🚀 How it works")

    st.write("1. Upload your resume")
    st.write("2. Paste a job description")
    st.write("3. Analyze your resume")
    st.write("4. Review your skill match")
    st.write("5. Download your report")

    st.divider()

    st.markdown("### 🛠️ Technologies")

    st.write("🐍 Python")
    st.write("🎨 Streamlit")
    st.write("📊 Scikit-learn")
    st.write("📄 PyPDF2")

    st.divider()

    st.caption(
        "Resume Optimizer • Portfolio Project"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 Resume Optimizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "Compare your resume with a job description "
    "and discover how well you match."
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# INPUT SECTION
# =========================================================

resume_column, job_column = st.columns(2)


# =========================================================
# RESUME UPLOAD
# =========================================================

with resume_column:

    st.markdown(
        '<div class="section-title">📄 Your Resume</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload your resume in PDF format."
    )

    resume_text = ""

    if uploaded_file is not None:

        try:

            pdf_reader = PdfReader(
                uploaded_file
            )

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:

                    resume_text += page_text

            st.success(
                f"Resume uploaded successfully! "
                f"({len(pdf_reader.pages)} page(s))"
            )

        except Exception as error:

            st.error(
                "Unable to read this PDF."
            )

            st.exception(error)


# =========================================================
# JOB DESCRIPTION
# =========================================================

with job_column:

    st.markdown(
        '<div class="section-title">💼 Target Job</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Paste the complete job description here...\n\n"
            "Example:\n"
            "We are looking for a Python Developer "
            "with experience in Python, SQL, Pandas "
            "and Machine Learning."
        )
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.markdown("")

analyze_button = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze_button:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

        st.stop()


    if not resume_text.strip():

        st.warning(
            "⚠️ No readable text was found in your PDF."
        )

        st.stop()


    if not job_description.strip():

        st.warning(
            "⚠️ Please paste a job description first."
        )

        st.stop()


    # -----------------------------------------------------
    # TEXT SIMILARITY
    # -----------------------------------------------------

    documents = [
        resume_text,
        job_description
    ]

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf_matrix = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        text_score = round(
            similarity * 100,
            2
        )

    except Exception:

        text_score = 0


    # -----------------------------------------------------
    # SKILL DETECTION
    # -----------------------------------------------------

    resume_skills = find_skills(
        resume_text
    )

    job_skills = find_skills(
        job_description
    )


    matched_skills = sorted(
        set(resume_skills).intersection(
            set(job_skills)
        )
    )


    missing_skills = sorted(
        set(job_skills).difference(
            set(resume_skills)
        )
    )


    # -----------------------------------------------------
    # SKILL SCORE
    # -----------------------------------------------------

    if len(job_skills) > 0:

        skill_score = round(
            (
                len(matched_skills)
                /
                len(job_skills)
            )
            * 100,
            2
        )

    else:

        skill_score = 0


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    final_score = round(
        (text_score * 0.4)
        +
        (skill_score * 0.6),
        2
    )


    # -----------------------------------------------------
    # SCORE DESCRIPTION
    # -----------------------------------------------------

    if final_score >= 80:

        score_label = "Excellent Match"

    elif final_score >= 60:

        score_label = "Good Match"

    elif final_score >= 40:

        score_label = "Moderate Match"

    else:

        score_label = "Needs Improvement"


    # =====================================================
    # SCORE DISPLAY
    # =====================================================

    st.markdown(
        f"""
        <div class="score-card">

            <div class="score-label">
                Overall Resume Match
            </div>

            <div class="score-number">
                {final_score}%
            </div>

            <div class="score-label">
                {score_label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # PROGRESS BAR
    # =====================================================

    st.progress(
        min(final_score / 100, 1.0)
    )


    # =====================================================
    # SCORE DETAILS
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Score Breakdown</div>',
        unsafe_allow_html=True
    )


    score_column1, score_column2, score_column3 = st.columns(3)


    with score_column1:

        st.metric(
            "Overall Score",
            f"{final_score}%"
        )


    with score_column2:

        st.metric(
            "Text Similarity",
            f"{text_score}%"
        )


    with score_column3:

        st.metric(
            "Skill Match",
            f"{skill_score}%"
        )


    # =====================================================
    # SKILL ANALYSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">🧠 Skill Analysis</div>',
        unsafe_allow_html=True
    )


    skill_column1, skill_column2 = st.columns(2)


    # =====================================================
    # MATCHING SKILLS
    # =====================================================

    with skill_column1:

        with st.container(border=True):

            st.subheader(
                "✅ Matching Skills"
            )

            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        skill.title()
                    )

            else:

                st.info(
                    "No matching skills detected."
                )


    # =====================================================
    # MISSING SKILLS
    # =====================================================

    with skill_column2:

        with st.container(border=True):

            st.subheader(
                "❌ Missing Skills"
            )

            if missing_skills:

                for skill in missing_skills:

                    st.error(
                        skill.title()
                    )

            else:

                st.success(
                    "No obvious missing skills detected!"
                )


    # =====================================================
    # ALL RESUME SKILLS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        "📋 Skills Found in Your Resume"
        "</div>",
        unsafe_allow_html=True
    )


    if resume_skills:

        skills_text = " • ".join(
            skill.title()
            for skill in resume_skills
        )

        st.info(
            skills_text
        )

    else:

        st.warning(
            "No recognized skills were found."
        )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        "💡 Improvement Suggestions"
        "</div>",
        unsafe_allow_html=True
    )


    recommendations = []


    if final_score < 40:

        recommendations.extend(
            [
                "Add relevant skills that you genuinely have.",
                "Highlight projects related to the target position.",
                "Rewrite experience bullets to emphasize relevant work.",
                "Add measurable achievements where possible."
            ]
        )


    elif final_score < 60:

        recommendations.extend(
            [
                "Add relevant missing skills if you genuinely have them.",
                "Highlight projects that are relevant to the position.",
                "Improve the wording of your experience descriptions.",
                "Include measurable achievements."
            ]
        )


    elif final_score < 80:

        recommendations.extend(
            [
                "Consider adding relevant missing skills you actually possess.",
                "Make your strongest experience more prominent.",
                "Add measurable results to your achievements.",
                "Keep your resume focused on the target position."
            ]
        )


    else:

        recommendations.extend(
            [
                "Your resume has a strong match with this position.",
                "Continue using measurable achievements.",
                "Keep the resume concise and focused.",
                "Make sure all listed skills represent genuine experience."
            ]
        )


    with st.container(border=True):

        for recommendation in recommendations:

            st.write(
                f"💡 {recommendation}"
            )


    # =====================================================
    # DOWNLOAD REPORT
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        "📥 Download Your Analysis"
        "</div>",
        unsafe_allow_html=True
    )


    report = create_report(
        final_score=final_score,
        text_score=text_score,
        skill_score=skill_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        recommendations=recommendations
    )


    st.download_button(
        label="📥 Download Resume Analysis",
        data=report,
        file_name="resume_analysis.txt",
        mime="text/plain",
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Resume Optimizer • Built with Python, Streamlit,
        Scikit-learn and PyPDF2
    </div>
    """,
    unsafe_allow_html=True
)