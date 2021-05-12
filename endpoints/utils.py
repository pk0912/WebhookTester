import uuid


def get_random_string():
    """
    :return:
    """
    random_string = str(uuid.uuid4())
    return random_string[:18]
