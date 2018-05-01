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
cr.execute("""merge into tco t
                using (select style_id from styles ) s
                on (t.style_id = s.style_id)
                when not matched then
                    insert (style_id, tco)
                    values (s.style_id,999999999) 
           """)        
cr.execute("""select style_id from tco where  tco = 999999999 """)
style_tup=cr.fetchall()
v_api='https://api.edmunds.com/v1/api/tco/'
a_key='TopSecret'
for style in style_tup:
    style_id=str(style[0])
    tco=999999999
    print style_id
    print tco
    tco_url=v_api + 'newtruecosttoownbystyleidandzip/' + style_id + '/41018' + '?fmt=json&api_key=' + a_key
    print tco_url
    try:
        tco_info=json.load(urllib2.urlopen(tco_url))
    except urllib2.HTTPError, error:
        contents = error.read()
        print contents
        if "TCO is not supported for style id" in contents:
            continue
    print tco_info
    tco=tco_info['value']
    print tco
    insert_values=[style_id, tco]
    print insert_values
    sql_string="""
        merge into  tco e
        using (
            select '""" + style_id + """' style_id,
                   '""" + str(tco) + """' tco
            from dual) d
        on (e.style_id = d.style_id)
        when matched then
            update set  e.tco = d.tco  
        when not matched then
            insert (style_id,
                    tco)
            values(:1,:2)
     """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    sleep(random()/45)
db.close()
