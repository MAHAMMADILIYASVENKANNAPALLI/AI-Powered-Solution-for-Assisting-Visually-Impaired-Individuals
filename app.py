import streamlit as st
import google.generativeai as ai
from PIL import Image
import pyttsx3

#------------------------------------------------------------------------------------------------------
# Google API Key Configuration
KEY = "AIzaSyBrbSrS4hpKVUk70O0B7KcUNi9d1oY7Jbw"
ai.configure(api_key=KEY)

#------------------------------------------------------------------------------------------------------
# Apply background color to the entire page and customize the UI elements
st.markdown(
    """
    <style>
        /* Apply background color to the entire page */
        body {
            background-color: #87CEEB; /* Sky blue color */
            color: #333;
            font-family: 'Arial', sans-serif;
        }

        /* Style the main container */
        .main {
            background-color: #87CEEB; /* Sky blue for main container */
            padding: 20px;
            border-radius: 10px;
        }

        /* Customize text input and text area boxes */
        .stTextInput, .stTextArea, .stButton > button {
            background-color: #ffffff; /* White background for input boxes */
            color: #333;
            border-radius: 10px;
            padding: 10px;
        }

        /* Button hover effect */
        .stButton > button:hover {
            background-color: #1E90FF; /* Dodger Blue hover effect */
            color: white;
        }

        /* Style the sidebar with a blue background */
        .css-1d391kg {
            background-color: #4682B4 !important;  /* Steel blue for sidebar */
        }

        /* Sidebar text color */
        .css-1d391kg .sidebar .sidebar-content {
            color: white !important;
        }

        /* Sidebar heading text */
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg p {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#------------------------------------------------------------------------------------------------------
# Page Title with Emoji
st.title("✨ AI-Powered Solution for Assisting Visually Impaired Individuals ✨")

#------------------------------------------------------------------------------------------------------
with st.sidebar:
    st.title("✨ AI-Powered Solution for Assisting Visually Impaired Individuals ✨")

    # Add image to the sidebar
    st.image("D:/images/lifeTree.jpg", caption="AI-powered assistance 🌳", use_column_width=True)

    st.write("""
    🌟 **Real-Time Scene Understanding**  
       Gain a detailed understanding of your surroundings! This feature uses advanced AI to analyze the uploaded image and provide a clear and accurate description of the scene, helping you visualize and comprehend what’s around you. 🌏
    """)
    
    st.write("""
    🔊 **Text-to-Speech Conversion for Visual Content**  
       Make text in images come alive! By extracting text from the uploaded image using Optical Character Recognition (OCR), this feature reads it aloud in real-time, ensuring you can easily access visual content without needing to read it manually. 📝🎙️
    """)
    
    st.write("""
    🧑‍🍳 **Personalized Assistance for Daily Tasks**  
       Get tailored guidance for your daily activities! From identifying items in the image to reading labels and categorizing objects (like groceries or books), this feature provides actionable suggestions and task-specific help to make your routine easier. 🏡📚
    """)

#------------------------------------------------------------------------------------------------------
# Define the prompts for each feature
real_time_prompt = "Describe the scene in the uploaded image in detail, including key elements, activities, or objects present in the environment."
text_to_speech_prompt = """
    Extract any visible text from the uploaded image.
    If possible, provide details about the text's context, such as its purpose or location within the image.
    Prepare the text for conversion into audible speech.
"""
personalized_assistance_prompt = """
    Based on the uploaded image:
    1. Identify and list the objects in the image.
    2. If any text or labels are visible, read and interpret them.
    3. Provide actionable guidance or suggestions related to the identified objects (e.g., using a device, preparing food, organizing books, etc.).
    4. Categorize the items and explain their possible uses or contexts.
"""

#------------------------------------------------------------------------------------------------------
# Multi-select options with Emojis
options = st.multiselect(
    "Choose an option ✨",
    ["Real-Time Scene Understanding 🌍", "Text-to-Speech Conversion for Visual Content 🔊", 
     "Personalized Assistance for Daily Tasks 🧑‍🍳"]
)

# Store selected options in session state
st.session_state.selected_options = options

# Display the selected options or a warning if no option is selected
if options:
    st.write("You selected:", options)
else:
    st.warning("Please select at least one option to proceed. 🚨")

#------------------------------------------------------------------------------------------------------
# AI model configuration
model = ai.GenerativeModel(model_name="models/gemini-1.5-flash")

#------------------------------------------------------------------------------------------------------
# File uploader
uploaded_file = st.file_uploader("Upload an image 📸", type=["jpg", "png", "jpeg"])

#------------------------------------------------------------------------------------------------------
# Text-to-Speech Function
def text_to_speech(text):
    """
    Convert the provided text to audible speech.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Adjust speaking rate (optional)
    engine.setProperty("volume", 0.9)  # Adjust volume (optional)
    engine.say(text)
    engine.runAndWait()

#------------------------------------------------------------------------------------------------------
# Generate response function for AI model
def generate_response(uploaded_file, prompt, feature_name):
    """
    Generates a response for the uploaded image based on the provided prompt and feature name.
    """
    if uploaded_file:
        # Load and display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Uploaded Image for {feature_name} 🖼️", use_column_width=True)

        # Generate the AI response for the image
        try:
            response = model.generate_content([image, prompt])
            return response.text
        except Exception as e:
            st.error(f"Error generating response for {feature_name}: {str(e)}")
    else:
        st.warning(f"Please upload an image to proceed with {feature_name}.")

#------------------------------------------------------------------------------------------------------
# Handle text-to-speech conversion
def handle_text_to_speech(uploaded_file, prompt):
    """
    Handle the text-to-speech feature by extracting text and converting it to speech.
    """
    if uploaded_file:
        # Generate AI response
        response_text = generate_response(uploaded_file, prompt, "Text-to-Speech Conversion")
        
        if response_text:
            st.write(response_text)  # Display the text for user reference
            st.success("Playing the extracted text as speech... 🎧")
            text_to_speech(response_text)  # Convert and play speech
    else:
        st.warning("Please upload an image to proceed. 📸")

#------------------------------------------------------------------------------------------------------
# Handle personalized assistance (without speech)
def handle_personalized_assistance(uploaded_file, prompt):
    """
    Handle the personalized assistance feature by identifying objects and providing actionable guidance.
    """
    if uploaded_file:
        # Generate AI response
        response_text = generate_response(uploaded_file, prompt, "Personalized Assistance for Daily Tasks")
        
        if response_text:
            st.write(response_text)  # Display the text for user reference
    else:
        st.warning("Please upload an image to proceed. 📸")

#------------------------------------------------------------------------------------------------------
# Handle scene understanding (without speech)
def handle_real_time_scene_understanding(uploaded_file, prompt):
    """
    Handle the real-time scene understanding feature by describing the scene in the uploaded image.
    """
    if uploaded_file:
        # Generate AI response
        response_text = generate_response(uploaded_file, prompt, "Real-Time Scene Understanding")
        
        if response_text:
            st.write(response_text)  # Display the text for user reference
    else:
        st.warning("Please upload an image to proceed. 📸")

#------------------------------------------------------------------------------------------------------
# Main functionality based on user selection
if "Real-Time Scene Understanding 🌍" in st.session_state.selected_options:
    handle_real_time_scene_understanding(uploaded_file, real_time_prompt)

if "Text-to-Speech Conversion for Visual Content 🔊" in st.session_state.selected_options:
    handle_text_to_speech(uploaded_file, text_to_speech_prompt)

if "Personalized Assistance for Daily Tasks 🧑‍🍳" in st.session_state.selected_options:
    handle_personalized_assistance(uploaded_file, personalized_assistance_prompt) 
