from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct-Q4_0.gguf")


def get_response(question : str) -> str:
    '''
    Generates a response.
    --------------------
    question : str [What is AI?]
    '''

    return model.generate("Without acknowledging this statement and keeping your answer short and concise. " + question)

with model.chat_session():
    while True:
        print()

        question = input("Chatbot | Ask me anything:\n\n")

        if question == "quit":
            break

        print("Loading...")
        print(get_response(question))
