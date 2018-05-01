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
cr.execute("""select style_id from styles minus select style_id from interiors""")
style_tup=cr.fetchall()
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='TopSecret'
for style in style_tup:
    style_id=style[0]
    print style_id
    interior_url=v_api + 'styles/' + str(style_id) + '/equipment?availability=standard&equipmentType=OTHER&name=INTERIOR_DIMENSIONS&fmt=json&api_key=' + a_key
    interior_info=json.load(urllib2.urlopen(interior_url))
    print interior_info
    try:
        attr=interior_info['equipment'][0]['attributes']
    except:
        cr.execute("""insert into interiors values(:1,:2,:3,:4,:5)""",[style_id,'0.00001','0.00001','0.00001','0.00001'])
        db.commit()
        sleep(random()/45)
        continue
    a_dict={}
    for attribute in attr:
        a_dict[attribute['name']]=attribute['value']
        if '1st Row Leg Room' in a_dict:
            leg_room=a_dict['1st Row Leg Room']
        else:
            leg_room='0.00001'
        if '1st Row Head Room' in a_dict:
            head_room=a_dict['1st Row Head Room']
        else:
            head_room='0.00001'
        if '1st Row Shoulder Room' in a_dict:
            shoulder_room=a_dict['1st Row Shoulder Room']
        else:
            shoulder_room='0.00001'
        if 'Epa Interior Volume' in a_dict:
            volume=a_dict['Epa Interior Volume']
        else:
            volume='0.00001'
    insert_values=[style_id,volume,leg_room,head_room,shoulder_room]
    print insert_values
    sql_string="""
        merge into interiors e
        using (
            select '""" + str(style_id) + """' style_id,
                   '""" + volume        + """' volume,
                   '""" + leg_room      + """' leg_room,
                   '""" + head_room     + """' head_room,
                   '""" + shoulder_room + """' shoulder_room
            from dual) d
        on (e.style_id = d.style_id)
        when matched then
            update set  e.volume        = d.volume,
                        e.leg_room      = d.leg_room,
                        e.head_room     = d.head_room,
                        e.shoulder_room = d.shoulder_room
        when not matched then
            insert (style_id,volume,leg_room,head_room,shoulder_room)
            values(:1,:2,:3,:4,:5)
        """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    sleep(random()/45)
db.close()
