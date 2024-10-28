import streamlit as st
import openai
from Functions_.retrieve_content import retrieve_content_file_uploaded
from Functions_.formatting_function import summary_layout


path = "Functions_/folderM/o"
try:
    with open(path, mode="r") as file:
        key=file.read()
except FileNotFoundError:
    print("File not found at the specified path.")
except Exception as e:
    print(f"An error occurred: {e}")
#---->
openai.api_key =key


#declaration of variables
file_content = ""
if "checkFormattingButton"  not in st.session_state:
    st.session_state['checkFormattingButton']=False

if "summary" not in st.session_state:
    st.session_state['summary']=""

instructions=''

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

file_uploaded = st.file_uploader("Televerser votre fichier ", type=["pdf", "docx", "pptx"])
minimum = st.slider(label="Minimum length of the summary", min_value=10, max_value=514)
maximum = st.slider(label="Maximum length of the summary", min_value=10, max_value=514)

#Text to summarize
file_content=retrieve_content_file_uploaded(file_uploaded)
#Instructions to the model
user_message = f"""
Below provided are some notes. Read through the notes, understand key takeaways, and summarize the meeting notes. 
Follow below instructions when responding:

Model Instructions:
- DO NOT make up or hallucinate any other information apart from the information given below.
- You MUST give the response in French.
-You should do the summary of the text provided
-The summary MUST contains beetwen {minimum} and {maximum} words
-At the end of the summary, mention the number of words of the summary
-Underline the keys words 
Text: {file_content}
"""



if st.button("Afficher le resumé :"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            max_tokens=512,
            temperature=0.7
        )

        # Extract response text
        response_text = response.choices[0].message['content']
        st.session_state['summary']=response_text
        st.session_state['checkFormattingButton']=True

    except Exception as e:
        print(f"ERROR: {e}")



#Handle the click button 
if st.session_state['checkFormattingButton'] is True:
    instructions=st.text_area(label='Enter your instructions:')
    if st.button('Formatting'):
        st.session_state['summary']=summary_layout(st.session_state['summary'],instructions)
        
#Display the summary
summary=st.session_state['summary']
st.markdown(summary,unsafe_allow_html=True) 


       
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by Ezekiel</p>", unsafe_allow_html=True)
