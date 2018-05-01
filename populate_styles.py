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
myear="2017"
cr.execute("""select make_id from makes""")
make_tup=cr.fetchall()
print make_tup
make_lst= list(zip(*make_tup)[0])
cr.execute("""select model_id from models""")
model_tup=cr.fetchall()
model_lst=list(zip(*model_tup)[0])
cr.execute("""select style_id from styles""")
style_tup=cr.fetchall()
style_lst=list(zip(*style_tup)[0])
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='r3crmsprc92pcyhnc6jkuqhe'
makes_url=v_api + '/makes?state=new&year=' + myear + '&view=basic&fmt=json&api_key=' + a_key
makes=json.load(urllib2.urlopen(makes_url))
for make in makes['makes']:
    make_name=make['niceName']
    make_id=make['id']
    print make_name
    cr.execute("""merge into makes m 
                using (select '""" + str(make_id) + """' make_id,'""" + make_name + """' nicename
                      from dual) d
                on (m.make_id = d.make_id)
                when matched then
                    update set m.nicename = d.nicename
                when not matched then
                    insert (make_id,nicename) 
                    values(:1,:2)""",[make_id,make_name])
    db.commit()
    if not make_id in make_lst:
        make_lst.append(make_id)
        print make_lst
        print 'Added new make ' + str(make_id)
        print make_name
    style_url=v_api + make_name + '/models?state=new&year=' + myear + '&view=basic&fmt=json&api_key=' + a_key
    styles=json.load(urllib2.urlopen(style_url))
    for model in styles['models']:
        model_name=model['niceName']
        print '  ' +  model_name
        model_id=model['years'][0]['id']
        year=str(model['years'][0]['year'])
        cr.execute("""merge into models m
                    using (select '""" + str(model_id) + """' model_id,'""" + str(make_id) + """' make_id,
                          '""" + year + """' year,'""" + model_name + """' nicename
                        from dual) d
                    on (m.model_id = d.model_id)
                    when matched then
                        update set m.nicename = d.nicename
                    when not matched then
                        insert (model_id,make_id,year,nicename) 
                        values(:1,:2,:3,:4)""",[model_id,make_id,year,model_name])
        db.commit()
        if not model_id in model_lst:
            model_lst.append(model_id)
            print 'Added new model ' + str(model_id)
            print model_name
        for style in model['years'][0]['styles']:
            style_name=style['name']
            print '       ' + style_name
            style_id=style['id']
            submodel=style['submodel']['niceName']
            if not style_id in style_lst:
                style_detail_url=v_api + '/styles/' + str(style_id) + '?view=full&fmt=json&api_key=' + a_key
                st_details=json.load(urllib2.urlopen(style_detail_url))
                if 'id' in st_details['engine']:
                    engine_id=st_details['engine']['id']
                else:
                    engine_id='0'
                if 'id' in st_details['transmission']:
                    trans_id=st_details['transmission']['id']
                else:
                    trans_id='0'
                driv_wheels=st_details['drivenWheels']
                doors=st_details['numOfDoors']
                msrp=str(st_details['price']['baseMSRP'])            
                deliv_charge=str(st_details['price']['deliveryCharges'])
                style_spec_url=(v_api + '/styles/' + str(style_id) + 
                            '/equipment?availability=standard&equipmentType=OTHER&name=SPECIFICATIONS&fmt=json&api_key='
                            + a_key)
                st_spec=json.load(urllib2.urlopen(style_spec_url))
                try:
                    attr=st_spec['equipment'][0]['attributes']
                    a_dict={}
                    for attribute in attr:
                        a_dict[attribute['name']]=attribute['value']
                    if 'Tco Curb Weight' in a_dict:
                        weight=a_dict['Tco Curb Weight'] 
                    elif 'Curb Weight' in a_dict:
                        weight=a_dict['Curb Weight']
                    else:
                        weight='99999'
                    if 'Epa Combined Mpg' in a_dict:
                        combined=a_dict['Epa Combined Mpg']
                    else:
                        combined='.000001'
                    if 'Manufacturer 0 60mph Acceleration Time (seconds)' in a_dict:
                        zeroto60=a_dict['Manufacturer 0 60mph Acceleration Time (seconds)']
                    else:
                        zeroto60='99999.0'
                    if 'Aerodynamic Drag (cd)' in a_dict:
                        drag_co=a_dict['Aerodynamic Drag (cd)']
                    else:
                        drag_co='99999.0'
                except:
                    drag_co=zeroto60=weight='99999'
                    combined='.000001'
                style_dim_url=(v_api + '/styles/' + str(style_id) + 
                            '/equipment?availability=standard&equipmentType=OTHER&name=EXTERIOR_DIMENSIONS&fmt=json&api_key='
                            + a_key)
                st_dim=json.load(urllib2.urlopen(style_dim_url))
                a_dict={}
                try:
                    attr=st_dim['equipment'][0]['attributes']
                    for attribute in attr:
                        a_dict[attribute['name']]=attribute['value']
                    if 'Overall Width Without Mirrors' in a_dict:
                        width=a_dict['Overall Width Without Mirrors']
                    elif 'Overall Width With Mirrors' in a_dict: 
                        width=a_dict['Overall Width With Mirrors']
                    else:
                        width='99999'
                    if 'Overall Height' in a_dict:
                        height=a_dict['Overall Height']
                    else:
                        height='99999'
                    if 'Overall Length' in a_dict:
                        length=a_dict['Overall Length'] 
                    else:
                        length='99999'
                except:
                    width=height=length='99999'
                insert_values=[style_id,model_id,make_id,style_name,submodel,engine_id,trans_id,driv_wheels,
                            doors,msrp,deliv_charge,weight,combined,zeroto60,drag_co,width,height,length]
                sql_string= """
                    merge into styles s using (
                    select '""" + str(style_id) + """' style_id,
                    '""" + str(make_id) + """' make_id,
                    '""" + str(model_id) + """' model_id,
                    '""" + style_name + """' style_name,
                    '""" + submodel + """' submodel,
                    '""" + engine_id + """' engine_id,
                    '""" + trans_id + """' trans_id,
                    '""" + driv_wheels + """' driv_wheels,
                    '""" + doors + """' doors,
                    '""" + msrp + """' msrp,
                    '""" + deliv_charge + """' deliv_charge,
                    '""" + weight + """' weight,
                    '""" + combined + """' combined,
                    '""" + zeroto60 + """' zeroto60,
                    '""" + drag_co + """' drag_co,
                    '""" + width + """' width,
                    '""" + height + """' height,
                    '""" + length + """' length 
                    from dual) d 
                    on (s.style_id = d.style_id ) 
                    when matched then 
                        update set  s.style_name = d.style_name,
                     s.make_id = d.make_id, 
                     s.model_id = d.model_id, 
                     s.submodel = d.submodel, 
                     s.engine_id = d.engine_id,
                     s.trans_id = d.trans_id, 
                     s.driv_wheels = d.driv_wheels,
                     s.doors = d.doors,
                     s.msrp = d.msrp, 
                     s.deliv_charge = d.deliv_charge,
                     s.weight = d.weight,
                     s.combined = d.combined, 
                     s.zeroto60 = d.zeroto60,
                     s.drag_co = d.drag_co,
                     s.width = d.width, 
                     s.height = d.height,
                     s.length = d.length 
                    when not matched then 
                        insert (style_id,
                        model_id,
                        make_id,
                        style_name,
                        submodel,
                        engine_id,
                        trans_id,
                        driv_wheels, 
                        doors,
                        msrp,
                        deliv_charge,
                        weight,
                        combined,
                        zeroto60,
                        drag_co,
                        width,
                        height,
                        length) 
                        values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18)
                    """
                cr.execute(sql_string,insert_values)
                db.commit()
                style_lst.append(style_id)
                print 'Added new style ' + str(style_id)
                print style_name
                sleep(random()/45) 
db.close()

