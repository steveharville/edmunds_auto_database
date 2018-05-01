# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# copyright 2016 Steve Harville
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
cr.execute("""select unique engine_id from styles where engine_id > 0  
              minus
              select engine_id from engines""")
engine_tup=cr.fetchall()
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='TopSecret'
for engine in engine_tup:
    engine_id=engine[0]
    print engine_id
    engine_url=v_api + 'engines/' + str(engine_id) + '?fmt=json&api_key=' + a_key
    eng_info=json.load(urllib2.urlopen(engine_url))
    print eng_info
    eng_name=eng_info['name']
    print eng_name
    if 'cylinder' in eng_info:
        cylinder=eng_info['cylinder']
    else:
        cylinder=0
    if 'displacement' in eng_info:
        disp=eng_info['displacement']
    else:
        disp=0
    if 'configuration' in eng_info:
        config=eng_info['configuration']
    else:
        config='???'
    if 'fuelType' in eng_info:
        fuel=eng_info['fuelType']
    else:
        fuel='???'
    if 'horsepower' in eng_info:
        hp=eng_info['horsepower']
    else:
        hp=0.000001
    if 'torque' in eng_info:
        torque=eng_info['torque']
    else:
        torque=0.000001
    if 'type' in eng_info:
        eng_type=eng_info['type']
    else:
        eng_type='???'
    if 'compressorType' in eng_info:
        compressor=eng_info['compressorType']
    else:
        compressor='???'
    insert_values=[engine_id, eng_name, cylinder, disp, config,fuel, hp, torque, eng_type, compressor]
    print insert_values
    sql_string="""
        merge into engines e
        using (
            select '""" + str(engine_id) + """' engine_id,
                   '""" + eng_name       + """' eng_name,
                   '""" + str(cylinder)  + """' cylinder,
                   '""" + str(disp)      + """' disp,
                   '""" + config         + """' config,
                   '""" + fuel           + """' fuel,
                   '""" + str(hp)        + """' hp,
                   '""" + str(torque)    + """' torque,
                   '""" + eng_type       + """' eng_type,
                   '""" + compressor     + """' compressor
            from dual) d
        on (e.engine_id = d.engine_id)
        when matched then
            update set  e.eng_name  = d.eng_name,
                        e.fuel      = d.fuel,
                        e.hp        = d.hp,
                        e.torque    = d.torque,
                        e.compressor=d.compressor  
        when not matched then
            insert (engine_id,
                    eng_name,
                    cylinder,
                    disp,
                    config,
                    fuel,
                    hp,
                    torque,
                    eng_type,
                    compressor)
            values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)
        """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    sleep(random()/45)
db.close()
