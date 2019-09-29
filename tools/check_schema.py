import json
from pprint import pprint

from deepdiff import DeepDiff

from coub_api import CoubApi
from tests import _BASE_PATH  # noqa
from tools.utils import extract_params_from_file


def compare_schema_with_data(schema, data):
    ddiff = DeepDiff(json.loads(schema.json()), data, view="tree")
    return ddiff.to_json()


if __name__ == "__main__":
    api = CoubApi()
    for coub_id in extract_params_from_file(
        _BASE_PATH / "snapshots/config.json", "coubs_list"
    ):
        response = api.coubs._get_coub_response(coub_id)
        schema = api.coubs.get_coub(coub_id)
        pprint(compare_schema_with_data(schema, response.json()))
        break
