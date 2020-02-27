import json
def return_metadata():
    
    with open('MetaData_index', 'r') as f:
        x = f.readlines()

    a = "".join(x)

    return json.dumps(x)