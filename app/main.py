from typing import Optional
from fastapi import FastAPI, Path, Query
# from fastapi import FastAPI, Request, Query, Depends, Path, Body

from pydantic import BaseModel

import os
from httpx import AsyncClient
import geohash2
from geohashrs import geohash_encode
import geohashlite
from pygeodesy import geohash as pygeodesy_geohash

from GeoApis import GeoApis

tags_metadata = [
    {
        "name": "IP Address APIs",
        "description": "APIs for looking up the Geolocation of an API Address.",
    },
]

api_collection = GeoApis()
app = FastAPI(
    title = os.environ.get("APP_NAME"),
    description = os.environ.get("APP_DESCRIPTION"),
    version = os.environ.get("APP_VERSION"),
    openapi_tags=tags_metadata
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
# - MIT License
# - No dependancies?
# - Last Update:  June, 4th 2021
# - Way more features than needed.
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
# - MIT License
# - One dependancy
# - Last Update:  July, 31st 2019
# - More features than needed.
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
# - Apache-2.0 License
# - Some dependancies.  I think for building, it's a Rust implementation.
# - Last Update: Aug 9th 2020
# - Has features needed.
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
# - AGPL-3.0 License
# - Has dependancies
# - Last Update: July 6th 2017
# - Has features needed.
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


@app.get("/{ip_address}",
    name="Get Geolocation of IP",
    summary="Returns the Geolocation for the specified IP Address.",
    tags=["IP Address APIs"])
async def get_location_for_ip(ip_address: str = Path(..., description="The IP address to lookup."), 
                              api: Optional[str] = Query("geoplugin", description="The Geolocation API to use for the lookup.  Options; **geoplugin**, **ipinfo**, or **ipwhois**")):
    """Looks up the Geolocation for a specified IP Address

    Example Responses:

    **geoplugin**
    - Does not appear to support an https endpoint
    - [geoPlugin - JSON Geolocation Web Service](https://www.geoplugin.com/webservices/json)
    ```
    {
    "geoplugin_request": "202.124.92.191",
    "geoplugin_status": 206,
    "geoplugin_delay": "1ms",
    "geoplugin_credit": "Some of the returned data includes GeoLite data created by MaxMind, available from <a href='http://www.maxmind.com'>http://www.maxmind.com</a>.",
    "geoplugin_city": "",
    "geoplugin_region": "",
    "geoplugin_regionCode": "",
    "geoplugin_regionName": "",
    "geoplugin_areaCode": "",
    "geoplugin_dmaCode": "",
    "geoplugin_countryCode": "AU",
    "geoplugin_countryName": "Australia",
    "geoplugin_inEU": 0,
    "geoplugin_euVATrate": false,
    "geoplugin_continentCode": "OC",
    "geoplugin_continentName": "Oceania",
    "geoplugin_latitude": "-33.494",
    "geoplugin_longitude": "143.2104",
    "geoplugin_locationAccuracyRadius": "1000",
    "geoplugin_timezone": "Australia/Sydney",
    "geoplugin_currencyCode": "AUD",
    "geoplugin_currencySymbol": "$",
    "geoplugin_currencySymbol_UTF8": "$",
    "geoplugin_currencyConverter": 1.2928
    }
    ```

    **ipinfo**
    - [ipinfo.io](https://ipinfo.io)
    - [How to find location with IP address in Python?](https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python/55432323#55432323)
    ```
    {
    "ip": "202.124.92.191",
    "city": "The Rocks",
    "region": "New South Wales",
    "country": "AU",
    "loc": "-33.8386,151.2033",
    "postal": "2060",
    "timezone": "Australia/Sydney",
    "readme": "https://ipinfo.io/missingauth"
    }
    ```

    **ipwhois**
    - [IPWHOIS.IO - API Documentation](https://ipwhois.io/documentation)
    ```
    {
    "ip": "202.124.92.191",
    "success": true,
    "type": "IPv4",
    "continent": "Oceania",
    "continent_code": "OC",
    "country": "Australia",
    "country_code": "AU",
    "country_flag": "https://cdn.ipwhois.io/flags/au.svg",
    "country_capital": "Canberra",
    "country_phone": "+61",
    "country_neighbours": "",
    "region": "New South Wales",
    "city": "North Sydney",
    "latitude": "-33.83965",
    "longitude": "151.20541",
    "asn": "",
    "org": null,
    "isp": null,
    "timezone": "Australia/Sydney",
    "timezone_name": "Australian Eastern Daylight Time",
    "timezone_dstOffset": "3600",
    "timezone_gmtOffset": "36000",
    "timezone_gmt": "GMT +10:00",
    "currency": "Australian Dollar",
    "currency_code": "AUD",
    "currency_symbol": "$",
    "currency_rates": "1.289489",
    "currency_plural": "Australian dollars",
    "completed_requests": 0
    }
    ```
    """
    async with AsyncClient() as client:
        url = api_collection.get_ip_api(api, ip_address)
        response = await client.get(url)
    return response.json()