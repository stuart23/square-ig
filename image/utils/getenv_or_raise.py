from os import getenv


def getenv_or_raise(key):
    """Get the environment variable value for the given key, or raise an exception if it's not set."""
    value = getenv(key)
    if value is None:
        raise KeyError(f"Environment variable '{key}' is not set.")
    return value