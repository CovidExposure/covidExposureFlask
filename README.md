# covidExposureFlask
## Run Example
Navigate to parent directory (covidExposureFlask/../):
```
$ export FLASK_APP=covidExposureFlask
$ flask run
```

In another terminal:
```
$ python covidExposureFlask/test/integ_test.py
```

## APIs
### Auth
```
POST /signup {"email": string, "password": string, "name": string}
POST /login {"email": string, "password": string, "remember": boolean}
GET /logout
```

### Business
```
GET /business
POST /business {"country": string, "latitude": float, "longitude": float, "name": string, "state": string, "city": string, "address1": string, "address2": (optional) string, "zipcode": string, "category": string}
GET /busiess/<business_id>/checkin
```

### Visitor
```
GET /visitor/test_record
POST /visitor/test_record {"is_positive": boolean, "time_tested": float}
GET /visitor/status
```
