import os
import sys

user_id = sys.argv[1]
if os.path.exists("../../{}".format(user_id)):
    with open('server_ip.txt','w') as f:
        f.write("127.0.0.1")