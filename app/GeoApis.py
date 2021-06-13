import os
import json

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
        return self.apis.keys()

    def get_ip_api(self, api_id: str, ip_address: str):
        return self._apis[api_id]["api"].format(ip_address=ip_address)