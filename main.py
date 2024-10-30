# main.py
from stt.stt import speak, get_supported_languages
from llm.get_response import llm
from tts.play_tts import play_tts
import uuid
import os
import json

CHAT_HISTORY_FOLDER = "chat_history"
IDs_FILE = "ids.json"

def load_or_create_conversation_history(conversation_id):
    history_file = os.path.join(CHAT_HISTORY_FOLDER, f"{conversation_id}_history.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as file:
            conversation_history = json.load(file)
    else:
        conversation_history = []
    return conversation_history

def delete_conversation_history(conversation_id):
    history_file = os.path.join(CHAT_HISTORY_FOLDER, f"{conversation_id}_history.json")
    if os.path.exists(history_file):
        os.remove(history_file)

def save_conversation_history(conversation_id, conversation_history):
    history_file = os.path.join(CHAT_HISTORY_FOLDER, f"{conversation_id}_history.json")
    with open(history_file, "w") as file:
        json.dump(conversation_history, file)

def trim_conversation_history(conversation_history, max_messages=10):
    """Keep only the last max_messages messages in the conversation history"""
    if len(conversation_history) > max_messages:
        return conversation_history[-max_messages:]
    return conversation_history

def save_ids(conversation_id, user_id):
    data = {
        "conversation_id": conversation_id,
        "user_id": user_id
    }
    with open(IDs_FILE, "w") as file:
        json.dump(data, file)

def load_ids():
    if os.path.exists(IDs_FILE):
        with open(IDs_FILE, "r") as file:
            data = json.load(file)
            return data.get("conversation_id"), data.get("user_id")
    return None, None

def get_ids():
    previous_conversation_id, previous_user_id = load_ids()
    if previous_conversation_id and previous_user_id:
        while True:
            choice = input(f"Found previous session (User ID: {previous_user_id}, Conversation ID: {previous_conversation_id}). Do you want to continue or start a new one? (C/N): ")
            if choice.upper() == "C":
                return previous_conversation_id, previous_user_id
            elif choice.upper() == "N":
                delete_conversation_history(previous_conversation_id)
                new_conversation_id = f"c-{uuid.uuid4().hex}"
                new_user_id = f"u-{uuid.uuid4().hex}"
                save_ids(new_conversation_id, new_user_id)
                return new_conversation_id, new_user_id
            else:
                print("Invalid choice. Please enter 'C' to continue or 'N' to start a new session.")
    else:
        new_conversation_id = f"c-{uuid.uuid4().hex}"
        new_user_id = f"u-{uuid.uuid4().hex}"
        save_ids(new_conversation_id, new_user_id)
        return new_conversation_id, new_user_id

def main(language):
    break_keywords = ['quit', 'bye', 'goodbye', 'close', 'exit']
    conversation_id, user_id = get_ids()

    if not os.path.exists(CHAT_HISTORY_FOLDER):
        os.makedirs(CHAT_HISTORY_FOLDER)

    conversation_history = load_or_create_conversation_history(conversation_id)

    while True:
        text = speak(language)

        if text.lower() in [keyword.lower() for keyword in break_keywords]:
            print("Break keyword detected. Exiting...")
            break

        response = llm(text, user_id, conversation_id, conversation_history)
        print(f"Response: {response}")
        play_tts(text=response)

        conversation_history.append({"role": "user", "content": text})
        conversation_history.append({"role": "bot", "content": response})
        conversation_history = trim_conversation_history(conversation_history)
        save_conversation_history(conversation_id, conversation_history)

if __name__ == "__main__":
    supported_languages = get_supported_languages()
    while True:
        language = input(f"Enter the language ({supported_languages}): ")
        language = language.lower()
        if language not in get_supported_languages().split(", "):
            print(f"Please enter only {supported_languages}.")
            continue
        break
    main(language)