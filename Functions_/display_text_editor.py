import streamlit as st
from streamlit_quill import st_quill as stq
# Display text editor only if "Afficher le résumé" has not been clicked
def display_text_editor():
    if not st.session_state['checkFormattingButton']:
        st.session_state.file_content = stq(value=st.session_state['response_model'], placeholder="Type here")
