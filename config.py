# Current mode of operation
current_mode = 'analysis'  # Change to 'analysis' or 'test' as needed.

config = {
    'test': 'data/test/',
    'analysis': 'data/analysis/'
}


def get_data_dir():
    return config[current_mode]


def get_file_path(file_name):
    return get_data_dir() + file_name
