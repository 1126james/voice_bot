# main.py
from stt.stt import speak, get_supported_languages
from llm.get_response import llm
import uuid
import os
import json

CHAT_HISTORY_FOLDER = "chat_history"

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

def save_conversation_id(conversation_id):
    with open("conversation_id.txt", "w") as file:
        file.write(conversation_id)

def load_conversation_id():
    if os.path.exists("conversation_id.txt"):
        with open("conversation_id.txt", "r") as file:
            return file.read().strip()
    else:
        return None

def get_conversation_id():
    previous_conversation_id = load_conversation_id()
    if previous_conversation_id:
        while True:
            choice = input(f"Found a previous conversation (ID: {previous_conversation_id}). Do you want to continue or start a new one? (C/N): ")
            if choice.upper() == "C":
                return previous_conversation_id
            elif choice.upper() == "N":
                delete_conversation_history(previous_conversation_id)
                new_conversation_id = f"c-{uuid.uuid4().hex}"
                save_conversation_id(new_conversation_id)
                return new_conversation_id
            else:
                print("Invalid choice. Please enter 'C' to continue or 'N' to start a new session.")
    else:
        new_conversation_id = f"c-{uuid.uuid4().hex}"
        save_conversation_id(new_conversation_id)
        return new_conversation_id

def main(language):
    break_keywords = ['quit', 'bye', 'goodbye', 'close', 'exit']
    user_id = f"u-{uuid.uuid4().hex}"
    conversation_id = get_conversation_id()

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

        conversation_history.append({"role": "user", "content": text})
        conversation_history.append({"role": "bot", "content": response})
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