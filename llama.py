from ollama import chat


def get_response(user_query):

    response = chat(
        model='llama3.2:1b',
        messages=[
            {
                'role': 'user',
                'content': user_query
            }
        ]
    )

    return response.message.content