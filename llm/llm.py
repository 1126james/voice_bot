from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def llm(query: str, steps: int) -> str:
    print("\n--- Calling LLM ---\n")
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors='pt')
    
    # initialize chat_history_ids with an empty tensor of type Long
    chat_history_ids = torch.empty(0, dtype=torch.long)
    
    # append the new user input tokens to the chat history
    if steps > 0:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1).long()
    else:
        print("\n--- Initializing New Chat Memory ---\n")
        bot_input_ids = new_user_input_ids.long()
    
    # generate a response while limiting the total chat history to 1000 tokens
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    
    # pretty print last output tokens from bot
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    llm()