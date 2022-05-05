import requests
from datetime import datetime

test_session_1 = requests.session()
test_session_2 = requests.session()
test_session_3 = requests.session()
host = "http://127.0.0.1:5000"

test_session_1.post(host+"/signup", data={"email":"test1@test.com","password":"pass1","name":"test1"})
test_session_2.post(host+"/signup", data={"email":"test2@test.com","password":"pass2","name":"test2"})
test_session_3.post(host+"/signup", data={"email":"test3@test.com","password":"pass3","name":"test3"})
test_session_1.post(host+"/login", data={"email":"test1@test.com","password":"pass1","remember":True})
test_session_2.post(host+"/login", data={"email":"test2@test.com","password":"pass2","remember":True})
test_session_3.post(host+"/login", data={"email":"test3@test.com","password":"pass3","remember":True})

test_session_1.post(host+"/business", data={"county":"orange","latitude":111.11,"longitude":111.11,"name":"test_business_1","state":"CA","type":"TestType","zipcode":"00000"})
test_session_1.post(host+"/business", data={"county":"orange","latitude":222.11,"longitude":222.11,"name":"test_business_2","state":"CA","type":"TestType","zipcode":"00000"})
r = test_session_1.get(host+"/business")
r.raise_for_status()
business_id_1 = r.json()[0]['id']
business_id_2 = r.json()[1]['id']

test_session_1.get(host+"/business/%s/checkin" % business_id_1).raise_for_status()
test_session_2.get(host+"/business/%s/checkin" % business_id_1).raise_for_status()
test_session_1.get(host+"/business/%s/checkin" % business_id_2).raise_for_status()
test_session_3.get(host+"/business/%s/checkin" % business_id_2).raise_for_status()

r = test_session_1.get(host+"/visitor/status")
r.raise_for_status()
test_status_1 = r.json()

r = test_session_2.get(host+"/visitor/status")
r.raise_for_status()
test_status_2 = r.json()

r = test_session_3.get(host+"/visitor/status")
r.raise_for_status()
test_status_3 = r.json()

r = test_session_2.get(host+"/visitor/test_record")
r.raise_for_status()
test_record_2 = r.json()
test_session_2.post(host+"/visitor/test_record",data={"is_positive":True,"time_tested":datetime.timestamp(datetime.now())}).raise_for_status()
r = test_session_2.get(host+"/visitor/test_record")
r.raise_for_status()
assert(len(r.json()) > len(test_record_2))

r = test_session_1.get(host+"/visitor/status")
r.raise_for_status()
assert(len(r.json()) > len(test_status_1))
assert(r.json()[-1]['status'] == 'EXPOSED')

r = test_session_2.get(host+"/visitor/status")
r.raise_for_status()
assert(len(r.json()) > len(test_status_2))
assert(r.json()[-1]['status'] == 'POSITIVE')

r = test_session_3.get(host+"/visitor/status")
r.raise_for_status()
assert(r.json() == test_status_3)