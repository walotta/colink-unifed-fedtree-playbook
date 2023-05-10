import json

def filter_log_from_fedtree_output(output):
    filtered_output = ""
    for line in output.split("\n"):
        line_json = json.dumps({"fedtree": line})  # TODO: convert log here
        if ".cpp" in line:
            filtered_output += f"{line_json}\n"
    return filtered_output

if __name__=='__main__':
    with open('stdout.txt','r') as f:
        stdout = f.read()
    with open('stderr.txt','r') as f:
        stderr = f.read()
    log = filter_log_from_fedtree_output(stdout + stderr)
    with open("log.txt",'w') as f:
        f.write(log)