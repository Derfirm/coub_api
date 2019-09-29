import json

__all__ = ("extract_params_from_file",)


def extract_params_from_file(path, name):
    with open(path) as f:
        return json.load(f)[name]
