import streamlit as st
import random
from auth import login, signup
  # adjust if your function is in another file
# Initialize login state once per session

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔥 Resume Roasted")
    st.subheader("Welcome!")

    choice = st.radio(
        "Choose an option",
        ["Sign In", "Sign Up"],
        horizontal=True
    )

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(choice):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            try:
                if choice == "Sign Up":
                    result = signup(email, password)
                    st.success("Account created successfully! You can now sign in.")

                else:
                    result = login(email, password)
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.success("Login successful!")
                    st.rerun()

            except Exception as e:
                st.error(f"{choice} failed: {e}")

    st.stop()


# YOUR MAIN PAGE CODE STARTS BELOW THIS LINE
st.title("Your main page")


# Only logged-in users should reach this section.
st.title("Resume Roasted Dashboard")
# --- CONFIGURATION (Keep this standard line at the top) ---
st.set_page_config(page_title="Resume Roaster", page_icon="🔥")


# --- OUR FUNCTIONS ---

def get_roast_message():
    """Returns a random funny roast from our list"""
    roasts = [
        "This resume looks like a grocery receipt but with less substance.",
        "Listing 'Microsoft Word' as a core skill? What is this, 2012?",
        "Your formatting looks like a broken textbook. Please find a template.",
        "You listed 15 skills but your experience section is completely empty.",
        "Are you a 'motivated self-starter'? Groundbreaking. Truly original.",
        "Too much empty space here. It looks like you gave up halfway through writing it."
    ]
    # Pick a random item from our list
    random_index = random.randint(0, len(roasts) - 1)
    return roasts[random_index]


def check_resume_for_skills(resume_text, required_skills):
    """
    Loops through the required skills and checks if they are in the resume.
    Returns two lists: skills found, and skills missing.
    """
    # Convert everything to lowercase so capitalization doesn't break our search
    lower_resume = resume_text.lower()
    
    found_list = []
    missing_list = []
    
    # Standard for loop to check each skill one by one
    for skill in required_skills:
        if skill in lower_resume:
            found_list.append(skill)
        else:
            missing_list.append(skill)
            
    return found_list, missing_list


# --- MAIN INTERFACE CODE ---

st.title("🔥 The Resume Roaster & Skill Gap Finder")
st.write("Built by students, for students. Drop your resume below to get roasted.")

st.subheader("1. What job are you applying for?")
role_choice = st.selectbox(
    "Choose a track:",
    ["Software Engineer", "Data Scientist", "Frontend Developer"]
)

# Set up the skill lists based on what role they selected using basic if/else
if role_choice == "Software Engineer":
    skills_to_look_for = ["python", "java", "data structures", "algorithms", "git", "sql"]
    resource_1 = "Data Structures: Try NeetCode.io or LeetCode"
    resource_2 = "Git & Version Control: Try the Git Immersion website"
    
elif role_choice == "Data Scientist":
    skills_to_look_for = ["python", "pandas", "machine learning", "statistics", "sql", "tableau"]
    resource_1 = "Machine Learning: Watch StatQuest on YouTube"
    resource_2 = "Pandas: Try the free Kaggle Learn courses"
    
else:  # Frontend Developer
    skills_to_look_for = ["javascript", "react", "html", "css", "tailwind", "typescript"]
    resource_1 = "React Framework: Use the official Next.js dashboard"
    resource_2 = "CSS Layouts: Watch Kevin Powell tutorials on YouTube"


st.subheader("2. Paste your Resume text")
user_resume = st.text_area("Copy and paste all the words from your resume here:", height=200)

# Create the submission button
submit_button = st.button("Roast My Resume! 🚀")

# Check if the button was clicked
if submit_button:
    # Check if they actually pasted something
    if user_resume == "":
        st.warning("Please paste some text first! We can't roast a blank page.")
    else:
        st.header("💀 The Roast")
        
        # Get two random roasts using our function
        first_roast = get_roast_message()
        second_roast = get_roast_message()
        
        # Display the roasts in warning boxes to make them look highlighted
        st.error(first_roast)
        st.error(second_roast)
        
        st.header("📊 Skill Gap Analysis")
        
        # Call our processing function
        skills_pasted, skills_missing = check_resume_for_skills(user_resume, skills_to_look_for)
        
        # Use columns to show found vs missing skills side-by-side
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("✅ What you have:")
            if len(skills_pasted) == 0:
                st.write("Nothing found. Yikes.")
            else:
                for s in skills_pasted:
                    st.write("- " + s.upper())
                    
        with col2:
            st.subheader("❌ Missing Skills:")
            if len(skills_missing) == 0:
                st.write("Wow! No missing skills.")
            else:
                for s in skills_missing:
                    st.write("- " + s.upper())
                    
        # Calculate a basic score using math equations
        total_skills = len(skills_to_look_for)
        skills_had_count = len(skills_pasted)
        score = int((skills_had_count / total_skills) * 100)
        
        st.subheader("📈 Estimated ATS Score")
        st.info("Your resume matches " + str(score) + "% of the core skills for this role.")
        
        # --- ROADMAP STUDY RECOMMENDATIONS ---
        st.header("🛠️ Recommended Learning Path")
        st.write("To fix the gaps we found, study these topics:")
        st.success(resource_1)
        st.success(resource_2)
        
        # Pop up some celebration balloons for completion
        st.balloons()
