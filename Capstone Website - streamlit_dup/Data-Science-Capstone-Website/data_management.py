import streamlit as st
from PIL import Image
import pandas as pd
from utils import pil_image_to_base64,format_proposal_as_markdown, resize_image, generate_unique_id, entry


def initialize_session_state():
    default_values = {
        'proposals': [],
        'approved': [],
        'rejected': [],
        'completion': [],
        'approved_completion': [],
        'edit_completion': [],
        'objective_image_up': None,
        'dataset_image_up': None,
        'possible_issues_image_up': None,
        'to_edit_proposal': [],
        'editing_index': None,
        'show_edit_form': None,
        'uploaded_word_doc':None,
        'uploaded_word_doc_name' : None,
        'prof_proposal': []
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

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
    
# def edit_proposal(index, proposed_by_professor=False):
#     # Retrieve the proposal based on whether it's by a professor
#     if proposed_by_professor:
#         proposal = st.session_state['proposals'][index]
#         st.session_state['prof_proposal'].append(proposal)
#     else:
#         proposal = st.session_state['proposals'].pop(index)
#         st.session_state['to_edit_proposal'].append(proposal)
    
#     if proposed_by_professor:
#         # Directly rerun to keep the professor's proposal editable and available
#         st.experimental_rerun()
#     else:
#         st.rerun()

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


def handle_approve(index):
    if st.session_state.get(f'approve_{index}_clicked', False):
        if entry():
            approve_proposal(index)
            st.session_state[f'approve_{index}_clicked'] = False  # Reset the state

def handle_reject(index):
    if st.session_state.get(f'reject_{index}_clicked', False):
        if entry():
            reject_proposal(index)
            st.session_state[f'reject_{index}_clicked'] = False  # Reset the state

def handle_edit(index):
    if st.session_state.get(f'edit_{index}_clicked', False):
        if entry():
            edit_proposal(index)
            st.session_state[f'edit_{index}_clicked'] = False  # Reset the state
            
# def show_prof_proposals():
#     prof_df = pd.DataFrame(st.session_state.prof_proposal)
#     # matching_proposals = prof_df[prof_df['proposed_by_professor']==True]
#     # st.write(matching_proposals)
#     if not prof_df.empty:
#         for index, proposal in prof_df.iterrows():
#             with st.expander(f"Proposal {index + 1}: {proposal['name']}"):
#                 # Define columns here, inside each expander's context

#                 left_col, right_col = st.columns(2)

#                 with left_col:

#                     st.write(f"**Project Name:** {proposal['project_name']}")
#                     st.write(f"**Mentor:** {proposal['mentor']}")
#                     st.write(f"**Objective:** {proposal['objective']}")
#                     st.image(st.session_state['objective_image_up'], caption="Objective Image", use_column_width=True)
#                     st.write(f"**Rationale:** {proposal['rationale']}")
#                     st.write(f"**Dataset:** {proposal['dataset']}")
#                     st.image(st.session_state['dataset_image_up'], caption="Dataset Image", use_column_width=True)
#                     st.write(f"**Timeline:** {proposal['timeline']}")
#                     st.write(f"**Contributors:** {proposal['contributors']}")
                    

#                 with right_col:
#                     st.write(f"**Semester:** {proposal['semester']}")
#                     st.write(f"**Expected Students:** {proposal['expected_students']}")
#                     st.write(f"**Mentor Email:** {proposal['mentor_email']}")
#                     st.write(f"**Approach:** {proposal['approach']}")
#                     st.write(f"**Possible Issues:** {proposal['possible_issues']}")
#                     st.image(st.session_state['possible_issues_image_up'], caption="Possible Issues Image", use_column_width=True)
#                     st.write(f"**GitHub Link:** {proposal['github_link']}")
#                     st.write(f"**Year:** {proposal['year']}")
                
#                 if st.button("Edit", key=f"edit_{index}"):
#                     st.session_state['editing_index'] = index
#                     st.session_state['show_edit_form'] = True
#                     break  # Exit the loop to only process one form at a time


#         # Check if we should display the editing form
#         if st.session_state.get('show_edit_form', False):
#             # Obtain the index of the proposal being edited

#             with st.form(key='edit_proposal_form'):                
#                     st.subheader("Edit Proposal Request Form")
#                     left_col, right_col = st.columns(2)
                    
#                     with left_col:
#                         # proposal_id = prof_df.loc[index,"proposal_id"]
#                         name = st.text_input("Name",value=prof_df.loc[index,"name"])
#                         project_name = st.text_input("Project Name",value=prof_df.loc[index,"project_name"])
#                         mentor = st.text_input("Mentor for the project",value=prof_df.loc[index,"mentor"])
#                         github_link = st.text_input("Github Link",value=prof_df.loc[index,"github_link"])
#                         objective = st.text_area("Objective",value=prof_df.loc[index,"objective"])
#                         rationale = st.text_area("Rationale",value=prof_df.loc[index,"rationale"])
#                         timeline = st.text_area("Timeline",value=prof_df.loc[index,"timeline"])
#                         contributors = st.text_input("Contributors",value=prof_df.loc[index,"contributors"])

#                     with right_col:
#                         semester = st.selectbox("Semester", options=["Spring", "Summer", "Fall"])
#                         expected_students = st.number_input("Expected number of students",value=prof_df.loc[index,"expected_students"])
#                         mentor_email = st.text_input("Mentor email",value=prof_df.loc[index,"mentor_email"])
#                         dataset = st.text_area("Dataset",value=prof_df.loc[index,"dataset"])
#                         approach = st.text_area("Approach",value=prof_df.loc[index,"approach"])
#                         possible_issues = st.text_area("Possible Issues",value=prof_df.loc[index,"possible_issues"])
#                         year = st.selectbox("Year", options=["2021", "2022", "2023", "2024"])

#                     submitted = st.form_submit_button("Submit")
#                     if submitted:
#                         proposal_id = generate_unique_id()
#                         proposal_data_edit = {
#                             "name": name,
#                             "project_name": project_name,
#                             "mentor": mentor,
#                             "github_link": github_link,
#                             "objective": objective,
#                             "rationale": rationale,
#                             "timeline": timeline,
#                             "contributors": contributors,
#                             "semester": semester,
#                             "expected_students": expected_students,
#                             "mentor_email": mentor_email,
#                             "dataset": dataset,
#                             "approach": approach,
#                             "possible_issues": possible_issues,
#                             "year": year,
#                             "project_id": proposal_id,
#                             "proposed_by_professor": False 
#                         }
#                         st.info(f"Note your new Project id{proposal_id}")
#                         # Update the appropriate proposal in the session state
#                         st.session_state.to_edit_proposal[index] = proposal_data_edit
#                         # Reset flags to hide the form
#                         st.session_state['show_edit_form'] = False
#                         st.session_state['editing_index'] = None

#                         # Optionally, you can move the updated proposal back to the 'proposals' list
                    
#                         st.session_state.proposals.append(st.session_state.to_edit_proposal)
                        
#                         # Rerun the app to refresh the state and UI
#                         st.rerun() 


    
def show_to_edit_proposals():
    proposal_id_to_edit = st.text_input("Enter the Proposal ID to edit:")
    # Convert DataFrame for easier ID checking
    df_edit = pd.DataFrame(st.session_state.to_edit_proposal)

    if proposal_id_to_edit:

        # Check if the entered ID matches any proposal ID
        matching_proposals = df_edit[df_edit['proposal_id'] == proposal_id_to_edit]

        if not matching_proposals.empty:
                    
            for index, proposal in df_edit.iterrows():
                    with st.expander(f"Proposal {index + 1}: {proposal['name']}"):
                        # Define columns here, inside each expander's context

                        left_col, right_col = st.columns(2)

                        with left_col:
                            st.write(f"**Project ID:** {proposal['proposal_id']}")
                            st.write(f"**Project Name:** {proposal['project_name']}")
                            st.write(f"**Mentor:** {proposal['mentor']}")
                            st.write(f"**Objective:** {proposal['objective']}")
                            st.image(st.session_state['objective_image_up'], caption="Objective Image", use_column_width=True)
                            st.write(f"**Rationale:** {proposal['rationale']}")
                            st.write(f"**Dataset:** {proposal['dataset']}")
                            st.image(st.session_state['dataset_image_up'], caption="Dataset Image", use_column_width=True)
                            st.write(f"**Timeline:** {proposal['timeline']}")
                            st.write(f"**Contributors:** {proposal['contributors']}")
                            

                        with right_col:
                            st.write(f"**Semester:** {proposal['semester']}")
                            st.write(f"**Expected Students:** {proposal['expected_students']}")
                            st.write(f"**Mentor Email:** {proposal['mentor_email']}")
                            st.write(f"**Approach:** {proposal['approach']}")
                            st.write(f"**Possible Issues:** {proposal['possible_issues']}")
                            st.image(st.session_state['possible_issues_image_up'], caption="Possible Issues Image", use_column_width=True)
                            st.write(f"**GitHub Link:** {proposal['github_link']}")
                            st.write(f"**Year:** {proposal['year']}")
                        
                        if st.button("Edit", key=f"edit_{index}"):
                            st.session_state['editing_index'] = index
                            st.session_state['show_edit_form'] = True
                            break  # Exit the loop to only process one form at a time

            # Check if we should display the editing form
            if st.session_state.get('show_edit_form', False):
                # Obtain the index of the proposal being edited
                index = st.session_state['editing_index']
                row = df_edit.loc[index]

                with st.form(key='edit_proposal_form'):                
                        st.subheader("Edit Proposal Request Form")
                        left_col, right_col = st.columns(2)

                        with left_col:
                            proposal_id = df_edit.loc[index,"proposal_id"]
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
                                "project_id": proposal_id
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

        else:
            st.write("No matching proposal found for the entered ID.")


def show_to_edit_completion():
    df_edit = pd.DataFrame(st.session_state.edit_completion)
    for index, proposal in df_edit.iterrows():
        with st.expander(f"Proposal {index + 1}: {proposal['project title']}"):
            # Define columns here, inside each expander's context
            st.write(f"**project title:** {proposal['project title']}")
            st.write(f"**Video Link** {proposal['Video Link']}")
            st.write(f"**github repo:** {proposal['github repo']}")
            st.write(f"**project website:** {proposal['project website']}")

            if st.button("Edit", key=f"edit_{index}"):
                st.session_state['editing_index'] = index
                st.session_state['show_edit_form'] = True
                break  # Exit the loop to only process one form at a time
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


def save_uploaded_images(objective_file, dataset_file, possible_issues_file):
    if objective_file is not None:
        st.session_state.objective_image_up = objective_file.getvalue()
    if dataset_file is not None:
        st.session_state.dataset_image_up = dataset_file.getvalue()
    if possible_issues_file is not None:
        st.session_state.possible_issues_image_up = possible_issues_file.getvalue()



def get_image_display_code(image_data):
    base64_img = pil_image_to_base64(image_data)
    return f"![image](data:image/png;base64,{base64_img})"

# Function to save the uploaded Word document to the session state
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Read the file data into a bytes object
        bytes_data = uploaded_file.read()
        # Save the bytes data in the session state
        st.session_state['uploaded_word_doc'] = bytes_data
        st.session_state['uploaded_word_doc_name'] = uploaded_file.name
        st.success(f"Uploaded {uploaded_file.name} successfully.")


