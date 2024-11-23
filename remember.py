
buffer=""     
with st.expander(label="Options de telechargement") as exp:
    choix=st.radio("Formats:",("pdf","docx","pptx"))
    if choix=="pdf":
        st.download_button(
        label="Telecharger",
        data=download_pdf(st.session_state['response_model']),
        file_name="document.pdf",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    elif choix=="docx":
        with open("markdown_content.md","w") as file:
            file.write(st.session_state['response_model'])
        convert_markdown_to_docx("markdown_content.md","document.docx")
        with open("document.docx","rb") as file:
            buffer=file.read()
        st.download_button(
            label="Telecharger",
            data=buffer,
            file_name="Document.docx"
        )
    
    else:
        with open("markdown_content2.md","w") as file:
            file.write(st.session_state['response_model'])
        convert_markdown_to_pptx_using_template("markdown_content2.md","document99.pptx","template.pptx")
        with open("document99.pptx","rb") as file:
            buffer=file.read()
        st.download_button(
            label="Telecharger",
            data=buffer,
            file_name="Document14.pptx"
        )