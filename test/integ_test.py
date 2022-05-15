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

test_session_1.post(host+"/business", data={"country":"US","name":"Donald Bren Hall (DBH)","state":"CA","city":"Irvine","address1":"Donald Bren Hall","zipcode":"92697"})
test_session_1.post(host+"/business", data={"country":"AU","name":"Gelato Messina Randwick","state":"NSW","city":"Randwick","address1":"162 Barker Street","address2":"Shop G08 & G08a","zipcode":"2031"})
r = test_session_1.get(host+"/business")
r.raise_for_status()
business_id_1 = None
business_id_2 = None
for business in r.json():
    if business['name'] == "Donald Bren Hall (DBH)":
        business_id_1 = business['id']
        assert(int(business['location']['latitude']) == 33)
        assert(int(business['location']['longitude']) == -117)
    elif business['name'] == "Gelato Messina Randwick":
        business_id_2 = business['id']
        assert(int(business['location']['latitude']) == -33)
        assert(int(business['location']['longitude']) == 151)
assert(business_id_1)
assert(business_id_2)


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
test_session_2.post(host+"/visitor/test_record",data={"isPositive":True,"timeTested":datetime.isoformat(datetime.now())}).raise_for_status()
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