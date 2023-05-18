# colink-unifed-fedtree-playbook

> This is a playbook implementation of unified fedtree protocol.

## Usage

1. download the colink-playbook
    ```bash
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/CoLearn-Dev/colink-playbook-dev/main/download.sh)"
    chmod +x colink-playbook
    ```

2. start the protocol
    ```bash
    COLINK_FEDTREE=$(pwd) ./colink-playbook --addr <addr> --jwt <jwt>
    ```

## Run test
  
```bash
COLINK_FEDTREE=$(pwd) python3 test/test.py
```