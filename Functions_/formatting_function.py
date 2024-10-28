import openai


def summary_layout(text,instructions):

    
    openai.api_key ="sk-GJPAXciZeshLqhrHRifEcTbiotKbcUzsrlMaqx82nXT3BlbkFJRmjfcg1nfcu1rlnKvyPH9l7j9q9DYhAT9rdBBu5F0A"
    
    if not instructions:
        instructions="DO NOT MODIFY ANYTHING.Generate the same text provided"
        
        
    # Construct the conversation imporved
    user_message = f"""Below provided is a text. read through this text.
    Follow below instructions when responding:

    Model Instructions:
    -Don't modify anything  expect what i ask you
    -When i tell you to modify something, you MUST just modify it but don't modify the overall text
    -{instructions}

    text:{text}


    """
    

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
        return response_text


    except Exception as e:
        a=f"ERROR: {e}"
        return a
