import streamlit as st
import pandas as pd
from pages import pending_approval_page, show_approved, show_rejected, pending_completion_page, show_completed_projects
from forms import proposal_request_form, completion_form
from data_management import initialize_session_state,show_to_edit_completion,show_to_edit_proposals

def display_sidebar():
    """Displays the sidebar for navigation."""
    st.sidebar.title("Navigation")
    projects_options = ["Proposal Request", "Pending Approval", "Edit Proposals", "Rejected Proposals", "Approved Projects"]
    completed_projects_options = ["Project Completion Form", "Project Completion Approval", "Edit Project Completion", "Completed Projects"]
    
    # Active page handling
    if 'active_page' not in st.session_state:
        st.session_state.active_page = "Proposal Request" 
    
    with st.sidebar:
        with st.expander("Projects & Proposals"):
            for option in projects_options:
                if st.button(option):
                    st.session_state.active_page = option
        
        with st.expander("Completed Projects"):
            for option in completed_projects_options:
                if st.button(option):
                    st.session_state.active_page = option

def filter_proposals(proposals_df):
    """Applies filters to the proposals DataFrame and returns the filtered DataFrame."""
    
    
    if proposals_df.empty:
        return pd.DataFrame()  # Return an empty DataFrame if there are no proposals

    # Sidebar filters
    unique_semesters = proposals_df['semester'].unique().tolist()
    unique_project_names = proposals_df['project_name'].unique().tolist()
    unique_years = proposals_df['year'].unique().tolist()
    
    selected_project_name = st.sidebar.selectbox("Filter by Project Name:", ['All'] + unique_project_names)
    selected_semester = st.sidebar.selectbox("Filter by Semester:", ['All'] + unique_semesters)
    selected_year = st.sidebar.selectbox("Filter by Year:", ['All'] + unique_years)
    
    # Apply filters
    if selected_semester != 'All':
        proposals_df = proposals_df[proposals_df['semester'] == selected_semester]
    if selected_project_name != 'All':
        proposals_df = proposals_df[proposals_df['project_name'] == selected_project_name]
    if selected_year != 'All':
        proposals_df = proposals_df[proposals_df['year'] == selected_year]
    
    return proposals_df

def main():
    st.image("gw-data-science-header.jpg", use_column_width=True)
    st.title("Data Science Capstone Website")

    # Initialize session state for app-wide variables
    initialize_session_state()

    # Display sidebar for navigation
    display_sidebar()
    proposals_df = pd.DataFrame(st.session_state.get('approved', []))
    rejected_df = pd.DataFrame(st.session_state.get('rejected', []))
    completion_df = pd.DataFrame(st.session_state.get('approved_completion', []))
    # filtered_proposals = filter_proposals()  # Apply filters to proposals
    default_columns = ["name", "project_name", "mentor", "objective", "semester", "year"]
    # Define additional columns that can be added to the display
    additional_columns = ["rationale","expected_students", "github_link", "dataset","timeline","approach","possible_issues"] 

    # source_repo_url = "https://github.com/mecaneer23/python-snake-game.git"
    # Display content based on the active page
    if st.session_state.active_page == "Proposal Request":
        proposal_request_form()
 
    elif st.session_state.active_page == "Pending Approval":
        pending_approval_page()
    elif st.session_state.active_page == "Edit Proposals":
        show_to_edit_proposals()
        # show_prof_proposals()
        # show_to_edit_proposals()
    elif st.session_state.active_page == "Rejected Proposals":
        # Use a multiselect widget to allow users to select additional columns to display
        selected_columns = st.multiselect("Select additional columns to display:", additional_columns)
        # Combine default columns with selected additional columns
        columns_to_display = default_columns + selected_columns
        filtered_proposals = filter_proposals(rejected_df) 
        show_rejected(filtered_proposals[columns_to_display])

    elif st.session_state.active_page == "Approved Projects":
        # Use a multiselect widget to allow users to select additional columns to display
        selected_columns = st.multiselect("Select additional columns to display:", additional_columns)

        # Combine default columns with selected additional columns
        columns_to_display = default_columns + selected_columns
        filtered_proposals = filter_proposals(proposals_df) 
        show_approved(filtered_proposals[columns_to_display]) 

    elif st.session_state.active_page == "Project Completion Form":
        completion_form()
    elif st.session_state.active_page == "Project Completion Approval":
        pending_completion_page()
    elif st.session_state.active_page == "Edit Project Completion":
        show_to_edit_completion()
    elif st.session_state.active_page == "Completed Projects":
        show_completed_projects(completion_df)
    else:
        st.write("Select an option from the sidebar.")

if __name__ == "__main__":
    main()
