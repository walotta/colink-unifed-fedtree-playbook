import json

if __name__=='__main__':
    with open('stdout.txt','r') as f:
        stdout = f.read()
    with open('stderr.txt','r') as f:
        stderr = f.read()
    msg = json.dumps({
        "stdout": stdout,
        "stderr": stderr,
    })
    with open("return_msg.txt",'w') as f:
        f.write(msg)