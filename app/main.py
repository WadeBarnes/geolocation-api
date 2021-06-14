from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel
from enum import Enum

import os
import ipaddress
from httpx import AsyncClient
import geohash2
from geohashrs import geohash_encode
import geohashlite
from pygeodesy import geohash as pygeodesy_geohash

from GeoApis import GeoApis
import json


tags_metadata = [
    {
        "name": "IP Address APIs",
        "description": "APIs for looking up the Geolocation of an API Address.",
    },
    {
        "name": "Geohash APIs",
        "description": "APIs for encoding lat/long as a Geohash.",
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

# Other References:
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

class GeoHashEncoder(str, Enum):
    pygeodesy = "pygeodesy"
    geohashlite = "geohashlite"
    geohashrs = "geohashrs"
    geohash2 = "geohash2"


@app.post("/encode",
    name="Geohash Encode",
    summary="Encodes a location (specified as lat/long) into a Geohash",
    tags=["Geohash APIs"],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example":{"geohash": "r4jc6yde"}
                }
            }
        }
    }
)
async def encode_using_geohash2(location: GeoHashRequest = Body(..., example={"latitude": -33.494, "longitude": 143.2104, "precision": 8}),
                                encoder: Optional[GeoHashEncoder] = Query(GeoHashEncoder.geohashrs)):
    """Encodes a location specified as lat/long into a Geohash.
    Supports the following Geohash encoders:

    **[geohashlite](https://pypi.org/project/geohashlite)**
    - MIT License
    - One dependancy
    - Last Update:  July, 31st 2019
    - More features than needed.

    **[geohashrs](https://pypi.org/project/geohashrs)**
    - Apache-2.0 License
    - Some dependancies.  I think for building, it's a Rust implementation.
    - Last Update: Aug 9th 2020
    - Has features needed.

    **[geohash2](https://pypi.org/project/geohash2/)**
    - AGPL-3.0 License
    - Has dependancies
    - Last Update: July 6th 2017
    - Has features needed.    

    **[PyGeodesy](https://pypi.org/project/PyGeodesy)**
    - MIT License
    - No dependancies?
    - Last Update:  June, 4th 2021
    - Way more features than needed.
    """

    if encoder == GeoHashEncoder.geohash2:
        geohash = geohash2.encode(location.latitude, location.longitude, precision = location.precision)
    elif encoder == GeoHashEncoder.geohashlite:
        geohash = geohashlite.encode(location.latitude, location.longitude, location.precision)
    elif encoder == GeoHashEncoder.geohashrs:
        geohash = geohash_encode(location.latitude, location.longitude, location.precision)
    elif encoder == GeoHashEncoder.pygeodesy:
        geohash = pygeodesy_geohash.encode(location.latitude, location.longitude, location.precision)
    else:
        raise HTTPException(status_code=400, detail=f"Invalid geohash encoder; {encoder}")

    return {"geohash": geohash}


# Response Documentation Reference:
#   - https://fastapi.tiangolo.com/tutorial/schema-extra-example/#body-with-multiple-examples
@app.get("/{ip_address}",
    name="Get Geolocation of IP",
    summary="Returns the Geolocation for the specified IP Address.",
    tags=["IP Address APIs"],
    responses={
        200: {
            "description": "Examples from the various Geolocation APIS:",
            "content": {
                "application/json": {
                    "examples":{
                        "geoplugin": {
                            "summary": "Response from geoplugin",
                            "description": "**geoplugin**.\
                                \n\n This API does not appear to support an https endpoint\
                                \n - [geoPlugin](https://www.geoplugin.com)\
                                \n - [geoPlugin - JSON Geolocation Web Service](https://www.geoplugin.com/webservices/json)",
                            "value": {
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
                                "geoplugin_euVATrate": False,
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
                        },
                        "ipinfo": {
                            "summary": "Response from ipinfo",
                            "description": "**ipinfo**.\
                                \n - [ipinfo.io](https://ipinfo.io)\
                                \n - [How to find location with IP address in Python?](https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python/55432323#55432323)",
                            "value": {
                                "ip": "202.124.92.191",
                                "city": "The Rocks",
                                "region": "New South Wales",
                                "country": "AU",
                                "loc": "-33.8386,151.2033",
                                "postal": "2060",
                                "timezone": "Australia/Sydney",
                                "readme": "https://ipinfo.io/missingauth"
                            }
                        },
                        "ipwhois": {
                            "summary": "Response from ipwhois",
                            "description": "**ipwhois**.\
                                \n - [IPWHOIS.IO](https://ipwhois.io)\
                                \n - [IPWHOIS.IO - API Documentation](https://ipwhois.io/documentation)",
                            "value": {
                                "ip": "202.124.92.191",
                                "success": True,
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
                                "org": None,
                                "isp": None,
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
                        },
                    }
                }
            },
        },
        400: {
            "description": "Error Examples:",
            "content": {
                "application/json": {
                    "examples":{
                        "Invalid IP Address": {
                            "value": {"detail": "Invalid IP Address; 209.53.249"}
                        },
                        "Invalid Geolocation API": {
                            "value": {"detail":"Invalid Geolocation API; some_geo_api.  Valid values are, ['geoplugin', 'ipinfo', 'ipwhois']"}
                        }
                    }
                }
            },
        },
    }
)
async def get_location_for_ip(ip_address: str = Path(..., description="The IP address to lookup."),
                              api: Optional[str] = Query("geoplugin", description="The Geolocation API to use for the lookup.  Options; **geoplugin**, **ipinfo**, or **ipwhois**")):
    """Looks up the Geolocation for a specified IP Address
    """
    try:
        ipaddress.ip_address(ip_address)
    except:
        raise HTTPException(status_code=400, detail=f"Invalid IP Address; {ip_address}")

    if not api in api_collection.keys:
        raise HTTPException(status_code=400, detail=f"Invalid Geolocation API; {api}.  Valid values are, {[*api_collection.keys]}")

    async with AsyncClient() as client:
        url = api_collection.get_ip_api(api, ip_address)
        response = await client.get(url)
    return response.json()