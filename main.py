import streamlit as st
import openai
from langchain_core.messages import AIMessage, HumanMessage
from Functions_.retrieve_content import retrieve_content_file_uploaded
from Functions_.response import responseModel,responseModelInitial


# Load API key
path = "Functions_/folderM/o"
try:
    with open(path, mode="r") as file:
        key = file.read()
except FileNotFoundError:
    print("File not found at the specified path.")
except Exception as e:
    print(f"An error occurred: {e}")

openai.api_key = key

# Declaration of variables
file_content = ""
if "checkFormattingButton" not in st.session_state:
    st.session_state['checkFormattingButton'] = False

if "response_model" not in st.session_state:
    st.session_state['response_model'] = ""
if "history" not in st.session_state:
    st.session_state.history = [
        AIMessage(content=""),
    ]
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

instructions = ''

# Streamlit UI setup
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

file_uploaded = st.file_uploader("Téléverser votre fichier ", type=["pdf", "docx", "pptx"])

# Text to summarize
file_content = retrieve_content_file_uploaded(file_uploaded)

# Dropdown list (selectbox) pour choisir le modèle
model_choice=""
with st.sidebar:
    st.header("Modèle AI")
    model_choice = st.selectbox(
        "Choisissez un modèle :",
        ("gpt-4o", "gpt-4", "gpt-3.5-turbo","gpt-3.5","gpt-3")
    )


# Radio button pour choisir le niveau de detail du resumé
summaryLevel = st.radio(
    "Choisissez le niveau de detail du resumé :",
    ("Complet", "Abrege")
)
parameters=[model_choice,summaryLevel]
if st.button("Afficher le résumé :"):
    st.session_state['response_model'] = responseModelInitial(file_content,parameters)
    st.session_state['checkFormattingButton'] = True



# Handle the formatting button
if st.session_state['checkFormattingButton'] is True:
    instructions = st.text_area(label='Enter your instructions:')
    if st.button('Formatting'):
        st.session_state['response_model'] = responseModel(st.session_state['response_model'], instructions,parameters)

# Display the summary
st.write(st.session_state['response_model'], unsafe_allow_html=True)


st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by RAD team</p>", unsafe_allow_html=True)
