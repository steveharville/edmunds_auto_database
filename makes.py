# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# copyright 2016 Steve Harville
import cx_Oracle
import os
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
cr.execute('''delete from styles''')
cr.execute('''delete from models''')
cr.execute('''delete from makes''')
db.commit()
myear="2016"
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='TopSecret'
makes_url=v_api + '/makes?state=new&year=' + myear + '&view=basic&fmt=json&api_key=' + a_key
makes=json.load(urllib2.urlopen(makes_url))
makecount=0
for make in makes['makes']:
    make_name=make['niceName']
    make_id=make['id']
    print make_name
    cr.execute('''insert into makes (make_id,nicename) 
                    values(:1,:2)''',[make_id,make_name]) 
    db.commit()
    for model in make['models']:
        model_name=model['niceName'] 
        model_id=model['years'][0]['id']
        year=model['years'][0]['year']
        cr.execute('''insert into models (model_id,make_id,year,nicename) 
                        values(:1,:2,:3,:4)''',[model_id,make_id,year,model_name])
        db.commit()
    style_url=v_api + make_name + '/models?state=new&year=' + myear + '&view=basic&fmt=json&api_key=' + a_key
    styles=json.load(urllib2.urlopen(style_url))
    for model in styles['models']:
        print '  ' + model['niceName']
        for style in model['years'][0]['styles']:
            style_name=style['name']
            style_id=style['id']
            submodel=style['submodel']['niceName']
            style_detail_url=v_api + '/styles/' + str(style_id) + '?view=full&fmt=json&api_key=' + a_key
            st_details=json.load(urllib2.urlopen(style_detail_url))
            engine_id=int(st_details['engine']['id'])
            trans_id=int(st_details['transmission']['id'])
            driv_wheels=st_details['drivenWheels']
            doors=int(st_details['numOfDoors'])
            msrp=st_details['price']['baseMSRP']            
            deliv_charge=st_details['price']['deliveryCharges']
            style_spec_url=(v_api + '/styles/' + str(style_id) + 
                            '/equipment?availability=standard&equipmentType=OTHER&name=SPECIFICATIONS&fmt=json&api_key='
                            + a_key)
            st_spec=json.load(urllib2.urlopen(style_spec_url))
            # print st_spec
            attr=st_spec['equipment'][0]['attributes']
            a_dict={}
            for attribute in attr:
                a_dict[attribute['name']]=attribute['value']
            # print a_dict
            if 'Tco Curb Weight' in a_dict:
                weight=int(a_dict['Tco Curb Weight']) 
            elif 'Curb Weight' in a_dict:
                weight=int(a_dict['Curb Weight'])
            else:
                weight=99999
            if 'Epa Combined Mpg' in a_dict:
                combined=int(a_dict['Epa Combined Mpg'])
            else:
                combined=.000001
            if 'Manufacturer 0 60mph Acceleration Time (seconds)' in a_dict:
                zeroto60=float(a_dict['Manufacturer 0 60mph Acceleration Time (seconds)'])
            else:
                zeroto60=99999.0
            if 'Aerodynamic Drag (cd)' in a_dict:
                drag_co=float(a_dict['Aerodynamic Drag (cd)'])
            else:
                drag_co=99999.0
            style_dim_url=(v_api + '/styles/' + str(style_id) + 
                            '/equipment?availability=standard&equipmentType=OTHER&name=EXTERIOR_DIMENSIONS&fmt=json&api_key='
                            + a_key)
            st_dim=json.load(urllib2.urlopen(style_dim_url))
            print st_dim
            attr=st_dim['equipment'][0]['attributes']
            a_dict={}
            for attribute in attr:
                a_dict[attribute['name']]=attribute['value']
            print a_dict
            if 'Overall Width Without Mirrors' in a_dict:
                width=float(a_dict['Overall Width Without Mirrors'])
            elif 'Overall Width With Mirrors' in a_dict: 
                width=float(a_dict['Overall Width With Mirrors'])
            else:
                width=99999
            height=float(a_dict['Overall Height'])
            length=float(a_dict['Overall Length']) 
            insert_values=[style_id,model_id,style_name,submodel,engine_id,trans_id,driv_wheels,
                            doors,msrp,deliv_charge,weight,combined,zeroto60,drag_co,width,height,length]
            print '    ' + str(insert_values) 
            #cr.execute('''insert into styles(style_id,model_id,style_name,submodel,engine_id,trans_id,driv_wheels,doors,msrp,deliv_charge)
            #                values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)''',insert_values)
            db.commit()
            sleep(random()/25) 
    makecount=makecount+1
    if makecount > 3 :
        break

db.close()

