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
cr.execute("""merge into rating_top t
                using (select style_id from styles ) s
                on (t.style_id = s.style_id)
                when not matched then
                    insert (style_id, grade, summary)
                    values (s.style_id,'Z','??') 
           """)        
db.commit()
cr.execute("""select style_id from rating_top where grade='Z' """)
style_tup=cr.fetchall()
v_api='https://api.edmunds.com/api/vehicle/v2/styles/'
a_key='TopSecret'

def insert_rating(style_id,title,grade,score,summary):
    "rating info insert into table"
    insert_values=[style_id,title,grade,score,summary]
    print insert_values
    sql_string="""
        merge into  ratings e
        using (
            select '""" + style_id + """' style_id,
                   '""" + title    + """' title,
                   '""" + grade    + """' grade,
                   '""" + score    + """' score,
                   '""" + summary  + """' summary
            from dual) d
        on (e.style_id = d.style_idi and e.title=d.title)
        when matched then
            update set  e.grade  = d.grade,
                        e.score  = d.score,  
                        e.summary= d.summary  
        when not matched then
            insert (style_id,
                    title,
                    grade,
                    score,
                    summary)
            values(:1,:2,:3,:4,:5)
     """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    return ;


for style in style_tup:
    style_id=str(style[0])
    grade='Z'
    summary='??'
    print style_id
    grade_url=v_api + style_id + '?fmt=json&api_key=' + a_key
    print grade_url
    grade_info=json.load(urllib2.urlopen(grade_url))
    print json.dumps(grade_info,indent=4)
    try:
        grade=grade_info['grade']
        print grade
    summary=grade_info['summary']
    insert_values=[style_id, grade, summary]
    print insert_values
    sql_string="""
        merge into  rating_top e
        using (
            select '""" + style_id + """' style_id,
                   '""" + grade    + """' grade,
                   '""" + summary  + """' summary
            from dual) d
        on (e.style_id = d.style_id)
        when matched then
            update set  e.grade  = d.grade,
                        e.summary= d.summary  
        when not matched then
            insert (style_id,
                    grade,
                    summary)
            values(:1,:2,:3)
     """
    cr.execute(sql_string,insert_values)                 
    db.commit()
    for category in grade_info['ratings']:
        insert_rating(style_id,category['title'],category['grade'],category['score'],category['summary'])
        for rate_detail in category['subRatings']:
            insert_rating(style_id,rate_detail['title'],rate_detail['grade'],rate_detail['score'],rate_detail['summary'])
    sleep(random()/45)
db.close()
