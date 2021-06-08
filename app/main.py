from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

import os
from httpx import AsyncClient
import geohash2
from geohashrs import geohash_encode
import geohashlite
from pygeodesy import geohash as pygeodesy_geohash

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
# Geolocation APIs:
# - https://ipgeolocation.io/


class GeoHashRequest(BaseModel):
    latitude: float
    longitude: float
    precision: Optional[int] = 12


@app.get("/")
async def read_root():
    return {"Message": "Hello World!"}


# ==========================================================================================
# PyGeodesy
# - https://pypi.org/project/PyGeodesy
#
# ipwhois:
# {
#   "latitude": -33.83965, "longitude": 151.20541,  "precision": 8
# }
# {
#   "pygeodesy": "r3gx2z8m"
# }
#
# ipinfo:
# {
#   "latitude": -33.8386, "longitude": 151.2033, "precision": 8
# }
# {
#   "pygeodesy": "r3gx2xyg"
# }
#
# geoPlugin:
# {
#   "latitude": -33.494, "longitude": 143.2104, "precision": 8
# }
# {
#   "pygeodesy": "r4jc6yde"
# }
#
#-------------------------------------------------------------------------------------------
@app.post("/pygeodesy/encode")
async def encode_using_pygeodesy(location: GeoHashRequest):
    geohash = pygeodesy_geohash.encode(location.latitude, location.longitude, location.precision)
    return {"pygeodesy": geohash}
# ==========================================================================================


# ==========================================================================================
# geohashlite
# - https://pypi.org/project/geohashlite
#
# ipwhois:
# {
#   "latitude": -33.83965, "longitude": 151.20541,  "precision": 8
# }
# {
#   "geohashlite": "r3gx2z8m"
# }
#
# ipinfo:
# {
#   "latitude": -33.8386, "longitude": 151.2033, "precision": 8
# }
# {
#   "geohashlite": "r3gx2xyg"
# }
#
# geoPlugin:
# {
#   "latitude": -33.494, "longitude": 143.2104, "precision": 8
# }
# {
#   "geohashlite": "r4jc6yde"
# }
#
#-------------------------------------------------------------------------------------------
@app.post("/geohashlite/encode")
async def encode_using_geohashlite(location: GeoHashRequest):
    geohash = geohashlite.encode(location.latitude, location.longitude, location.precision)
    return {"geohashlite": geohash}
# ==========================================================================================


# ==========================================================================================
# geohashrs
# - https://pypi.org/project/geohashrs
#
# ipwhois:
# {
#   "latitude": -33.83965, "longitude": 151.20541,  "precision": 8
# }
# {
#   "geohashrs": "r3gx2z8m"
# }
#
# ipinfo:
# {
#   "latitude": -33.8386, "longitude": 151.2033, "precision": 8
# }
# {
#   "geohashrs": "r3gx2xyg"
# }
#
# geoPlugin:
# {
#   "latitude": -33.494, "longitude": 143.2104, "precision": 8
# }
# {
#   "geohashrs": "r4jc6yde"
# }
#
#-------------------------------------------------------------------------------------------
@app.post("/geohashrs/encode")
async def encode_using_geohashrs(location: GeoHashRequest):
    geohash = geohash_encode(location.latitude, location.longitude, location.precision)
    return {"geohashrs": geohash}
# ==========================================================================================


# ==========================================================================================
# geohash2
# - https://pypi.org/project/geohash2/
#
# ipwhois:
# {
#   "latitude": -33.83965, "longitude": 151.20541,  "precision": 8
# }
# {
#   "geohashrs": "r3gx2z8m"
# }
#
# ipinfo:
# {
#   "latitude": -33.8386, "longitude": 151.2033, "precision": 8
# }
# {
#   "geohashrs": "r3gx2xyg"
# }
#
# geoPlugin:
# {
#   "latitude": -33.494, "longitude": 143.2104, "precision": 8
# }
# {
#   "geohashrs": "r4jc6yde"
# }
#
#-------------------------------------------------------------------------------------------
@app.post("/geohash2/encode")
async def encode_using_geohash2(location: GeoHashRequest):
    geohash = geohash2.encode(location.latitude, location.longitude, precision = location.precision)
    return {"geohash2": geohash}
# ==========================================================================================


# ==========================================================================================
# IPWHOIS.IO
#   - https://ipwhois.io/documentation
IP_WHO_IS_API = "https://ipwhois.app/json/{ip_address}"
# IP_WHO_IS_API = "https://ipwhois.app/json/209.53.249.193?objects=latitude,longitude"
#
# {
#   "ip": "202.124.92.191",
#   "success": true,
#   "type": "IPv4",
#   "continent": "Oceania",
#   "continent_code": "OC",
#   "country": "Australia",
#   "country_code": "AU",
#   "country_flag": "https://cdn.ipwhois.io/flags/au.svg",
#   "country_capital": "Canberra",
#   "country_phone": "+61",
#   "country_neighbours": "",
#   "region": "New South Wales",
#   "city": "North Sydney",
#   "latitude": "-33.83965",
#   "longitude": "151.20541",
#   "asn": "",
#   "org": null,
#   "isp": null,
#   "timezone": "Australia/Sydney",
#   "timezone_name": "Australian Eastern Daylight Time",
#   "timezone_dstOffset": "3600",
#   "timezone_gmtOffset": "36000",
#   "timezone_gmt": "GMT +10:00",
#   "currency": "Australian Dollar",
#   "currency_code": "AUD",
#   "currency_symbol": "$",
#   "currency_rates": "1.289489",
#   "currency_plural": "Australian dollars",
#   "completed_requests": 0
# }
#
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
#
# {
#   "ip": "202.124.92.191",
#   "city": "The Rocks",
#   "region": "New South Wales",
#   "country": "AU",
#   "loc": "-33.8386,151.2033",
#   "postal": "2060",
#   "timezone": "Australia/Sydney",
#   "readme": "https://ipinfo.io/missingauth"
# }
#
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
#
# {
#   "geoplugin_request": "202.124.92.191",
#   "geoplugin_status": 206,
#   "geoplugin_delay": "1ms",
#   "geoplugin_credit": "Some of the returned data includes GeoLite data created by MaxMind, available from <a href='http://www.maxmind.com'>http://www.maxmind.com</a>.",
#   "geoplugin_city": "",
#   "geoplugin_region": "",
#   "geoplugin_regionCode": "",
#   "geoplugin_regionName": "",
#   "geoplugin_areaCode": "",
#   "geoplugin_dmaCode": "",
#   "geoplugin_countryCode": "AU",
#   "geoplugin_countryName": "Australia",
#   "geoplugin_inEU": 0,
#   "geoplugin_euVATrate": false,
#   "geoplugin_continentCode": "OC",
#   "geoplugin_continentName": "Oceania",
#   "geoplugin_latitude": "-33.494",
#   "geoplugin_longitude": "143.2104",
#   "geoplugin_locationAccuracyRadius": "1000",
#   "geoplugin_timezone": "Australia/Sydney",
#   "geoplugin_currencyCode": "AUD",
#   "geoplugin_currencySymbol": "$",
#   "geoplugin_currencySymbol_UTF8": "$",
#   "geoplugin_currencyConverter": 1.2928
# }
#
#-------------------------------------------------------------------------------------------
@app.get("/geoplugin/{ip_address}")
async def get_location_from_geoplugin(ip_address: str):
    async with AsyncClient() as client:
        url = GEO_PLUGIN_API.format(ip_address=ip_address)
        # print(url)
        response = await client.get(url)
    return response.json()
# ==========================================================================================