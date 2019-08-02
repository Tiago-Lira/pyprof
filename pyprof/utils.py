import os


root_path = None


def get_root_path():
    global root_path

    if root_path is None:
        root_path = os.environ.get('PROFILE_PATH')

    if root_path is None:
        root_path = os.path.join(os.getcwd(), 'prof')

    return root_path


def get_paths(path=None):
    if path is None:
        path = get_root_path()

    file_names = []

    for root, _, files in os.walk(path):
        file_names += [os.path.join(root, file_name) for file_name in files]

    return file_names


def join_path(*paths):
    root_path = get_root_path()

    if not os.path.exists(root_path):
        os.makedirs(root_path)

    return os.path.join(root_path, *paths)
