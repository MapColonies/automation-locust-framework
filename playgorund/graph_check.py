def to_bool(string, default):
    # (str- bool) -> (bool)
    """
    This method convert string to bool - "True, "Yes", "1" are considered True
    """
    if string and string.strip():
        return string.strip()[0].lower() in ["1", "t", "y"]
    return default


def str_to_bytes(string):
    """
    Convert from string to bytes
    """
    if string is None:
        return None

    return string.encode("utf-8")


def bytes_to_str(string):
    """
    Convert from bytes to str.
    """
    if string is None:
        return None

    return string.decode("utf-8")


def get_environment_variable(name, default_val):
    # (str, object) -> object
    """
    Returns an environment variable in the type set by the default value.
    If environment variable is empty or cannot be converted to default_val type, function returns default_val
    Note that for boolean value either 'True' 'Yes' '1', regardless of case sensitivity are considered as True.
    """
    value = """[
            [
                (34.78599261466954, 30.62650484692135),
                (34.78599261466954, 30.56735846770877),
                (34.873818350199315, 30.56735846770877),
                (34.873818350199315, 30.62650484692135),
                (34.78599261466954, 30.62650484692135),
            ],
            [
                (34.75686905280091, 30.674265565587575),
                (34.75686905280091, 30.668797385759987),
                (34.756895479083596, 30.668797385759987),
                (34.756895479083596, 30.674265565587575),
                (34.75686905280091, 30.674265565587575),
            ],
        ]"""
    if value:
        if isinstance(default_val, bool):
            value = to_bool(value, default_val)
        elif default_val is not None:
            try:
                value = type(default_val)(value)
            except ValueError:
                pass
                value = default_val

    else:
        value = default_val
    return value


print(type(get_environment_variable(name=None, default_val="list")))
