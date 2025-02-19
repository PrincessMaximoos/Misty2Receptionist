ids : list[dict] = [{"Name" : "Name", "Company" : "Company", "IDNum" : "IDNum"}, ]
visitor_count = 0

import json

with open("output/visitor_info.json", "w") as f:
    json.dump({"result" : ids, "num" : visitor_count}, f)