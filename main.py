# main.py
from stt.stt import speak
from llm.llm import llm

def main():
    steps = 0
    break_keywords = ['quit', 'bye', 'goodbye', 'close', 'exit']
    while True:
    # Get transcription from STT
        print("Calling STT")
        text = speak()

        # Check if the spoken text exactly matches any break keyword
        print("\n--- Checking breakword ---\n")
        if text.lower() in [keyword.lower() for keyword in break_keywords]:
            print("Break keyword detected. Exiting...")
            break
        else:
            print("No breakword found.\n")

        # Pass text to LLM and get response
        response = llm(text, steps)
        print(f"Response: {response}")
        steps+=1

        # Initialize new chat history in llm.py
        if steps == 5:
            steps = 0

if __name__ == "__main__":
    main()