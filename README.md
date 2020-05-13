# LicenseServer

## Client control commands

Control commands is sent in plain ascii form.  
Client requests:

```bash
HELO $UID.$KEY # tell server that client process is up
VALD $UID.$KEY # tell server that client is alive
GBYE $UID.$KEY # tell server that client is offline
```

Server response:

```bash
TICK # reply to HELO that client is valid
THNX # reply to GBYE that client exits normally
FAIL # reply to all requests
```

> TODO:  
> seems that commands can be simplified  
> eg. HELO and VALD is identical  
> eg. GBYE seems redundent to server  

## Server

Server stores keys and their users, in a structure as follows:

```json
{
    "d1221586-94b3-11ea-ae09-d43b04ce19a4": {
        "uid": {
            "e9b16108-94c5-11ea-bb37-0242ac130002": 1589338804.8976097,
            "c08aca5e-94c9-11ea-bb37-0242ac130002": 1589339031
        },
        "max": 50
    },
    "97df96fc-94c9-11ea-bb37-0242ac130002": {
        "uid": {
            "a98dd300-94c9-11ea-bb37-0242ac130002": 1589338898
        },
        "max": 100
    }
}
```

`key` should be dynamically generated from RestAPI(currently underconstruction)

## Client

User get `key` from WebUI, and client auto-generate its UID(eg. `UUID1`) on first run.
