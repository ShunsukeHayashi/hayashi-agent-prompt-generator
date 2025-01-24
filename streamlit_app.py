import streamlit as st
from app import HayashiAgent

def main():
    st.set_page_config(
        page_title="Hayashi Agent",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize agent
    agent = HayashiAgent()
    
    # Header
    st.title("🤖 Hayashi Agent System")
    st.markdown("---")
    
    # Mode selection
    modes = [mode['name'] for mode in agent.config['operational_modes']]
    selected_mode = st.selectbox(
        "Select Operation Mode",
        modes,
        index=modes.index('architect') if 'architect' in modes else 0
    )
    
    # Display environment info
    with st.expander("Environment Information", expanded=False):
        st.json(agent.environment)
    
    # Generate and display prompt
    st.markdown("## Generated Prompt")
    prompt = agent.render_prompt(mode=selected_mode)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Formatted View", "Raw Text"])
    
    with tab1:
        st.markdown(prompt)
    
    with tab2:
        st.text_area(
            "Raw Prompt",
            value=prompt,
            height=500,
            disabled=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"Hayashi Agent v{agent.config['version']} | "
        f"Mode: {selected_mode} | "
        f"Environment: {agent.environment['type']}"
    )

if __name__ == "__main__":
    main() 