def read_variable_from_env(variable_name):
    if(variable_name == 'PUBLIC_KEY'):
        with open('.env', 'r') as file:
            for line in file:
                if variable_name in line:
                    value = line.split('=')[1].strip()
                    return value
    else:
        with open('local.env', 'r') as file:
            for line in file:
                if variable_name in line:
                    value = line.split('=')[1].strip()
                    return value
