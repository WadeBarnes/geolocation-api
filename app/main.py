import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from httpx import AsyncClient

app = FastAPI(
    title = os.environ.get("APP_NAME"),
    description = os.environ.get("APP_DESCRIPTION"),
    version = os.environ.get("APP_VERSION"),
)

# ToDo:
#   - Add geohash convertion methods and APIs.

# Other referances:
# Lat,Long to goehash convertion web site:
#   - http://geohash.co/
#
# - https://rapidapi.com/blog/ip-geolocation-api/
#
# GeoHash Modules:
# - https://github.com/mrJean1/PyGeodesy
# - https://pypi.org/project/PyGeodesy/
# - https://pypi.org/project/geohashlite/
# - https://pypi.org/project/geohashrs/
# - https://pypi.org/project/geohash2/


@app.get("/")
async def read_root():
    return {"Message": "Hello World!"}


# ==========================================================================================
# IPWHOIS.IO
#   - https://ipwhois.io/documentation
IP_WHO_IS_API = "https://ipwhois.app/json/{ip_address}"
# IP_WHO_IS_API = "https://ipwhois.app/json/209.53.249.193?objects=latitude,longitude"
#-------------------------------------------------------------------------------------------
@app.get("/ipwhois/{ip_address}")
async def get_location_from_ipwhois(ip_address: str):
    async with AsyncClient() as client:
        url = IP_WHO_IS_API.format(ip_address=ip_address)
        # print(url)
        response = await client.get(url)
    return response.json()
# ==========================================================================================


# ==========================================================================================
# ipinfo.io
#   - https://ipinfo.io
#   - https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python/55432323#55432323
IP_INFO_API = "https://ipinfo.io/{ip_address}/json"
#-------------------------------------------------------------------------------------------
@app.get("/ipinfo/{ip_address}")
async def get_location_from_ipinfo(ip_address: str):
    async with AsyncClient() as client:
        url = IP_INFO_API.format(ip_address=ip_address)
        # print(url)
        response = await client.get(url)
    return response.json()
# ==========================================================================================


# ==========================================================================================
# geoPlugin
#   - Does not appear to support an https endpoint
#   - https://www.geoplugin.com/webservices/json
GEO_PLUGIN_API = "http://www.geoplugin.net/json.gp?ip={ip_address}"
#-------------------------------------------------------------------------------------------
@app.get("/geoplugin/{ip_address}")
async def get_location_from_geoplugin(ip_address: str):
    async with AsyncClient() as client:
        url = GEO_PLUGIN_API.format(ip_address=ip_address)
        # print(url)
        response = await client.get(url)
    return response.json()
# ==========================================================================================