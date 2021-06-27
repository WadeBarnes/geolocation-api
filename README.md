[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# Geolocation API

A simple Geolocation API based on [FastAPI](https://fastapi.tiangolo.com/), using [WadeBarnes/fastapi-example](https://github.com/WadeBarnes/fastapi-example) as the starting point.

The purpose of this project is to provide an API that can supply basic Geolocation information, such as latitude and longitude along with a geohash, for locations and IP addresses.

Refer to the API documentation for details on the available APIs and how to use them.

## Development Use:

### Help:
```
./manage -h
```

### Spin up the api container:

This command will spin up the API container and open a tab in your default browser to the documentation page where you can read about and interact with the various APIs.

```
./manage up
```

### Tear down the api container:
```
./manage down
```