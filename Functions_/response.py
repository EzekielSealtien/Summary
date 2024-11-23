import openai
import streamlit as st
from .openaikeys.key import get_open_ai_key

def responseModel(text, instructions,parameters):

    openai.api_key =get_open_ai_key()
    
    model_choice=parameters[0]
    summaryLevel=parameters[1]
    if not instructions:
        instructions = "DO NOT MODIFY ANYTHING. Generate the same text provided."

        # Construct the user query with limited history
    user_query = f"""
    Please process the following text according to the provided instructions. The model should be capable of both formatting and executing any additional tasks described in the instructions. Use HTML tags and inline CSS where necessary to apply formatting.

    Instructions:
    - Review the instructions provided below to understand what actions are required. These actions may include formatting (e.g., bold, italic, underline) as well as other operations like adding or modifying text elements.
    - For formatting, use only the requested HTML tags (e.g., `<b>`, `<i>`, `<u>`, `<div style="...">`) to frame specific portions of the text without changing the content itself.
    - If spacing adjustments are needed, use non-breaking spaces (`&nbsp;`) as specified.
    - Apply the specified formatting by framing only the requested text with HTML tags, without altering or removing any existing style properties.
    - If changing the color of titles, use inline CSS to set the color requested  (`style="color:color requested;"`) without changing other styles like font size, font weight, or alignment.
    - Only apply formatting instructions as stated, and avoid modifying any other existing styles.
    - Execute all instructions as specified in the additional instructions below, which may include adding, modifying, or reordering text.
    - Only apply instructions given; do not generate or alter content outside of these specifications.
    - Return the text formatted with HTML/CSS tags as instructed.

    Additional Instructions:
    {instructions}

    Here is the text to process:
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

    openai.api_key =get_open_ai_key()
    model_choice=parameters[0]
    summaryLevel=parameters[1]
    language=parameters[2]

    user_query = f"""
    Below is a text  that may or may not contain multiple sections with titles such as "Introduction," "Conclusion," etc. Please follow these instructions carefully when summarizing:

    Instructions:
    - First, check if the text contains section titles (e.g., "Introduction," "Conclusion",tec) or subtitles. 
    - If titles or subtitles are present, do not modify or remove these titles. Instead, summarize the content within each section individually, keeping each summary concise.
    - If no titles or subtitles are detected, summarize the entire text as a single cohesive summary.
    - Maintain  HTML/CSS-styled formatting in the final output.
    -Check the summary level specified:
        - If the summary level is "abrege", provide an abbreviated summary that covers only the main points in a concise manner.
        - If the summary level is "complet", provide a comprehensive summary that includes all key details from the text.
        - Ensure that the summary is coherent and maintains the context of the original text.
        Summary Level: {summaryLevel}
french
    - Only summarize the content without adding or modifying any additional information.
    

    - Provide the summary in {language} .

    Here is the text  content  to summarize:
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