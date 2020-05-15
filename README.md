# LicenseServer

## client control commands

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
NCMD # invalid command
GOOD # good to go
THNX # bye bye
```

## server RESTful API

```bash
/db
```

Get current database, including all key, uid, last_seen, and max.

```bash
/gen_key
/gen_key/:max
```

Generate new key, where max is optional.

```bash
/del_key/:key
```

Delete one existing key.

```bash
/del_uid/:key/:uid
```

Delete one existing uid.