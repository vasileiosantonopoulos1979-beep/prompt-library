import streamlit as st
import json
from datetime import datetime

# Initialize session state for prompts
if 'prompts' not in st.session_state:
    st.session_state.prompts = []

st.title("🔖 Prompt Library")

# Sidebar for adding new prompts
with st.sidebar:
    st.header("Add New Prompt")
    title = st.text_input("Title")
    category = st.selectbox("Category", ["General", "Coding", "Writing", "Analysis", "Creative"])
    prompt_text = st.text_area("Prompt", height=150)
    tags = st.text_input("Tags (comma-separated)")
    
    if st.button("Save Prompt"):
        if title and prompt_text:
            new_prompt = {
                "id": len(st.session_state.prompts),
                "title": title,
                "category": category,
                "prompt": prompt_text,
                "tags": [t.strip() for t in tags.split(",") if t.strip()],
                "created": datetime.now().isoformat()
            }
            st.session_state.prompts.append(new_prompt)
            st.success("Prompt saved!")
            st.rerun()

# Main area - display and search prompts
search = st.text_input("🔍 Search prompts", placeholder="Search by title, tags, or content...")
filter_category = st.multiselect("Filter by category", ["General", "Coding", "Writing", "Analysis", "Creative"])

# Filter prompts
filtered_prompts = st.session_state.prompts
if search:
    filtered_prompts = [p for p in filtered_prompts if 
                       search.lower() in p['title'].lower() or 
                       search.lower() in p['prompt'].lower() or
                       any(search.lower() in tag.lower() for tag in p['tags'])]
if filter_category:
    filtered_prompts = [p for p in filtered_prompts if p['category'] in filter_category]

# Display prompts
for prompt in filtered_prompts:
    with st.expander(f"📝 {prompt['title']} - *{prompt['category']}*"):
        st.write(prompt['prompt'])
        st.caption(f"Tags: {', '.join(prompt['tags']) if prompt['tags'] else 'None'}")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("📋 Copy", key=f"copy_{prompt['id']}"):
                st.code(prompt['prompt'], language=None)
        with col2:
            if st.button("🗑️ Delete", key=f"del_{prompt['id']}"):
                st.session_state.prompts = [p for p in st.session_state.prompts if p['id'] != prompt['id']]
                st.rerun()

if not filtered_prompts:
    st.info("No prompts found. Add your first prompt using the sidebar!")
