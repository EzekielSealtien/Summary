import streamlit as st
import boto3
from botocore.exceptions import ClientError
from Functions.read_functions import lire_docx,lire_pdf,lire_ppt

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

fichier_telecharge = st.file_uploader("", type=["pdf", "docx", "pptx"])

file_content = ""

if fichier_telecharge is not None:
    extension_fichier = fichier_telecharge.name.split('.')[-1].lower()

    if extension_fichier in ["pdf", "docx", "pptx"]:
        st.markdown("---")
                
        if extension_fichier == "pdf":
            file_content = lire_pdf(fichier_telecharge)
        elif extension_fichier == "docx":
            file_content = lire_docx(fichier_telecharge)
        elif extension_fichier == "pptx":
            file_content = lire_ppt(fichier_telecharge)
            
    else:
        st.markdown("---")
        st.error("⚠️ Seuls les fichiers PDF, DOCX, et PPTX sont acceptés.")


minimum = st.slider(label="Minimum length of the summary", min_value=10, max_value=514)
maximum = st.slider(label="Maximum length of the summary", min_value=10, max_value=514)

# Placeholder for the button to trigger the summarization
if st.button("Afficher le resumé :"):

    # Initialize Amazon Bedrock client
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.titan-text-premier-v1:0"

    # Construct the conversation
    user_message = f"""Below provided are some notes. Read through the notes, understand key take aways and summarize the meeting notes. 
    Follow below instructions when responding:

    Model Instructions:
    - You MUST Keep the response beetwen {minimum} and {maximum} words. 
    - DO NOT make up or hallucinate any other information apart from the information given below. 
    -You MUST give the response in french
    -Lorsque vous répondrez, donnez à la fin le nombre de mots du  résumé que tu as produit

    Notes:{file_content}


    Now, summarize the meeting notes above, following the provided instructions above."""
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]
    
    try:
        # Send the message to the model, using a basic inference configuration(real-time inference)
        response = client.converse(
            modelId="amazon.titan-text-premier-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":512,"stopSequences":[],"temperature":0.7,"topP":0.9},
            additionalModelRequestFields={}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        st.write(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)




st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made by Ezekiel</p>", unsafe_allow_html=True)
