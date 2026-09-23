from flask import Flask, render_template, request, redirect, url_for
from llama import get_response
import json
import os
import uuid


app = Flask(__name__)

# ==================================================
# CHAT FILE
# ==================================================

CHAT_FOLDER = "chats"

CHAT_FILE = os.path.join(
    CHAT_FOLDER,
    "chat_history.json"
)


# ==================================================
# CREATE CHAT FOLDER
# ==================================================

if not os.path.exists(CHAT_FOLDER):

    os.makedirs(CHAT_FOLDER)


# ==================================================
# CREATE JSON FILE
# ==================================================

if not os.path.exists(CHAT_FILE):

    with open(CHAT_FILE, "w") as file:

        json.dump({}, file)


# ==================================================
# LOAD CHATS
# ==================================================

def load_chats():

    try:

        with open(CHAT_FILE, "r") as file:

            data = json.load(file)

            # Make sure JSON contains a dictionary
            if isinstance(data, dict):

                return data

            return {}

    except (json.JSONDecodeError, FileNotFoundError):

        # If JSON file is empty or corrupted
        # return an empty dictionary

        return {}


# ==================================================
# SAVE CHATS
# ==================================================

def save_chats(chats):

    with open(CHAT_FILE, "w") as file:

        json.dump(
            chats,
            file,
            indent=4
        )


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    chats = load_chats()

    return render_template(
        "index.html",
        chats=chats,
        current_chat=None,
        current_chat_id=None
    )


# ==================================================
# NEW CHAT
# ==================================================

@app.route("/new-chat")
def new_chat():

    # Create a temporary unique ID
    # BUT DON'T SAVE IT YET

    chat_id = str(uuid.uuid4())

    return redirect(
        url_for(
            "chat_page",
            chat_id=chat_id
        )
    )


# ==================================================
# OPEN CHAT
# ==================================================

@app.route("/chat/<chat_id>")
def chat_page(chat_id):

    chats = load_chats()

    # ----------------------------------------------
    # If chat is already saved
    # ----------------------------------------------

    if chat_id in chats:

        current_chat = chats[chat_id]

    else:

        # ------------------------------------------
        # New temporary chat
        # ------------------------------------------

        current_chat = {
            "title": "New Chat",
            "messages": []
        }

    return render_template(
        "index.html",
        chats=chats,
        current_chat=current_chat,
        current_chat_id=chat_id
    )


# ==================================================
# SEND MESSAGE
# ==================================================

@app.route(
    "/chat/<chat_id>/send",
    methods=["POST"]
)
def send_message(chat_id):

    # Get user message
    user_message = request.form["message"].strip()


    # Don't process empty message

    if not user_message:

        return redirect(
            url_for(
                "chat_page",
                chat_id=chat_id
            )
        )


    # Load saved chats

    chats = load_chats()


    # ==================================================
    # CHECK WHETHER CHAT ALREADY EXISTS
    # ==================================================

    if chat_id not in chats:

        # ----------------------------------------------
        # This is a NEW chat.
        # Create it NOW.
        # ----------------------------------------------

        chats[chat_id] = {

            "title": "New Chat",

            "messages": []

        }


    # Get current chat

    chat_data = chats[chat_id]


    # Get previous conversation

    history = chat_data["messages"]


    # ==================================================
    # GET AI RESPONSE
    # ==================================================

    bot_response = get_response(
        user_message,
        history
    )


    # ==================================================
    # ADD USER MESSAGE
    # ==================================================

    history.append({

        "role": "user",

        "content": user_message

    })


    # ==================================================
    # ADD AI RESPONSE
    # ==================================================

    history.append({

        "role": "assistant",

        "content": bot_response

    })


    # ==================================================
    # CREATE CHAT TITLE
    # ==================================================

    if chat_data["title"] == "New Chat":

        title = user_message[:35]

        if len(user_message) > 35:

            title += "..."

        chat_data["title"] = title


    # ==================================================
    # SAVE CHAT
    # ==================================================

    save_chats(chats)


    # ==================================================
    # OPEN CHAT AGAIN
    # ==================================================

    return redirect(
        url_for(
            "chat_page",
            chat_id=chat_id
        )
    )


# ==================================================
# DELETE CHAT
# ==================================================

@app.route("/delete/<chat_id>")
def delete_chat(chat_id):

    chats = load_chats()


    if chat_id in chats:

        del chats[chat_id]


    save_chats(chats)


    return redirect(
        url_for("home")
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )