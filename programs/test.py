from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf") # downloads / loads a 4.66GB LLM
print()
model.generate("Keep all responses short")
with model.chat_session():
    print(model.generate("How heartrate can be used to detect hypertension"))

