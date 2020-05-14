# LicenseServer

## control commands

Control commands is ascii encoded.  
Client requests(70 Bytes, fixed-length):

```bash
HELO.$UID.$KEY # tell server that client process is up
GBYE.$UID.$KEY # tell server that client is offline
```

Server response(4 Bytes, fixed-length):

```bash
NKEY # key invalid
FULL # no sparing slot
GOOD # good to go
NCMD # invalid command
```
