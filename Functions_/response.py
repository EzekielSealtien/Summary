import openai
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage


def responseModel(text, instructions,parameters):

    openai.api_key = "sk-GJPAXciZeshLqhrHRifEcTbiotKbcUzsrlMaqx82nXT3BlbkFJRmjfcg1nfcu1rlnKvyPH9l7j9q9DYhAT9rdBBu5F0A"
    
    model_choice=parameters[0]
    summaryLevel=parameters[1]
    if not instructions:
        instructions = "DO NOT MODIFY ANYTHING. Generate the same text provided."

        # Construct the user query with limited history
    user_query = f"""
    Please format the following text according to the provided instructions using HTML tags and inline CSS where necessary. 

    Formatting Instructions:
    - Apply the specified formatting by framing only the requested text with HTML tags, without altering the overall content.
    - Use basic HTML/CSS tags, like `<b>`, `<i>`, `<u>`, and `<span style="color: red;">text</span>`, as needed.
    - Use non-breaking spaces (`&nbsp;`) to control spacing when specified.
    - Only apply formatting instructions, and do not output raw HTML code unless specified.

    Additional Instructions:
    {instructions}

    Here is the text to format:
    {text}
    """

    try:
        response = openai.ChatCompletion.create(
            model=model_choice,
            messages=[
                {"role": "user", "content": user_query}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # Extract response text
        response_text = response.choices[0].message['content']
        st.session_state.user_input = user_query
        return response_text

    except Exception as e:
        a = f"ERROR: {e}"
        return a



def responseModelInitial(text,parameters):

    openai.api_key = "sk-GJPAXciZeshLqhrHRifEcTbiotKbcUzsrlMaqx82nXT3BlbkFJRmjfcg1nfcu1rlnKvyPH9l7j9q9DYhAT9rdBBu5F0A"

    model_choice=parameters[0]
    summaryLevel=parameters[1]
    user_query = f"""
    Below is a text that may or may not contain multiple sections with titles such as "Introduction," "Conclusion," etc. Please follow these instructions carefully when summarizing:

    Instructions:
    - First, check if the text contains section titles (e.g., "Introduction," "Conclusion",tec) or subtitles. 
    - If titles or subtitles are present, do not modify or remove these titles. Instead, summarize the content within each section individually, keeping each summary concise.
    - If no titles or subtitles are detected, summarize the entire text as a single cohesive summary.
    - Maintain Markdown formatting in the final output.
    -Check the summary level specified:
        - If the summary level is "abrege", provide an abbreviated summary that covers only the main points in a concise manner.
        - If the summary level is "complet", provide a comprehensive summary that includes all key details from the text.
        - Ensure that the summary is coherent and maintains the context of the original text.
        Summary Level: {summaryLevel}

    - Only summarize the content without adding or modifying any additional information.
    - Provide the summary in French.

    Here is the text to summarize:
    {text}
    """


    try:
        response = openai.ChatCompletion.create(
            model=model_choice,
            messages=[
                {"role": "user", "content": user_query}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        # Extract response text
        response_text = response.choices[0].message['content']
        st.session_state.user_input = user_query
        return response_text

    except Exception as e:
        a = f"ERROR: {e}"
        return a