# Alfen API endpoints

## General info
All `GET` requests will deliver content with the content type `{'content-type': 'alfen/json; charset=utf-8'}`.

For `POST` requests you have to use `{'content-type': 'application/json'}`.

Before each request you have to login first and logout afterwards. The sessions are managed by the wallbox and you don't need to set a session token or something similar, I guess the wallbox uses the IP adress to authenticate the requests.

The info API doesn't need authentication / a login request.

The wallbox uses an invalid self signed certificate, you need to disable all SSL checks to perform the API calls.

## Login
`HTTP POST https://<HOST_IP>/api/login`
```
{
    "username": "admin",
    "password": ""
}
```

## Logout
`HTTP POST https://<HOST_IP>/api/logout`


## Info
`HTTP GET https://<HOST_IP>/api/info`

## Restart
`HTTP POST https://<HOST_IP>/api/cmd`
```
{"command":"reboot"}
```

## Log
`HTTP GET https://<HOST_IP>/api/log?offset=<OFFSET>`

>Default offset (256)

# Props (POST)

`HTTP POST https://<HOST_IP>/api/prop`

Sample Request
```
{
    "216C_0": {
        "id": "216C_0",
        "value": 2
    }
}
```

# Props (GET)
`HTTP GET https://<HOST_IP>/api/prop?ids=<PROP_CODES>`

Sample Response
```
{
    "version": 2,
    "properties": [
        {
            "id": "2060_0",
            "access": 1,
            "type": 27,
            "len": 0,
            "cat": "generic",
            "value": 6271674
        },
        {
            "id": "2056_0",
            "access": 1,
            "type": 7,
            "len": 0,
            "cat": "generic",
            "value": 27
        },
        {
            "id": "2221_3",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 222.19999694824219
        },
        {
            "id": "2221_4",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 222.29998779296875
        },
        {
            "id": "2221_5",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 221.97000122070312
        },
        {
            "id": "2221_A",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 4.56500005722046
        },
        {
            "id": "2221_B",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 0
        },
        {
            "id": "2221_C",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 0
        },
        {
            "id": "2221_16",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "meter1",
            "value": 981.4000244140625
        },
        {
            "id": "2201_0",
            "access": 1,
            "type": 8,
            "len": 0,
            "cat": "temp",
            "value": 42.875
        }
    ],
    "offset": 0,
    "total": 10
}
```

### Alfen prop codes

| Code | description | unit |
| ----------- | ----------- | --- |
|2060_0| system uptime| /1000 for minutes |
|2056_0| Number of bootups| |
|2221_3| Voltage L1| V |
|2221_4| Voltage L2| V |
|2221_5| Voltage L3| V |
|2221_A| Current L1| A |
|2221_B| Current L2| A |
|2221_C| Current L3| A |
|2221_16| Active power total | /1000 for kW |
|2201_0| Temperature| C |
|2501_2| State |  |

### Alfen states (2501_2)
|ID|Value|
|----|----|
|4|Charge point available|
|7|Cable connected|
|10|Vehicle connected, start (Charging stopped)|
|11|Normal Charging|
# Firmware
`HTTP GET https://<HOST_IP>/api/firmware`

Sample response
```
{
    "OD_fileFirmwareUpdateStatus": {
        "id": "2911_0",
        "value": 0
    },
    "uploadInProgress": false,
    "version": 2
}
```
