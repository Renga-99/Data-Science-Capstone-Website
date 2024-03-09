from PIL import Image
import io
import base64
import streamlit as st
import subprocess
import os
import shutil
import uuid

local_dir = r"D:/Capstone Website - streamlit_dup/Data-Science-Capstone-Website/github clones"
target_repo_url = "https://github.com/Renga-99/Data-Science-Capstone-Website.git"
# Function to convert PIL image to Base64
def pil_image_to_base64(image):
    img_buffer = io.BytesIO()
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

def format_completion_as_markdown(completion):

    markdown_template = f"""
# George Washington University  
## Data Science Program
### Capstone Final Completion
#### Project Title: {completion["project title"]}
#### Video Link: {completion["Video Link"]}
#### Github Link: {completion["github repo"]}
#### Project Website: {completion["project website"]}  
#### Document uploaded name: {completion["Project Document"]}


"""
    return markdown_template

def archive_source_repo_into_target(source_repo_url, target_repo_url, local_clone_path, archive_dir_name="Archive"):
    # Define paths for the local clones
    source_repo_dir = os.path.join(local_clone_path, "source_repo")
    target_repo_dir = os.path.join(local_clone_path, "target_repo")

    # Clone the source repository
    subprocess.run(["git", "clone", source_repo_url, source_repo_dir], check=True)

    # Clone the target repository if it hasn't been cloned already
    if not os.path.exists(target_repo_dir):
        subprocess.run(["git", "clone", target_repo_url, target_repo_dir], check=True)

    # Create the Archive directory in the target repo if it doesn't exist
    archive_path = os.path.join(target_repo_dir, archive_dir_name)
    os.makedirs(archive_path, exist_ok=True)

    # Copy the contents from the source repo to the Archive directory in the target repo
    for item in os.listdir(source_repo_dir):
        if item != ".git":  # Ignore the .git directory
            src_path = os.path.join(source_repo_dir, item)
            dst_path = os.path.join(archive_path, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

    # Change to the target repo directory for Git operations
    os.chdir(target_repo_dir)
    
    # Git add, commit, and push changes
    subprocess.run(["git", "add", "."], check=True)
    commit_message = "Archived content from source repository"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

    # Clean up: remove the local clone of the source repository
    shutil.rmtree(source_repo_dir, ignore_errors=True)

def generate_unique_id():
    # Generate a random UUID
    unique_id = uuid.uuid4()
    return str(unique_id)


def entry():
    if 'password_correct' not in st.session_state:
        st.session_state['password_correct'] = False

    if st.session_state['password_correct']:
        return True
    
    enter_pass = st.text_input("Enter the Password to proceed:", key="password_entry")

    if enter_pass:
        if enter_pass == "root":
            st.session_state['password_correct'] = True
            st.experimental_rerun()
            return True
        else:
            st.session_state['password_correct'] = False
            st.error("Incorrect password.")
    return False