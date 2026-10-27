import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


import streamlit as st
import time

st.set_page_config(
    page_title="Research Agent Pipeline",
    page_icon="🤖",
    layout="centered"
)

st.title("Research Pipeline Runner")
st.write("Run the multi-agent research pipeline (`Search Agent` -> `Reader Agent` -> `Writer Chain` -> `Critic Chain`).")

# Topic input
topic = st.text_input("Research Topic", placeholder="e.g. Autonomous Agents in 2026")

# Execution mode toggle
mode = st.radio("Mode", ["Live Pipeline", "Mock Demo"], horizontal=True)

def run_pipeline(topic_str):
    results = {}
    
    # Step 1
    with st.spinner("Step 1/4: Search agent is searching the web..."):
        if mode == "Live Pipeline":
            try:
                from src.agents.agents import build_search_agent
                search_agent = build_search_agent()
                res = search_agent.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_str}")]})
                results["search"] = res['messages'][-1].content
            except Exception as e:
                st.error(f"Search Agent error: {e}")
                return None
        else:
            time.sleep(1)
            results["search"] = f"Search results for: {topic_str}. Found recent papers, market reports, and key technical benchmarks."

    # Step 2
    with st.spinner("Step 2/4: Reader agent is scraping top resources..."):
        if mode == "Live Pipeline":
            try:
                from src.agents.agents import build_reader_agent
                reader_agent = build_reader_agent()
                res = reader_agent.invoke({"messages": [("user", f"Based on the search results, pick the most relevant URL and scrape it.\n\nSearch Results:\n{results['search'][:800]}")]})
                results["scraped"] = res['messages'][-1].content
            except Exception as e:
                st.error(f"Reader Agent error: {e}")
                return None
        else:
            time.sleep(1)
            results["scraped"] = f"Scraped content from top source: Detailed metrics and architectural overview of {topic_str}."

    # Step 3
    with st.spinner("Step 3/4: Writer chain is drafting the report..."):
        if mode == "Live Pipeline":
            try:
                from src.agents.agents import writer_chain
                research_combined = f"SEARCH RESULTS : \n {results['search']} \n\nDETAILED SCRAPED CONTENT : \n {results['scraped']}"
                results["report"] = writer_chain.invoke({"topic": topic_str, "research": research_combined})
            except Exception as e:
                st.error(f"Writer Chain error: {e}")
                return None
        else:
            time.sleep(1.5)
            results["report"] = f"# Report: {topic_str}\n\n## Overview\nThis report synthesizes recent findings on {topic_str}. Key takeaways indicate rapid advancement and strong market adoption.\n\n## Details\n- High scalability\n- Robust integration capabilities"

    # Step 4
    with st.spinner("Step 4/4: Critic chain is reviewing the report..."):
        if mode == "Live Pipeline":
            try:
                from src.agents.agents import critic_chain
                report_content = results["report"].content if hasattr(results["report"], "content") else str(results["report"])
                results["feedback"] = critic_chain.invoke({"report": report_content})
            except Exception as e:
                st.error(f"Critic Chain error: {e}")
                return None
        else:
            time.sleep(1)
            results["feedback"] = "Critic Feedback: Well-structured report. Recommendation: Expand section 2 with concrete code examples."

    return results

if st.button("Run Pipeline"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        output = run_pipeline(topic)
        if output:
            st.success("Pipeline executed successfully!")
            
            st.subheader("Final Report")
            report_text = output["report"].content if hasattr(output["report"], "content") else str(output["report"])
            st.markdown(report_text)
            
            with st.expander("View Critic Feedback"):
                feedback_text = output["feedback"].content if hasattr(output["feedback"], "content") else str(output["feedback"])
                st.write(feedback_text)
                
            with st.expander("View Raw Search & Scraped Data"):
                st.text("Search Results:")
                st.write(output["search"])
                st.text("Scraped Content:")
                st.write(output["scraped"])