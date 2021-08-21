import json
with open("backup.json","r") as f:
    json_data = json.loads(f.read());
    pk = 1
    for model in json_data:
        if model['model'] == 'chat.message':
            model['pk'] = pk
            pk += 1
    with open("good_backup.json","w") as wf:
        wf.write(json.dumps(json_data))
