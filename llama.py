from ollama import chat


def get_response(user_query, chat_history=None):

    messages = []

    if chat_history:
        messages.extend(chat_history)

    messages.append({
        "role": "user",
        "content": user_query
    })

    response = chat(
        model="llama3.2:1b",
        messages=messages
    )

    return response.message.content