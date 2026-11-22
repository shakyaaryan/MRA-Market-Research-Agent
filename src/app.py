import streamlit as st

from workflow.graph import run_research

st.set_page_config(
    page_title="Market Research Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Market Research Assistant")
st.caption("A multi-agent workflow for evidence-based market research.")

with st.sidebar:
    st.subheader("How it works")
    st.markdown(
        """
        1. **Researcher** gathers web evidence.
        2. **Analyst** writes a research brief.
        3. **Critic** reviews the brief.
        4. **Analyst** revises it once if needed.
        """
    )
    st.info("Research quality depends on the availability and reliability of public sources.")

query = st.text_area(
    "Enter a company or industry to research",
    placeholder="Example: Analyze the food delivery market in Nepal.",
    height=110,
)

if st.button("Start research", type="primary", disabled=not query.strip()):
    try:
        with st.spinner("Agents are researching and preparing your brief..."):
            result = run_research(query.strip())

        st.success("Research workflow completed.")
        st.markdown(result["final_report"])

        with st.expander("View research evidence"):
            for index, finding in enumerate(result.get("findings", []), start=1):
                st.markdown(f"**{index}. {finding.title}**")
                st.write(finding.content)
                st.markdown(f"[Open source]({finding.source_url})")
                st.divider()

        with st.expander("View critic review"):
            st.write(result.get("critic_feedback", "No critic feedback recorded."))
            st.write(f"Approved: {result.get('approved', False)}")
            st.write(f"Revisions made: {result.get('revision_count', 0)}")

    except Exception as exc:
        st.error(f"The research workflow failed: {exc}")
        st.caption("Check that your API keys are configured and that you have an internet connection.")
