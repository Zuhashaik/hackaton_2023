import streamlit as st

# Define the function to redirect to Page 1
def page1():
    st.write("Text detection is like a treasure hunt in images. It's the process of finding hidden words and turning them into searchable data.")
    
# Define the function to redirect to Page 2
def page2():
    st.write("Spot the human: Person detection for a safer world")
    
# Define the function to redirect to Page 3
def page3():
    st.write("Discover hidden secrets in your surroundings with cutting-edge surroundings detection technology")

# Set up the layout of the UI with 3 containers
st.set_page_config(page_title="Hackathon", page_icon=":smiley:", layout="wide")
col1, col2, col3 = st.columns(3)

# Add a button to the first container that redirects to Page 1
with col1:
    st.write("Text Detection in Image")
    if st.button("Try TDI"):
        st.session_state.page = "page1"

# Add a button to the second container that redirects to Page 2
with col2:
    st.write("Person Detection")
    if st.button("Try PD"):
        st.session_state.page = "page2"

# Add a button to the third container that redirects to Page 3
with col3:
    st.write("Surroundings Detection")
    if st.button("Try SD"):
        st.session_state.page = "page3"
    
# Check which page to show based on the button clicked
if "page" in st.session_state:
    if st.session_state.page == "page1":
        page1()
        
    elif st.session_state.page == "page2":
        page2()
        
    elif st.session_state.page == "page3":
        page3()
        
else:
    st.write("Welcome to the Main Page!")
