import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import os
from PIL import Image
import io
import base64
import shutil
from io import BytesIO
import stat
# Initialize session state for storing proposals if it doesn't exist
if 'proposals' not in st.session_state:
    st.session_state['proposals'] = []
if 'approved' not in st.session_state:
    st.session_state['approved'] = []
if 'rejected' not in st.session_state:
    st.session_state['rejected'] = []
# Initialize session state for uploaded document if it doesn't exist
if 'uploaded_word_doc' not in st.session_state:
    st.session_state['uploaded_word_doc'] = None
if 'uploaded_word_doc_name' not in st.session_state:
    st.session_state['uploaded_word_doc_name'] = ""
if 'completion' not in st.session_state:
    st.session_state['completion'] = []
if 'approved_completion' not in st.session_state:
    st.session_state['approved_completion'] = []
if 'edit_completion' not in st.session_state:
    st.session_state['edit_completion'] = []
if 'to_edit_proposal' not in st.session_state:
    st.session_state['to_edit_proposal'] = []
# If the 'editing_index' is not in session_state, add it.
if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = None
if 'objective_image_up' not in st.session_state:
    st.session_state.objective_image_up = None
if 'dataset_image_up' not in st.session_state:
    st.session_state.dataset_image_up = None
if 'possible_issues_image_up' not in st.session_state:
    st.session_state.possible_issues_image_up = None

# Function to save the uploaded Word document to the session state
def save_objective_photo(objective_file,dataset_file,possible_issues_file):
    
    if objective_file is not None:
        # Read the file data into a bytes object
        st.session_state.objective_image_up = objective_file.getvalue()
        st.success(f"Uploaded {objective_file.name} successfully.")
    if dataset_file is not None:
        # Read the file data into a bytes object
        st.session_state.dataset_image_up = dataset_file.getvalue()
        st.success(f"Uploaded {dataset_file.name} successfully.")
    if possible_issues_file is not None:
        # Read the file data into a bytes object
        st.session_state.possible_issues_image_up = possible_issues_file.getvalue()
        st.success(f"Uploaded {possible_issues_file.name} successfully.")


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
        
       


        preview = st.form_submit_button("Preview")
        submitted = st.form_submit_button("Submit")

        if submitted:
            save_objective_photo(objective_image,dataset_image,possible_issues_image)
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
                
            }
            # proposal_data = pd.DataFrame.from_dict(proposal_data, orient = "index")
            submit_proposal(proposal_data)

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

            }
        
            st.markdown(format_proposal_as_markdown(preview_data), unsafe_allow_html=True)
            # with st.expander("Preview Your Proposal"):
            #     with left_col:
            #         st.write(f"**Name:** {name}")
            #         st.write(f"**Project Name:** {project_name}")
            #         st.write(f"**Mentor:** {mentor}")
            #         st.write(f"**Github Link:** {github_link}")
            #         st.write(f"**Objective:** {objective}")
            #         st.write(f"**Rationale:** {rationale}")
            #         st.write(f"**Timeline:** {timeline}")
            #         st.write(f"**Contributors:** {contributors}")
            #     with right_col:
            #         st.write(f"**Semester:** {semester}")
            #         st.write(f"**Expected Students:** {expected_students}")
            #         st.write(f"**Dataset:** {dataset}")
            #         st.write(f"**Possible Issues:** {possible_issues}")
            #         st.write(f"**Year:** {year}")





def submit_proposal(proposal_data):
    st.session_state['proposals'].append(proposal_data)
    st.success("Proposal submitted successfully!")


def approve_proposal(index):
    proposal = st.session_state['proposals'].pop(index)
    st.session_state['approved'].append(proposal)
    st.rerun()

def reject_proposal(index):
    proposal = st.session_state['proposals'].pop(index)
    st.session_state['rejected'].append(proposal)
    st.rerun()

def edit_proposal(index):
    proposal = st.session_state['proposals'].pop(index)
    st.session_state['to_edit_proposal'].append(proposal)
    st.rerun()
def show_to_edit_proposals():
    df_edit = pd.DataFrame(st.session_state.to_edit_proposal)
    st.write(df_edit)

    for index, row in df_edit.iterrows():
        # The unique key for each button is created by appending the index to a base string
        if st.button(f"Edit {row['name']}", key=f"button_{index}"):
            # Save the index of the proposal being edited
            st.session_state['editing_index'] = index
            # Use Streamlit's session state to display the form
            st.session_state['show_edit_form'] = True
            # Break the loop to prevent more than one form from showing
            break
    # Check if we should display the editing form
    if st.session_state.get('show_edit_form', False):
        # Obtain the index of the proposal being edited
        index = st.session_state['editing_index']
        row = df_edit.loc[index]

        with st.form(key='edit_proposal_form'):
                st.subheader("Edit Proposal Request Form")
                left_col, right_col = st.columns(2)
                
                with left_col:
                    name = st.text_input("Name",value=df_edit.loc[index,"name"])
                    project_name = st.text_input("Project Name",value=df_edit.loc[index,"project_name"])
                    mentor = st.text_input("Mentor for the project",value=df_edit.loc[index,"mentor"])
                    github_link = st.text_input("Github Link",value=df_edit.loc[index,"github_link"])
                    objective = st.text_area("Objective",value=df_edit.loc[index,"objective"])
                    rationale = st.text_area("Rationale",value=df_edit.loc[index,"rationale"])
                    timeline = st.text_area("Timeline",value=df_edit.loc[index,"timeline"])
                    contributors = st.text_input("Contributors",value=df_edit.loc[index,"contributors"])

                with right_col:
                    semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
                    expected_students = st.number_input("Expected number of students",value=df_edit.loc[index,"expected_students"])
                    mentor_email = st.text_input("Mentor email",value=df_edit.loc[index,"mentor_email"])
                    dataset = st.text_area("Dataset",value=df_edit.loc[index,"dataset"])
                    approach = st.text_area("Approach",value=df_edit.loc[index,"approach"])
                    possible_issues = st.text_area("Possible Issues",value=df_edit.loc[index,"possible_issues"])
                    year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])

                submitted = st.form_submit_button("Submit")
                if submitted:
                            proposal_data_edit = {
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
                            # Update the appropriate proposal in the session state
                            st.session_state.to_edit_proposal[index] = proposal_data_edit
                            # Reset flags to hide the form
                            st.session_state['show_edit_form'] = False
                            st.session_state['editing_index'] = None

                            # Optionally, you can move the updated proposal back to the 'proposals' list
                            updated_proposal = st.session_state.to_edit_proposal.pop(index)
                            st.session_state.proposals.append(updated_proposal)

                            # Rerun the app to refresh the state and UI
                            st.rerun() 

# Function to convert PIL image to Base64
def pil_image_to_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format="JPEG")  # You can change 'JPEG' to 'PNG' if needed
    base64_img = base64.b64encode(img_buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{base64_img}"
def resize_image(image, width=300):
    # Calculate the target height to maintain the aspect ratio
    # Calculate the target height to maintain the aspect ratio
    aspect_ratio = image.height / image.width
    target_height = int(aspect_ratio * width)
    return image.resize((width, target_height))

def format_proposal_as_markdown(proposal):


    # Open the image from session state and convert to Base64
    if st.session_state.objective_image_up is not None:
        image_bytes_io = io.BytesIO(st.session_state.objective_image_up)
        image_obj = Image.open(image_bytes_io)
        resized_image = resize_image(image_obj)
        base64_image = pil_image_to_base64(resized_image)
        image_markdown_obj = f"![Uploaded Image]({base64_image})"
    else:
        image_markdown_obj = "No image uploaded"
    
    
    # Open the image from session state and convert to Base64
    if st.session_state.dataset_image_up is not None:
        image_bytes_io = io.BytesIO(st.session_state.dataset_image_up)
        image_data = Image.open(image_bytes_io)
        resized_image = resize_image(image_data)
        base64_image = pil_image_to_base64(resized_image)
        image_markdown_data = f"![Uploaded Image]({base64_image})"
    else:
        image_markdown_data = "No image uploaded"

    # Open the image from session state and convert to Base64
    if st.session_state.possible_issues_image_up is not None:
        image_bytes_io = io.BytesIO(st.session_state.possible_issues_image_up)
        image_issue = Image.open(image_bytes_io)
        resized_image = resize_image(image_issue)
        base64_image = pil_image_to_base64(resized_image)
        image_markdown_issue = f"![Uploaded Image]({base64_image})"
    else:
        image_markdown_issue = "No image uploaded"


    # Embed the Base64 image string in the Markdown template
    markdown_template = f"""
# Capstone Proposal
## {proposal["project_name"]}
### Proposed by: {proposal["name"]}
#### Mentor Email: {proposal["mentor_email"]}
#### Advisor: {proposal["mentor"]}
#### George Washington University  
#### Data Science Program

## 1. Objective:
{proposal["objective"]}


{image_markdown_obj}
## 2. Dataset:
{proposal["dataset"]}


{image_markdown_data}
## 3. Rationale:
{proposal["rationale"]}

## 4. Approach:
{proposal["approach"]}

## 5. Timeline:
{proposal["timeline"]}

## 6. Expected Number of Students:
{proposal["expected_students"]}

## 7. Possible Issues:
{proposal["possible_issues"]}

{image_markdown_issue}

## Contact
- Author: {proposal["name"]}
- Email: [{proposal["mentor_email"]}](mailto:{proposal["mentor_email"]})
- GitHub: [{proposal["github_link"]}]
"""
    return markdown_template

            
def clone_github_repo(git_link, local_dir=""):
   

    if local_dir and not os.path.exists(local_dir):
        os.makedirs(local_dir)
    if local_dir:
        os.chdir(local_dir)
    try:
        subprocess.check_call(['git', 'clone', git_link])
        print(f"Repository cloned successfully in: {os.path.abspath(local_dir)}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")

def on_rm_error(func, path, exc_info):
    # Error handler for shutil.rmtree
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def clone_and_push_repo(git_link, local_dir="", new_repo_git_link="", new_branch_name="archive-update"):
    original_dir = os.getcwd()  # Save the original directory
    repo_name = git_link.split('/')[-1].replace('.git', '')  # Extract repo name from git link

    if local_dir and not os.path.exists(local_dir):
        os.makedirs(local_dir)

    repo_path = os.path.join(local_dir, repo_name)

    try:
        subprocess.check_call(['git', 'clone', git_link, repo_path])
        os.chdir(repo_path)

        # Set the remote to the target repository
        subprocess.check_call(['git', 'remote', 'add', 'upstream', new_repo_git_link])

        # Fetch the latest changes from the upstream repository
        subprocess.check_call(['git', 'fetch', 'upstream'])

        # Checkout to a new branch from the upstream main
        subprocess.check_call(['git', 'checkout', '-b', new_branch_name, 'upstream/main'])

        # Create the Archive folder and move contents into it
        archive_path = os.path.join(repo_path, 'Archive')
        if not os.path.exists(archive_path):
            os.makedirs(archive_path, exist_ok=True)
        for item in os.listdir(repo_path):
            if item not in ['Archive', '.git']:
                shutil.move(os.path.join(repo_path, item), archive_path)

        # Add and commit the changes
        subprocess.check_call(['git', 'add', '--all'])
        subprocess.check_call(['git', 'commit', '-m', 'Initial commit'])

        # Push the new branch with changes to the upstream repository
        subprocess.check_call(['git', 'push', '-u', 'upstream', new_branch_name])

        print(f"Changes pushed to new branch: {new_branch_name} in {new_repo_git_link}.")
        print(f"Please create a pull request on GitHub to merge {new_branch_name} into main.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to process repository: {e}")
    finally:
        os.chdir(original_dir)  # Change back to the original directory
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=on_rm_error)  # Use the error handler

def pending_approval_page():

    if st.session_state['proposals']:
        for index, proposal in enumerate(st.session_state['proposals']):
            proposal_markdown = format_proposal_as_markdown(proposal)
            st.markdown(proposal_markdown, unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Yes", key=f"approve_{index}"):
                    approve_proposal(index)
            with col2:
                if st.button("No", key=f"reject_{index}"):
                    reject_proposal(index)
            with col3:
                if st.button("Edit", key=f"edit_{index}"):
                    edit_proposal(index)
    else:
        st.write("No pending proposals")

def show_approved():
    df_approved = pd.DataFrame(st.session_state.approved)
    st.write(df_approved)
def show_rejected():
    df_rejected = pd.DataFrame(st.session_state.rejected)
    st.write(df_rejected)

# Function to save the uploaded Word document to the session state
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Read the file data into a bytes object
        bytes_data = uploaded_file.read()
        # Save the bytes data in the session state
        st.session_state['uploaded_word_doc'] = bytes_data
        st.session_state['uploaded_word_doc_name'] = uploaded_file.name
        st.success(f"Uploaded {uploaded_file.name} successfully.")

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


            # You can add logic to save other form fields to the session state or a database

def submit_completion(completion):
    st.session_state['completion'].append(completion)
    st.success("Project completion form submitted successfully!")

def approve_completion(index):
    completion = st.session_state['completion'].pop(index)
    st.session_state['approved_completion'].append(completion)
    st.rerun()
def edit_completion(index):
    completion = st.session_state['completion'].pop(index)
    st.session_state['edit_completion'].append(completion)
    st.rerun()
def show_approved_completion():
    df_approved = pd.DataFrame(st.session_state.approved_completion)
    st.write(df_approved)


    
def show_to_edit_completion():
    df_edit = pd.DataFrame(st.session_state.edit_completion)
    st.write(df_edit)

    for index, row in df_edit.iterrows():
        # The unique key for each button is created by appending the index to a base string
        if st.button(f"Edit {row['project title']}", key=f"button_{index}"):
            # Save the index of the proposal being edited
            st.session_state['editing_index'] = index
            # Use Streamlit's session state to display the form
            st.session_state['show_edit_form'] = True
            # Break the loop to prevent more than one form from showing
            break
    # Check if we should display the editing form
    if st.session_state.get('show_edit_form', False):
        # Obtain the index of the proposal being edited
        index = st.session_state['editing_index']
        row = df_edit.loc[index]

        with st.form(key='edit_proposal_form'):
                st.subheader("Edit Completion Form")
                project_title = st.text_input("Name",value=df_edit.loc[index,"project title"])
                video_link = st.text_input("Video Link",value=df_edit.loc[index,"Video Link"])
                github_link = st.text_input("github repo",value=df_edit.loc[index,"github repo"])
                website = st.text_input("project website",value=df_edit.loc[index,"project website"])
                # Word document upload field
                document = st.file_uploader("Upload your project document", type=['docx'])

                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    save_uploaded_file(document)
                    data_edit = {
                        "project_title": project_title,
                        "video_link": video_link,
                        "github_link": github_link,
                        "github_link": github_link,
                        "website": website,
                        "document": document.name if document is not None else "File not uploaded",
                    }
                    # Update the appropriate proposal in the session state
                    st.session_state.edit_completion[index] = data_edit
                    # Reset flags to hide the form
                    st.session_state['show_edit_form'] = False
                    st.session_state['editing_index'] = None

                    # Optionally, you can move the updated proposal back to the 'proposals' list
                    updated_proposal = st.session_state.edit_completion.pop(index)
                    st.session_state.completion.append(updated_proposal)

                    # Rerun the app to refresh the state and UI
                    st.rerun() 





def pending_completion():
    if st.session_state['completion']:
        for index, completion in enumerate(st.session_state['completion']):
            st.table(completion)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes", key=f"approve_{index}"):
                    approve_completion(index)
            with col2:
                if st.button("Edit", key=f"reject_{index}"):
                    edit_completion(index)
    else:
        st.write("No pending project completion forms")


def main():
    st.image("gw-data-science-header.jpg", use_column_width=True)
    st.title("Data Science Capstone Website")
    # git_link = 'https://github.com/mecaneer23/python-snake-game.git'
    # local_dir = 'D://Capstone Website - streamlit/Data-Science-Capstone-Website/github clones'
    # new_repo_git_link = 'https://github.com/amir-jafari/Capstone.git'
    # page = st.selectbox("Navigate to:", ["Proposal Request", "Pending Approval","Edit Proposals", "Rejected", "Approved Projects", "Project Completion Form","Project completion aprroval", "Pending Completion", "Completed Projects"], index=0)
    # Initialize active_page in session_state if not present
    if 'active_page' not in st.session_state:
        st.session_state.active_page = None

    projects_options = ["Proposal Request  ",
                        "Pending Approval  ",
                        "Edit Proposals    ",
                        "Rejected          ",
                        "Approved Projects "]
    completed_projects_options = ["Project Completion Form    ",
                                  "Project Completion Approval",
                                  "Edit Project Completion    ",
                                  "Completed Projects         "]
    # Create columns in the sidebar for Projects and Completed Projects
    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.markdown("### Projects & Proposals")

        for option in projects_options:
            if st.button(option.strip()):
                st.session_state.active_page = option.strip()

    with col2:
        st.markdown("### Completed Projects")
        for option in completed_projects_options:
            if st.button(option.strip(), key=option):  # Ensure unique keys for buttons
                st.session_state.active_page = option.strip()

# Example usage

# clone_and_push_repo(git_link, local_dir, new_repo_git_link)

    # Convert proposals to DataFrame for easier manipulation
    proposals_df = pd.DataFrame(st.session_state['approved'])


    # Collect unique values for filters
    unique_semesters = proposals_df['semester'].unique().tolist()
    unique_project_names = proposals_df['project_name'].unique().tolist()
    unique_years = proposals_df['year'].unique().tolist()

    # Sidebar filters
    selected_project_name = st.sidebar.selectbox("Filter by Project Name:", ['All'] + unique_project_names)
    selected_semester = st.sidebar.selectbox("Filter by Semester:", ['All'] + unique_semesters)
    selected_year = st.sidebar.selectbox("Filter by Year:", ['All'] + unique_years)

    # Filter proposals based on selected criteria
    filtered_proposals = proposals_df
    if selected_semester != 'All':
        filtered_proposals = filtered_proposals[filtered_proposals['semester'] == selected_semester]
    if selected_project_name != 'All':
        filtered_proposals = filtered_proposals[filtered_proposals['project_name'] == selected_project_name]
    if selected_year != 'All':
        filtered_proposals = filtered_proposals[filtered_proposals['year'] == selected_year]

    # Display content based on the active page
    if st.session_state.active_page:
        # Display the appropriate page based on the active_page
        if st.session_state.active_page == "Proposal Request":
            proposal_request_form()

        elif st.session_state.active_page == "Pending Approval":
            st.subheader("Pending Approval")
            pending_approval_page()
        elif st.session_state.active_page == "Edit Proposals":
            st.subheader("Edit Proposals")
            show_to_edit_proposals()
        elif st.session_state.active_page == "Rejected":
            st.subheader("Rejected Proposals")
            show_rejected()
        elif st.session_state.active_page == "Approved Projects":
            st.subheader("Approved Proposals")
                # Define default columns to display
            default_columns = ["name", "project_name", "mentor", "objective", "semester", "year"]
            # Define additional columns that can be added to the display
            additional_columns = ["rationale","expected_students", "github_link", "dataset","timeline","approach","possible_issues"] 

            # Use a multiselect widget to allow users to select additional columns to display
            selected_columns = st.multiselect("Select additional columns to display:", additional_columns)

            # Combine default columns with selected additional columns
            columns_to_display = default_columns + selected_columns

            st.table(filtered_proposals[columns_to_display])

        elif st.session_state.active_page == "Project Completion Form":
            completion_form()
        elif st.session_state.active_page == "Project Completion Approval":
            st.subheader("Project Completion Approval")
            pending_completion()
        elif st.session_state.active_page == "Edit Project Completion":
            st.subheader("Edit Project Completion")
            show_to_edit_completion()
        elif st.session_state.active_page == "Completed Projects":
            st.subheader("Project Completion Approval")
            show_approved_completion()
            # clone_and_push_repo(git_link, local_dir, new_repo_git_link)

    else:
        st.write("Select an option from the sidebar.")


    # if selected_project == "Proposal Request":
    #     proposal_request_form()
   
    #     # git_link = "https://github.com/Renga-99/Stroke-Prediction"  
    #     # local_dir = "D://Capstone Website - streamlit//Data-Science-Capstone-Website//github clones"  
    #     # clone_github_repo(git_link, local_dir)     

    # elif selected_project == "Pending Approval":
    #     st.subheader("Pending Approval")
    #     pending_approval_page()

    # elif selected_project == "Edit Proposals":
    #     st.subheader("Edit Proposals")
    #     show_to_edit_proposals()
   
    # elif selected_project == "Rejected":
    #     st.subheader("Rejected")
    #     show_rejected()
  
    # elif selected_project == "Approved Projects":
    #     st.subheader("Approved Projects")
        
    #     # Display filtered proposals
    #     for index, proposal in filtered_proposals.iterrows():
    #         st.write(proposal) 
    
    #     # show_approved()
    # elif selected_completed_project == "Project Completion Form":

    #     completion_form()
    #     # Display info about the uploaded file (if any)
    #     if st.session_state['uploaded_word_doc'] is not None:
    #         st.write(f"Uploaded Word document: {st.session_state['uploaded_word_doc_name']}")
    # elif selected_completed_project == "Project completion aprroval":
    #     st.subheader("Project completion aprroval")
    #     pending_completion()

    # elif selected_completed_project == "Pending Completion":
    #     st.subheader("Pending Completion")
    #     show_to_edit_completion()
  
    
    # elif selected_completed_project == "Completed Projects":
    #     st.subheader("Completed Projects")
    #     show_approved_completion()


if __name__ == "__main__":
    main()
