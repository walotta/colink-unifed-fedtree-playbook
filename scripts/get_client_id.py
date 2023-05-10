import json

if __name__=='__main__':
    with open('param.json','r') as f:
        param = json.load(f)
    participants = param['participants']
    user_id = param['user_id']
    passed_server = 0
    client_id = None
    for i, p in enumerate(participants):
        if p[1] == "server":
            passed_server += 1
        if p[0] == user_id:
            client_id = i - passed_server
    assert client_id is not None
    with open('client_id.txt','w') as f:
        f.write(str(client_id))
