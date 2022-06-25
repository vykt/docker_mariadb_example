# docker_mariadb_example
Flask &amp; Mariadb running a REST API on a debian-slim docker container.

### INSTALLATION:

Pull debian:bullseye image:
```
docker pull debian:bullseye
```

Build the API image:
```
docker build -t debian-flask-restapi:bullseye .
```


### RUN:

Launch via docker-compose:
```
docker-compose up
```

You can connect to the API on:
```
localhost:5001
```

Alternatively, to get the IP of the container run:
```
docker inspect debian-flask-restapi_container | grep IP
```

Then connect, port 5000 if via this method:
```
172.n.0.n:5000
```

### INTERACT WITH API:

API calls are passed via http headers in json format. There are 3 API calls:

**ADD SONG**:

```
HTTP POST
```


Takes:
```
'title'		- string, max length of 64, song name.
'artist'		- string, max length of 64, musician.
'resource'	- string, max length of 256, url to resource.
```

Returns:
```
'status'		- HTTP status code, 201 on success, 500 on fail.
```


**DELETE SONG**

```
HTTP DELETE
```


Takes:
```
'id'			- int, id of song, provided by LIST SONGS.
```

Returns:
```
'status'		- HTTP status code, 204 on success, 500 on fail.
```


**LIST SONGS**

Takes:
```
nothing
```

Returns, for each song:
```
'id':			- int, id of song.
	'title'		- string, song name.
	'artist'	- string, musician.
	'resource'	- string, url to resource.
```


### EXAMPLES:

Add "Provider" by Frank Ocean, located at https://invidious.weblibre.org/watch?v=XKQNJzquduI:
```
curl -X POST -H "title: Provider" -H "artist: Frank Ocean" -H "resource: https://invidious.weblibre.org/watch?v=XKQNJzquduI" localhost:5001
```

Remove "Post Rave Maximalist" by Machine Girl, id of 5:
```
curl -X DELETE -H "id: 5" localhost:5001
```

Get the stored songs:
```
curl -X GET localhost:5001
```
