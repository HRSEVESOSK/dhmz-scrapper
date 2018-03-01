#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json,pgsql
from urllib2 import urlopen
#from urllib.request import urlopen
from datetime import datetime
import xml.etree.ElementTree as ET

print("****** Scrapper process started on '%s' \n" % datetime.now().isoformat())
connection = pgsql.PGSql()
xmlUrl = "http://vrijeme.hr/hrvatska_n.xml"
response = urlopen(xmlUrl)
tree = ET.parse(response)
root = tree.getroot()
date = root[0][0].text.split(".")
timeCheck = root[0][1].text
dateTimeString = date[2] + "-" + date[1] + "-" + date[0] + "T" + timeCheck + ":00:00"
print("Processing observations for datetime: '%s'" % dateTimeString)
for grad in root.findall('Grad'):
    gradId = (grad.find('GradIme').text).replace(" ","_").replace("(","").replace(")","")
    gradIme = grad.find('GradIme').text
    gradLat = grad.find('Lat').text
    gradLon = grad.find('Lon').text
    sql="SELECT oid FROM grad WHERE id='%s'" % gradId
    connection.connect()
    gradExists = connection.query(sql, False)
    connection.close()
    if not gradExists:
        metadata = ''
        sql = "INSERT INTO grad (id,geom) VALUES ('%s', ST_SetSRID(ST_MakePoint(%s, %s),4326)) RETURNING OID" % (gradId,gradLon,gradLat)
        connection.connect()
        insertGrad = connection.query(sql,False)
        connection.close()
        gradOID = insertGrad[0][0]
        print("Inserting new FOI:'%s'" % gradOID)
    else:
        sql = "SELECT oid FROM grad WHERE id='%s'" % gradId
        connection.connect()
        selectGrad = connection.query(sql, False)
        connection.close()
        gradOID = selectGrad[0][0]
    if gradOID:
        sql = 'SELECT time::timestamp from observation where grad_ref = %s order by time desc' % gradOID
        connection.connect()
        lastObsDateTime = connection.query(sql, False)
        connection.close()
        if not lastObsDateTime or (lastObsDateTime[0][0]).isoformat() != dateTimeString:
            print("Inserting Observations for grad '%s' and time '%s'" % (gradOID,(dateTimeString)))
            data = {}
            for obs in root.findall(".//Grad[GradIme='%s']/Podatci/*" % grad.find('GradIme').text):
                table = 'obs'
                data[obs.tag] = obs.text
            json_data = json.dumps(data, ensure_ascii=False)
            sql="INSERT INTO observation (time,grad_ref,data) VALUES ('%s',%s,'%s')" % (dateTimeString, gradOID, json_data)
            connection.connect()
            insertObservation = connection.query(sql, False)
            connection.close()
            if(insertObservation):
                print("Observations '%s' succesfully inserted for time '%s' and FOI '%s'" % (json_data,dateTimeString,gradOID))
            else:
                print("Failed insert for observations '%s' succesfully inserted for time '%s' and FOI '%s'" % (json_data, dateTimeString, gradOID))
        else:
            print("Observations for grad '%s' and time '%s' are already stored in the database" % (gradOID,(lastObsDateTime[0][0]).isoformat()))
            continue
    else:
        print("Process could not get/insert FOI for '%s'" % gradId)
print("\n****** Scrapper process finished on '%s' \n" % datetime.now().isoformat())