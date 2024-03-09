import streamlit as st
from data_management import save_uploaded_images, submit_proposal, submit_completion, save_uploaded_file
from utils import format_proposal_as_markdown,generate_unique_id

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
            objective_image = st.file_uploader("Upload an image for objective if needed", type=["jpg", "jpeg", "png"],key="objective_image")
            rationale = st.text_area("Rationale")
            timeline = st.text_area("Timeline")
            contributors = st.text_input("Contributors")
            proposal_id = generate_unique_id()

        with right_col:
            semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
            expected_students = st.number_input("Expected number of students", min_value=1, value=1)
            mentor_email = st.text_input("Mentor email")
            dataset = st.text_area("Dataset")
            dataset_image = st.file_uploader("Upload an image for dataset", type=["jpg", "jpeg", "png"], key="dataset_image")
            approach = st.text_area("Approach")
            possible_issues = st.text_area("Possible Issues")
            possible_issues_image = st.file_uploader("Upload an image for possible issues", type=["jpg", "jpeg", "png"],key="possible_issues_image")
            year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])
            proposed_by_professor = st.checkbox("Proposed by a Professor")
        
       


        preview = st.form_submit_button("Preview")
        submitted = st.form_submit_button("Submit")

        if submitted:
            save_uploaded_images(objective_image,dataset_image,possible_issues_image)
            proposal_data = {
                "name": name,
                "project_name": project_name,
                "mentor": mentor,
                "github_link": github_link,
                "objective": objective,
                "objective_image_name" : objective_image.name if objective_image is not None else "Not Uploaded",
                "rationale": rationale,
                "timeline": timeline,
                "contributors": contributors,
                "semester": semester,
                "expected_students": expected_students,
                "mentor_email": mentor_email,
                "dataset": dataset,
                "dataset_image_name" : dataset_image.name if dataset_image is not None else "Not Uploaded",
                "approach": approach,
                "possible_issues": possible_issues,
                "possible_issues_image_name": possible_issues_image.name if possible_issues_image is not None else "Not Uploaded",
                "year": year,
                "proposal_id": proposal_id,
                "proposed_by_professor":proposed_by_professor
                
            }
            # proposal_data = pd.DataFrame.from_dict(proposal_data, orient = "index")
            submit_proposal(proposal_data)
            st.info(f' Proposal ID: {proposal_id}. This is an info alert! Make sure to note down your proposal ID number!')

        # Initialize variable names with default values
        objective_image_name = "Not Uploaded"
        dataset_image_name = "Not Uploaded"
        possible_issues_image_name = "Not Uploaded"

        if preview:
            if objective_image is not None:
                st.session_state.objective_image_up = objective_image.getvalue()
                objective_image_name = objective_image.name
            # No else part needed since default value is already set

            if dataset_image is not None:
                st.session_state.dataset_image_up = dataset_image.getvalue()
                dataset_image_name = dataset_image.name
            # No else part needed since default value is already set

            if possible_issues_image is not None:
                st.session_state.possible_issues_image_up = possible_issues_image.getvalue()
                possible_issues_image_name = possible_issues_image.name
            # No else part needed since default value is already set
        
            preview_data = {
                "name": name,
                "project_name": project_name,
                "mentor": mentor,
                "github_link": github_link,
                "objective": objective,
                "objective_image_name" : objective_image_name,
                "rationale": rationale,
                "timeline": timeline,
                "contributors": contributors,
                "semester": semester,
                "expected_students": expected_students,
                "mentor_email": mentor_email,
                "dataset": dataset,
                "dataset_image_name" : dataset_image_name,
                "approach": approach,
                "possible_issues": possible_issues,
                "possible_issues_image_name": possible_issues_image_name ,
                "year": year,
                "proposal_id": proposal_id,
                "proposed_by_professor" : proposed_by_professor

            }
        
            st.markdown(format_proposal_as_markdown(preview_data), unsafe_allow_html=True)



# Function to handle the project completion form
def completion_form():
    st.subheader("Project Completion Form")
    with st.form(key='completion_form'):
        # You can add other input fields as necessary
        project_title = st.text_input("Project Title")
        video_link = st.text_input("Video Link")
        github_repo = st.text_input("GitHub Repository")
        project_website = st.text_input("Project Website Link if available")

        # Word document upload field
        uploaded_file = st.file_uploader("Upload your project document", type=['docx'])

        # Form submission button
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            # Save the uploaded Word document when the form is submitted
            save_uploaded_file(uploaded_file)
            completion = {
                "project title" : project_title,
                "Video Link" : video_link,
                "github repo" : github_repo,
                "project website": project_website,
                "Project Document" : uploaded_file.name if uploaded_file is not None else "File not uploaded"
            }
            submit_completion(completion)


