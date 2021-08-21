import json
with open("good_backup.json","r") as f:
    json_data = json.loads(f.read());
    total_msgs = 500
    out = filter(lambda x: x['pk']<total_msgs, json_data)
    #for pk,model in enumerate(json_data):
    #    if model['model'] == 'chat.message':
    #        if pk>total_msgs:
    #            json_data.pop(pk)
    with open("fiftyThousandMsgs.json","w") as wf:
        wf.write(json.dumps(json_data))
