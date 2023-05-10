import sys
import json
import tempfile
import os
import base64

def read_param_from_file(param_path):
    with open(param_path, 'r') as f:
        param_str = json.load(f)
    return base64.b64decode(param_str['param'])

def load_config_from_param_and_check(param: bytes):
    unifed_config = json.loads(param.decode())
    framework = unifed_config["framework"]
    assert framework == "fedtree"
    deployment = unifed_config["deployment"]
    if deployment["mode"] != "colink":
        raise ValueError("Deployment mode must be colink")
    return unifed_config

DATASET_TO_OBJECTIVE = {
    "breast_horizontal": 'binary:logistic',
    "default_credit_horizontal": 'binary:logistic',
    "give_credit_horizontal": 'binary:logistic',
    "student_horizontal": 'reg:linear',
    "vehicle_scale_horizontal": 'multi:softmax',
    "breast_vertical": 'binary:logistic',
    "motor_vertical": 'reg:linear',
    "default_credit_vertical": 'binary:logistic',
    "dvisits_vertical": 'reg:linear',
    "give_credit_vertical": 'binary:logistic',
    "student_vertical": 'reg:linear',
    "vehicle_scale_vertical": 'multi:softmax',
    "femnist": 'multi:softmax',
}

def convert_unifed_config_to_fedtree_config(unifed_config):  # note that for the target config, the "data" field is still missing
    tree_param = unifed_config['training']['tree_param']
    fedtree_config = {
        "n_parties": len(unifed_config["deployment"]["participants"]) - 1,  # fedTree does not count the server in "n_parties"
        "n_trees": tree_param['n_trees'],
        "depth": tree_param['max_depth'],
        "max_num_bin": tree_param['max_num_bin'],
        "data_format": "csv",
        "objective": DATASET_TO_OBJECTIVE[unifed_config['dataset']],
        "learning_rate": unifed_config['training']['learning_rate'],
        "verbose": 1,
    }
    if unifed_config['algorithm'] == 'histsecagg':
        fedtree_config["mode"] = "horizontal"
        fedtree_config["privacy_tech"] = "sa"
    elif unifed_config['algorithm'] == 'secureboost':
        fedtree_config["mode"] = "vertical"
        fedtree_config["privacy_tech"] = "he"
    else:
        raise ValueError(f"Unknown algorithm {unifed_config['algorithm']}")
    return fedtree_config

def create_conf_file_content_from_fedtree_config(fedtree_config):
    conf_file_content = ""
    for key, value in fedtree_config.items():
        conf_file_content += f"{key}={value}\n"
    return conf_file_content

if __name__=='__main__':
    type = sys.argv[1]
    param_path = sys.argv[2]
    fedtree_conf_name_path = sys.argv[3]
    param_str = read_param_from_file(param_path)
    unifed_config = load_config_from_param_and_check(param_str)
    fedtree_config = convert_unifed_config_to_fedtree_config(unifed_config)
    root_dir = os.environ.get('COLINK_FEDTREE')
    if type == 'server':
        if unifed_config['algorithm'] == 'secureboost':
            fedtree_config["data"] = f"{root_dir}/data/{unifed_config['dataset']}_1.csv"
        with open(fedtree_conf_name_path, 'w') as f:
            f.write(create_conf_file_content_from_fedtree_config(fedtree_config))
    elif type == 'client':
        with open("client_id.txt","r") as f:
            client_id = f.read()
        fedtree_config["data"] = f"{root_dir}/data/{unifed_config['dataset']}_{client_id}.csv"
        if unifed_config['algorithm'] == 'histsecagg':
            fedtree_config["n_features"] = {"breast_horizontal": 30}[unifed_config['dataset']]  # currently just a hack, later we should get this from the mapping file for predefined datasets
        test_data_path = f"{root_dir}/data/{unifed_config['dataset']}"+"_test.csv"
        if os.path.isfile(f"{test_data_path}"):
            fedtree_config["test_data"] = test_data_path
        with open("server_ip.txt",'r') as f:
            server_ip = f.read()
        server_ip = fedtree_config["ip_address"] = server_ip
        with open(fedtree_conf_name_path, 'w') as f:
            f.write(create_conf_file_content_from_fedtree_config(fedtree_config))

