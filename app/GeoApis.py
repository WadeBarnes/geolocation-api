import os
import json
from enum import Enum
from pydantic import BaseModel

class GeoLocation(BaseModel):
    ip: str
    country: str
    region: str
    city: str
    latitude: float
    longitude: float

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
    def normalize_response(location: dict) -> GeoLocation:
        """Normalizes the response from a supported GeoLocation API into a consistent structure.
        """
        ip = location.get("geoplugin_request") or location.get("ip") or ""
        country = location.get("geoplugin_countryCode") or location.get("country_code") or location.get("country") or ""
        region = location.get("geoplugin_regionName") or location.get("region") or ""
        city = location.get("geoplugin_city") or location.get("city") or ""
        latitude = location.get("geoplugin_latitude") or location.get("latitude") or location.get("loc").split(",")[0]
        longitude = location.get("geoplugin_longitude") or location.get("longitude") or location.get("loc").split(",")[1]
        geo_location = GeoLocation(
            ip = ip,
            country = country,
            region = region,
            city = city,
            latitude = latitude,
            longitude = longitude
        )
        return geo_location

    @staticmethod
    def get_GeoApiEnum() -> GeoApiEnum:
        """Dynamically generates a GeoApiEnum that can be used to select the available GeoLocation APIs.
        """
        apis = GeoApis()
        return GeoApiEnum('GeoApi', list(apis.keys))