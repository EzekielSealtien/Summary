import streamlit as st
from streamlit_quill import st_quill as stq
from Functions_.retrieve_content import retrieve_content_file_uploaded
from Functions_.response import responseModel, responseModelInitial
from Functions_.display_text_editor import display_text_editor
#from Functions_.downloadFunctions import convert_markdown_to_docx,download_pdf,convert_markdown_to_pptx_using_template
# Declaration of session state variables
if "file_content" not in st.session_state:
    st.session_state.file_content = ""
if "checkFormattingButton" not in st.session_state:
    st.session_state['checkFormattingButton'] = False
if "response_model" not in st.session_state:
    st.session_state['response_model'] = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

instructions = ''
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d0f0c0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 Uploader et Afficher le Contenu de votre Fichier</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>Sélectionnez un fichier pour afficher son contenu</h4>", unsafe_allow_html=True)

# File uploader and text input
file_uploaded = st.file_uploader("Téléverser votre fichier (Votre fichier ne doit pas dépasser 1MB)", type=["pdf", "docx", "pptx"])
st.write("Ou saisissez votre texte:")

# Display text editor only if "Afficher le résumé" has not been clicked

display_text_editor()
# Text processing for uploaded file
if file_uploaded is not None:
    if file_uploaded.size > 1 * 1024 * 1024:  # 1MB limit
        st.error("Le fichier dépasse la limite de 1MB. Veuillez téléverser un fichier plus petit.")
    else:
        if not st.session_state['checkFormattingButton']:
            st.session_state.file_content = retrieve_content_file_uploaded(file_uploaded)
# Sidebar for model selection
model_choice = ""
with st.sidebar:
    st.header("Modèle AI")
    model_choice = st.selectbox(
        "Choisissez un modèle :",
        ("gpt-3.5-turbo", "gpt-4")
    )
# Radio button for summary detail level
summaryLevel = st.radio(
    "Choisissez le niveau de détail du résumé :",
    ("Complet", "Abrégé")
)
# Radio button for the language of the summay
language = st.radio(
    "Choisissez la langue :",
    ("Francais", "Anglais","Espagnol","Grec")
)
parameters = [model_choice, summaryLevel,language]
# Generate the summary and hide stq editor
if st.button("Afficher le résumé :"):
    st.session_state['response_model'] = responseModelInitial(st.session_state.file_content, parameters)
    st.session_state['checkFormattingButton'] = True  # This hides the stq editor
    st.rerun()  # Rerun the script to immediately update the view
  
# Display the response summary after formatting
st.write(st.session_state['response_model'], unsafe_allow_html=True)
     
# Handle formatting instructions
if st.session_state['checkFormattingButton']:
    instructions = st.text_area(label='Entrez vos instructions :')
    if st.button('Formatage'):
        st.session_state['response_model'] = responseModel(st.session_state['response_model'], instructions, parameters)
        st.rerun()  

     
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by RAD team</p>", unsafe_allow_html=True)
