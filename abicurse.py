#!/usr/bin/python
import restful_lib
from lxml import etree
from lxml import objectify

base_uri = "http://10.60.20.30/api"
conn = restful_lib.Connection(base_uri, username="aboldu", password="23invaders")

def getobj(res):
    r = conn.request_get(res)
    obj =  objectify.fromstring(r["body"].encode('ascii', 'replace'))
    return obj

# for ent in ents.enterprise: 
def print_vms():
    ents = getobj("/admin/enterprises")
    for ent in ents.enterprise :
       vms = getobj("/admin/enterprises/"+str(ent.id)+"/action/virtualmachines") 
       if vms.countchildren() != 0:
           for vm in vms.virtualMachine:
               # Basic information
               print "+-------------------------------------------------------+"
               print "Virtual Machine: "+vm.name
               print "ID: "+str(vm.id)
               try:
                   vm.description
               except AttributeError:
                   print "Description:"
               else:
                   print "Description: "+vm.description
               print "State: "+vm.state
               print "CPU Cores: "+str(vm.cpu)
               print "HD: "+str(vm.hdInBytes / 1024)+" Mb"
               print "RAM: "+str(vm.ram)+" Mb"
               try:
                   vm.vdrpIP
               except AttributeError:
                   print "Remote access: No"
               else:
                   print "Remote access: "+str(vm.vdrpIP)+":"+str(vm.vdrpPort)

               for c in vm.getchildren():
                   # Owner
                   if c.values() and c.values()[2] == 'user':
                       user_url = c.values()[0]
                       user = getobj(user_url[user_url.rfind("api")+3:])
                       try:
                           user.nick
                       except AttributeError:
                           print "Owner: None"
                       else:
                           print "Owner: "+str(user.nick)
                   # API URL
                   if c.values() and c.values()[2] == 'edit':
                       api_url = c.values()[0]
                       print "API URL: "+str(api_url)

                   # DC
                   if c.values() and c.values()[2] == 'datacenter':
                       dc_url = c.values()[0]
                       dc = getobj(dc_url[dc_url.rfind("api")+3:])
                       print "Datacenter: "+str(dc.name)

                   # VDC
                   if c.values() and c.values()[2] == 'virtualdatacenter':
                       vdc_url = c.values()[0]
                       vdc = getobj(vdc_url[vdc_url.rfind("api")+3:])
                       print "Virtual datacenter: "+str(vdc.name)

                   # VAPP
                   if c.values() and c.values()[2] == 'virtualappliance':
                       vapp_url = c.values()[0]
                       vapp = getobj(vapp_url[vapp_url.rfind("api")+3:])
                       print "Virtual appliance: "+str(vapp.name)


                   # Storage



                   # Networking



                   # Get related template
                   if c.values() and c.values()[2] == 'virtualmachinetemplate':
                       template_url = c.values()[0]
                       template = getobj(template_url[template_url.rfind("api")+3:])
                       print "Template: "+str(template.name)
                       print "Template path: "+template.path
               print "+-------------------------------------------------------+"
               print ""


print_vms()


