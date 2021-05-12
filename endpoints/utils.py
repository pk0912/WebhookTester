import uuid


def get_random_string():
    """
    :return: First 18 characters of a random UUID converted to string
    """
    random_string = str(uuid.uuid4())
    return random_string[:18]
