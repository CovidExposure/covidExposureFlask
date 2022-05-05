# covidExposureFlask
## APIs
###  Auth
```
POST /signup {"email": string, "password": string, "name": string}
POST /login {"email": string, "password": string, "remember": boolean}
GET /logout
```

### Business
```
GET /business
POST /business {"county": string, "latitude": float, "longitude": float, "name": string, "state": string, "type": string, "zipcode": int}
GET /busiess/<business_id>/checkin
```

### Visitor
```
GET /visitor/test_record
POST /visitor/test_record {"is_positive": boolean, "time_tested": float}
GET /visitor/status
```
## Example
```
$ python test/integ_test.py
```
