#!/usr/bin/python
import restful_lib
from lxml import etree
from lxml import objectify

base_url = "http://10.60.10.250:8009/api"
conn = restful_lib.Connection(base_url, username="admin", password="xabiquo")
dc = conn.request_get("/admin/datacenters")
dc_tree = etree.fromstring(dc["body"].encode('ascii', 'replace'))
dc_obj =  objectify.fromstring(dc["body"].encode('ascii', 'replace'))

users = conn.request_get("/admin/enterprises/1/users")
users_obj =  objectify.fromstring(users["body"].encode('ascii', 'replace'))

i = users_obj.totalSize
u = users_obj.user
while i > 0:
   print u.nick
   u = u.getnext()
   i = i - 1


