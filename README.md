# COVID Exposure Backend

## Getting Started
0. Set up a Virtual Environment (Recommended)
   + [https://www.ics.uci.edu/~thornton/ics32/Notes/ThirdPartyLibraries/](https://www.ics.uci.edu/~thornton/ics32/Notes/ThirdPartyLibraries/)
1. Navigate to the project directory and execute `pip install -r requirements.txt`
2. Navigate to project's parent directory and run
   ```
   export FLASK_APP=covidExposureFlask
   flask run
   ```
3. Open another terminal and type `python covidExposureFlask/test/integ_test.py` (Windows) or `python3 covidExposureFlask/test/integ_test.py` (Linux)

## API Format
### Auth
```
POST /signup {"email": string, "password": string, "name": string}
POST /login {"email": string, "password": string, "remember": boolean}
POST /logout
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

## Docker Support
Dockerfile is in the repository
build using the command
```
docker build -f Dockerfile -t covidexposure ./ 
```
to run docker
```
docker run -ti -e FLASK_APP=covidExposure -p 5000:5000 covidexposure
```
