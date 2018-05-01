# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cx_Oracle
import os
import json
import urllib2
db = cx_Oracle.connect(os.getenv("CX_ORACLE_USERNAME"),
                       os.getenv("CX_ORACLE_PASSWORD"),
                       os.getenv("CX_ORACLE_TNSENTRY"))
print 'Database connection status : ' + str(db)
cr=db.cursor()
print 'Cursor status : ' + str(cr)
myear="2017"
v_api='https://api.edmunds.com/api/vehicle/v2/'
a_key='r3crmsprc92pcyhnc6jkuqhe'
makes_url=v_api + '/makes?state=new&year=' + myear + '&view=basic&fmt=json&api_key=' + a_key
makes=json.load(urllib2.urlopen(makes_url))
makecount=0
for make in makes['makes']:
    make_name=make['niceName']
    make_id=str(make['id'])
    print make_name
    cr.execute("""merge into makes m 
                using (select '""" + make_id + """' make_id,'""" + make_name + """' nicename
                      from dual) d
                on (m.make_id = d.make_id)
                when matched then
                    update set m.nicename = d.nicename
                when not matched then
                    insert (make_id,nicename) 
                    values(:1,:2)""",[make_id,make_name]) 
    db.commit()
    for model in make['models']:
        model_name=model['niceName'] 
        model_id=str(model['years'][0]['id'])
        year=str(model['years'][0]['year'])
        cr.execute("""merge into models m
                    using (select '""" + model_id + """' model_id,'""" + make_id + """' make_id,'""" + year + """' year,'""" + model_name + """' nicename
                        from dual) d
                    on (m.model_id = d.model_id)
                    when matched then
                        update set m.nicename = d.nicename
                    when not matched then
                        insert (model_id,make_id,year,nicename) 
                        values(:1,:2,:3,:4)""",[model_id,make_id,year,model_name])
        db.commit()
db.close()

