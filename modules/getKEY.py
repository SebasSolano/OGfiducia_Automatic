def read_variable_from_env(variable_name):
    if(variable_name):
        with open('.env', 'r') as file:
            for line in file:
                if variable_name in line:
                    value = line.split('=')[1].strip()
                    return value
                
def write_variable_to_env(variable_name, new_value):
    with open('.env', 'r') as file:
        lines = file.readlines()

    with open('.env', 'w') as file:
        for line in lines:
            if variable_name in line:
                file.write(f"{variable_name}={new_value}\n")
            else:
                file.write(line)