# from gpt4all import GPT4All
# model = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf") # downloads / loads a 4.66GB LLM

# with model.chat_session():
#     # model.generate("<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful AI assistant knowledgeable in the subject of AI. You should keep all answers short and concise.<|eot_id|><|start_header_id|>user<|end_header_id|>")    
#     print()
#     print(model.generate("Without acknowledging this statement and keeping your answer short and concise. How heartrate can be used to detect hypertension"))



# def update_count():
#     with open("output/visitor_info.txt", "a") as vis: # wb is important, standard write doesnt work (write as bytes maybe???)
#         vis.write("\n+-----------------------------------------+\n")
#         string = "Number of Visitors: " + str(visitor_count) + '\n'
#         for id in ids:
#             for item in id.values():
#                 string += "{:<20}".format(str(item)) + '| '
#             string += '\n'
#         vis.write(string)
#     vis.close()

# ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, 
#                     {"Name" : "Max McGill", "Company" : "Staffs", "IDNum" : "0"}, 
#                     {"Name" : "Benhur Bastaki", "Company" : "Staffs", "IDNum" : "1"}]
# visitor_count = 2

ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, ]
visitor_count = 0


# update_count()

import json

# with open("output/visitor_info.json") as f:
#     test = json.load(f)
#     print(test["num"])

with open("output/visitor_info.json", "w") as f:
    json.dump({"result" : ids, "num" : visitor_count}, f)