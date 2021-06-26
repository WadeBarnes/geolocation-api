import os
import json
from enum import Enum


class GeoApiEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class GeoApis(object):
    def __init__(self):
        self._apis = self.__load_api_list()

    def __get_script_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    def __load_api_list(self):
        with open(f"{self.__get_script_dir()}/geo_apis.json") as json_file:
            apis = json.load(json_file)
        return apis

    @property
    def keys(self):
        return self._apis.keys()

    def get_ip_api(self, api: GeoApiEnum, ip_address: str) -> str:
        return self._apis[api.value]["api"].format(ip_address=ip_address)

    @staticmethod
    def get_GeoApiEnum() -> GeoApiEnum:
        """Dynamically generates a GeoApiEnum that can be used to select the available GeoLocation APIs.
        """
        apis = GeoApis()
        return GeoApiEnum('GeoApi', list(apis.keys))