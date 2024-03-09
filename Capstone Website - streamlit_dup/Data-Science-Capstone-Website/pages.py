import streamlit as st
from data_management import approve_proposal, reject_proposal, approve_completion, edit_proposal, edit_completion,handle_approve,handle_reject,handle_edit
from utils import format_proposal_as_markdown, format_completion_as_markdown,archive_source_repo_into_target,entry
import pandas as pd

local_dir = r"D:\Capstone Website - streamlit_dup\Data-Science-Capstone-Website\github clones"
target_repo_url = "https://github.com/Renga-99/Data-Science-Capstone-Website.git"
# source_repo_url = "https://github.com/mecaneer23/python-snake-game.git"
def pending_approval_page():
    if st.session_state['proposals']:
        for index, proposal in enumerate(st.session_state['proposals']):
            with st.expander(f"Approve/Reject {proposal['project_name']}"):
                st.markdown(format_proposal_as_markdown(proposal), unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    approve_button = st.button("Approve", key=f"approve_{index}")
                    if approve_button:
                        st.session_state[f'approve_{index}_clicked'] = True
                
                with col2:
                    reject_button = st.button("Reject", key=f"reject_{index}")
                    if reject_button:
                        st.session_state[f'reject_{index}_clicked'] = True
                
                with col3:
                    edit_button = st.button("Edit", key=f"edit_{index}")
                    if edit_button:
                        st.session_state[f'edit_{index}_clicked'] = True
                
                # Handle actions
                handle_approve(index)
                handle_reject(index)
                handle_edit(index)
    else:
        st.write("No pending proposals")

def show_approved(proposal):
    
    if st.session_state['approved']:
        st.table(proposal)
    else:
        st.write("No approved proposals")

def show_rejected(proposal):
    if st.session_state['rejected']:
        st.table(proposal)
    else:
        st.write("No rejected proposals")


def pending_completion_page():
 
    if st.session_state['completion']:
        for index, completion in enumerate(st.session_state['completion']):
            with st.expander(f"Approve/Edit Project Completion {completion['project title']}"):
                # st.table(completion)
                st.markdown(format_completion_as_markdown(completion),unsafe_allow_html= True)
                if st.button("Approve Completion", key=f"approve_comp_{index}"):
                    archive_source_repo_into_target(completion['github repo'], target_repo_url, local_dir) 
                    approve_completion(index)

                       
                if st.button("Edit", key=f"edit_comp_{index}"):

                    edit_completion(index)  # Pass the updated completion data
 
    else:
        st.write("No pending project completions")

def show_completed_projects(completion):
    if st.session_state['approved_completion']:
        st.table(completion)
    else:
        st.write("No completed projects")

