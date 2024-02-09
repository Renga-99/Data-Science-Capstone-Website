import streamlit as st
import pandas as pd
import numpy as np
# Initialize session state for storing proposals if it doesn't exist
if 'proposals' not in st.session_state:
    st.session_state['proposals'] = []

def submit_proposal(proposal_data):
    # Here you would implement saving the proposal data to a database or another storage
    # For simplicity, we're appending it to the session state
    st.session_state['proposals'].append(proposal_data)
    
    st.success("Proposal submitted successfully!")

def proposal_request_form():
    with st.form("proposal_form"):
        st.subheader("Proposal Request Form")
        left_col, right_col = st.columns(2)
        
        with left_col:
            name = st.text_input("Name")
            project_name = st.text_input("Project Name")
            mentor = st.text_input("Mentor for the project")
            github_link = st.text_input("Github Link")
            objective = st.text_area("Objective")
            rationale = st.text_area("Rationale")
            timeline = st.text_area("Timeline")
            contributors = st.text_input("Contributors")

        with right_col:
            semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall", "Winter"])
            expected_students = st.number_input("Expected number of students", min_value=1, value=1)
            mentor_email = st.text_input("Mentor email")
            dataset = st.text_area("Dataset")
            approach = st.text_area("Approach")
            possible_issues = st.text_area("Possible Issues")
            year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            proposal_data = {
                "name": name,
                "project_name": project_name,
                "mentor": mentor,
                "github_link": github_link,
                "objective": objective,
                "rationale": rationale,
                "timeline": timeline,
                "contributors": contributors,
                "semester": semester,
                "expected_students": expected_students,
                "mentor_email": mentor_email,
                "dataset": dataset,
                "approach": approach,
                "possible_issues": possible_issues,
                "year": year,
            }
            # proposal_data = pd.DataFrame.from_dict(proposal_data, orient = "index")
            submit_proposal(proposal_data)
# Function to display pending proposals
def pending_approval_page():
    st.subheader("Pending Approval")
    
    # Filter out only the proposals that are pending
    pending_proposals = [p for p in st.session_state['proposals']]
    
    # Display the proposals in a table
    for proposal in pending_proposals:
        st.write(proposal['name'], proposal['project_name'], proposal['status'])
        


def main():
    st.title("Data Science Capstone Website")
    page = st.selectbox("Navigate to:", ["Proposal Request", "Pending Approval", "Rejected", "Approved Projects", "Completion", "Pending Completion", "Completed Projects"], index=0)

    if page == "Proposal Request":
        proposal_request_form()
    elif page == "Pending Approval":
        st.subheader("Pending Approval")
        pending_approval_page()
        # Display approved proposals here
    elif page == "Rejected":
        st.subheader("Rejected")
        # Display past projects here
    elif page == "Approved Projects":
        st.subheader("Approved Projects")
        # Display approval/rejection interface here
    elif page == "Completion":
        st.subheader("Completion")
        # Display approval/rejection interface here
    elif page == "Pending Completion":
        st.subheader("Pending Completion")
        # Display approval/rejection interface here
    elif page == "Completed Projects":
        st.subheader("Completed Projects")
        # Display approval/rejection interface here

if __name__ == "__main__":
    main()
