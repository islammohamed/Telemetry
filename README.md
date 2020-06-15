# Code test

## GPS Tracker
This application is providing a simple functionality to track GPS, provide simple Restful API.

### Create a new route

<b>POST</b> /routes/2020-06-15/longest/

```
curl -X POST http://127.0.0.1:8000/routes/
```

### Create a new route way point

<b>POST</b> /routes/2020-06-15/longest/
```
curl http://127.0.0.1:8000/routes/d2813fee-5faf-4ad1-aac3-914ce01c438e/way_point/ -d '{"lat": -25.4025905, "lon": -49.3124416}'  -H "Content-Type:application/json" 
```

### Get route length

<b>GET</b> /routes/d2813fee-5faf-4ad1-aac3-914ce01c438e/length/
```
curl http://127.0.0.1:8000/routes/d2813fee-5faf-4ad1-aac3-914ce01c438e/length/ 
```



### Get the longest route for a given day 

<b>POST</b> /routes/2020-06-15/longest/

 
```
curl http://127.0.0.1:8000/routes/2020-06-13/longest/
```



## Requirements
- Python 3.7+
- Django 3.0
- POSTGRES with POSTGIS


## Setup instructions

### Build
```
docker-compose build
```
### Run Migration
```
docker-compose exec web python manage.py migrate --noinput
```

### Run tests
```
docker-compose exec web python manage.py test
```

