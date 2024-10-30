pip install -r requirements.txt
py main.py

# Shoutout to GPT-SoVITS-beta0706 for TTS part.
Follow their instructions and implement my GPT & SoVITS models to use Rem Japanese Voice.
1. Navigate to put_into_GPT-SoVITS
2. Put .pth to SoVITS_weights
3. Put .ckpt to GPT_weights
4. Set the argument/default path to the voice.wav and transcribed text
5. Inference.

# !!! DYOR for pytorch !!!
# The below code installs pytorch and related lib
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

This project goal is to allow users speak directly to llms.
Speech-to-text STT: input=user voice, output=text
Large language model LLM: input=text, output=llm_response
Text-to-speech TTS: input=llm_response, output=llm_response_voice

# Next-task:
Make a more presentable version within the Chinese market with 周星驰 voice.

# To-do:
1. Fine-tune LLM, to be task-specific and to be able to take on roles.
2. Make a more presentable version within the Chinese market with 周星驰 voice.

# Done:
1. Basic framework for STT -> LLM is completed.
2. TTS localhost API is completed.
3. Created system_prompt to limit LLM, can only respond in Japanese.
4. Basic framework for LLM -> TTS is completed.
5. Test different models, pipelines, and APIs for lower response time and accuracy.
6. Fine-tune TTS, with custom voice, from collecting data samples, labelling, training, etc. (Japanese Rem voice)

# Notes
Finally found a way to use POE models (GPT-4o, Cluade-3.5-Haiku...), the smoothness in convo is much better than Hugging face pipielines, can also do role-plays, could be a temp solution before fine-tuning my own LLM model.