import json
with open("fiftyThousandMsgs.json","r") as f:
    json_data = json.loads(f.read());
    pk = 1
    for model in json_data:
        if model['model'] == 'chat.message':
            pk += 1
    print(pk)
