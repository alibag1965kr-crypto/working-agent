import streamlit as st
from engine import analyze_notice
from utils import extract_text_from_pdf

st.set_page_config(
    page_title="NoticeAble AI",
    page_icon="📄",
    layout="wide",
)

st.title("📄 NoticeAble AI")
st.caption("Making important public information easier to understand.")

st.info(
    "NoticeAble AI turns public notices into explanations, "
    "document checklists, and action plans using local AI."
)

st.warning(
    "This is an experimental tool, not an official government service. "
    "Verify important dates and requirements against the original notice."
)

with st.sidebar:
    st.header("About this project")
    st.write(
        "NoticeAble AI helps people navigate complicated administrative "
        "information using locally running AI."
    )
    st.markdown("**Technology**")
    st.write("Python · Streamlit · Ollama · Pydantic")
    st.markdown("**Privacy**")
    st.write(
        "Notice text is sent to your configured Ollama server. "
        "Avoid entering confidential or sensitive personal information."
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Your notice")

    input_type = st.radio(
        "Choose input type",
        ["Paste text", "Upload PDF"],
        horizontal=True,
    )

    raw_text = ""

    if input_type == "Paste text":
        raw_text = st.text_area(
            "Paste the notice here",
            height=300,
            placeholder="Paste a scholarship notice, college circular, "
                        "public announcement, or other notice...",
        )

    else:
        uploaded_file = st.file_uploader(
            "Upload a text-based PDF",
            type=["pdf"],
        )

        if uploaded_file:
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
                st.success(
                    f"Extracted {len(raw_text)} characters from the PDF."
                )
            except Exception as exc:
                st.error(str(exc))

    analyze_button = st.button(
        "✨ Generate Action Plan",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.subheader("📋 Your actionable insights")

    st.write(
        "Your results will include a plain-language summary, "
        "eligibility conditions, required documents, a step-by-step "
        "action plan, and information that needs verification."
    )

    if analyze_button:
        if not raw_text.strip():
            st.error("Please paste a notice or upload a readable PDF.")

        else:
            try:
                with st.spinner("Analyzing with your local AI model..."):
                    analysis = analyze_notice(raw_text)

                st.success("Analysis completed.")

                st.markdown("### 💡 Simple explanation")
                st.write(analysis.summary)

                st.markdown("### 🎓 Eligibility criteria")

                if analysis.eligibility_criteria:
                    for item in analysis.eligibility_criteria:
                        st.markdown(f"- {item}")
                else:
                    st.write("No explicit criteria were identified.")

                st.markdown("### 📁 Required documents")

                if analysis.required_documents:
                    for document in analysis.required_documents:
                        st.markdown(f"- {document}")
                else:
                    st.write("No documents were explicitly identified.")

                st.markdown("### 📅 Action plan")

                if analysis.action_plan:
                    for index, action in enumerate(
                        analysis.action_plan, start=1
                    ):
                        st.info(
                            f"**Step {index}: {action.task}\n\n"
                            f"Deadline: {action.deadline}**"
                        )
                else:
                    st.write("No action steps were identified.")

                st.markdown("### 🔎 Verify these details")

                if analysis.missing_information:
                    for item in analysis.missing_information:
                        st.warning(item)
                else:
                    st.write(
                        "No missing details were identified by the model. "
                        "This does not guarantee the notice is complete."
                    )

                with st.expander("View structured analysis"):
                    st.json(analysis.model_dump())

            except Exception as exc:
                st.error(
                    "Analysis failed. Check that Ollama is running, "
                    "the model is installed, and your dependencies "
                    f"are available.\n\nDetails: {exc}"
                )

st.divider()

st.caption(
    "NoticeAble AI · Open-source prototype · "
    "Always verify critical details with the issuing organization."
)
