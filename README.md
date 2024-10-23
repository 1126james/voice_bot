pip install -r requirements.txt
py main.py

# !!! DYOR for pytorch !!!
# The below code installs pytorch and related lib
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

This project goal is to allow users speak directly to llms.
Speech-to-text STT: input=user voice, output=text
Large language model LLM: input=text, output=llm_response
Text-to-speech TTS: input=llm_response, output=llm_response_voice

Next-task:
Build basic framework for LLM -> TTS.

To-do:
1. Test different models, pipelines, and APIs for lower response time and accuracy.
2. Fine-tune TTS first, with custom voice. All by myself, from collecting data samples, labelling, training, etc.
3. Fine-tune LLM, to be task-specific and to be able to take on roles.

Done:
Basic framework for STT -> LLM is completed.

Finally found a way to use POE models (GPT-4o, Cluade-3.5-Haiku...), the smoothness in convo is much better than Hugging face pipielines, can also do role-plays, could be a temp solution before fine-tuning my own model.