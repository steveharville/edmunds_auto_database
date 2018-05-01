# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cx_Oracle
import os
import sys
import json
import urllib2
from random import random
from time import sleep

db = cx_Oracle.connect(os.getenv("CX_ORACLE_USERNAME"),
                       os.getenv("CX_ORACLE_PASSWORD"),
                       os.getenv("CX_ORACLE_TNSENTRY"))
print 'Database connection status : ' + str(db)
cr=db.cursor()
print 'Cursor status : ' + str(cr)
cr.execute("""select unique trans_id from styles""")
transmission_tup=cr.fetchall()
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='r3crmsprc92pcyhnc6jkuqhe'
for transmission in transmission_tup:
    trans_id=transmission[0]
    print trans_id
    transmission_url=v_api + 'transmissions/' + str(trans_id) + '?fmt=json&api_key=' + a_key
    trans_info=json.load(urllib2.urlopen(transmission_url))
    print trans_info
    trans_name=trans_info['name']
    print trans_name
    ttype=trans_info['transmissionType']
    try:
        speeds=int(trans_info['numberOfSpeeds'])
    except:
        speeds=9999
    insert_values=[trans_id,trans_name,ttype,speeds]
    print insert_values
    sql_string="""
        merge into transmissions e
        using (
            select '""" + str(trans_id) + """' trans_id,
                   '""" + trans_name    + """' trans_name,
                   '""" + ttype         + """' ttype,
                   '""" + str(speeds)   + """' speeds
            from dual) d
        on (e.trans_id = d.trans_id)
        when matched then
            update set  e.trans_name  = d.trans_name,
                        e.ttype       = d.ttype,
                        e.speeds      = d.speeds
        when not matched then
            insert (trans_id,
                    trans_name,
                    ttype,
                    speeds
                    )
            values(:1,:2,:3,:4)
        """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    sleep(random()/45)
db.close()
