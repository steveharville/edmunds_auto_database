select makes.nicename make, 
       year,
       models.nicename model,
       round(weight/hp,2) pounds_hp,
       round(weight/torque,2) pounds_torq,
       round(msrp*weight/hp,0) / 1000 msrp_wt_hp,
       round(msrp*weight/torque,0) / 1000 msrp_wt_tor,
       style_name,
       submodel,
       driv_wheels,
       doors,
       leg_room,
       round(msrp/1000,0) msrp,
       round(tco/1000,0) tco,
       round((((tco-msrp)/msrp)*100),0) percent,
       weight,
       combined,
       width*height fr_area,
       cylinder,
       fuel,
       hp,
       torque,
       eng_type,
       compressor,
       ttype
from makes,models,styles,engines,transmissions,interiors,tco
where 
msrp/1000 <32
--and year=2017
--and weight=9999
--and submodel in ('suv','hatchback','wagon')
--and length > 178
and weight/hp < 15
and weight/torque < 12
--and msrp*weight/torque < 300000
--and weight/hp + weight/torque < 30
--and (tco-msrp)/tco < .3
--and compressor='NA'
--and doors  < 4
--and combined > 10
and submodel not like '%cab%'
--and ttype like  '%AUTO%'
and models.nicename in  ('golf-gti')
--and eng_type='gas'
--and eng_type='diesel'
--and eng_type='hybrid'
--and eng_type in ('electric','hybrid')
and makes.make_id=models.make_id
and   models.model_id = styles.model_id
and   styles.engine_id=engines.engine_id
and   styles.trans_id=transmissions.trans_id
and   styles.style_id=interiors.style_id
and   styles.style_id=tco.style_id
--order by 15;
--order by tco;
--order by  weight/torque;
--order by  msrp*weight/hp;
--order by leg_room desc;
--order by combined desc;
order by msrp*weight/torque;
--order by make, model;
--order by torque desc;
--order by  msrp;
--order by weight/hp;
--order by msrp*width*height*weight/torque;

       
select  makes.nicename,model_id,models.nicename from makes,models where makes.make_id=models.make_id and models.model_id in (select styles.model_id from styles where weight=9999 and msrp < 50000) order by makes.nicename,models.nicename;
select models.model_id, styles.style_id from models,styles where models.model_id=styles.model_id and models.nicename='malibu' and submodel='hybrid';
select models.model_id,weight, year from styles, models where  models.model_id=styles.style_id and models.nicename='fusion';
update styles set weight=9999 where weight=3000;
commit;
update styles set weight=3260 where model_id=200744427 and weight = 9999;
update styles set weight=4030 where model_id=200729831 and weight = 9999;
update styles set weight=3979 where model_id=200724880 and weight = 9999;
update styles set weight=3800 where model_id=200751751 and weight = 9999;
update styles set weight=3500 where model_id=200692011 and weight = 9999;
update styles set weight=3118 where model_id=200492971 and weight = 9999;
update styles set weight=3118 where model_id=200745924 and weight = 9999;
update styles set weight=3700 where model_id=200779605 and weight = 9999;
update styles set weight=3200 where model_id=200747325 and weight = 9999;
update styles set weight=4449 where model_id=200782175 and weight = 9999;
update styles set weight=4100 where model_id=200782175 and weight = 9999;
update styles set weight=4200 where model_id=401589394 and weight = 9999;
update styles set weight=4051 where model_id=401582329 and weight = 9999;
update styles set weight=3200 where model_id=200737268 and weight = 9999;
update styles set weight=4300 where model_id=200747759 and weight = 9999;
update styles set weight=3933 where model_id=401581494 and weight = 9999;
update styles set weight=4200 where model_id=401611671 and weight = 9999;
update styles set weight=3500 where model_id=401581354 and weight = 9999;
update styles set weight=2400 where model_id=200744978 and weight = 9999;
update styles set weight=2770 where model_id=200734751 and weight = 9999;
update styles set weight=3100 where model_id=200745612 and weight = 9999;
update styles set weight=2800 where model_id=200772765 and weight = 9999;
update styles set weight=3150 where model_id=401575886 and weight = 9999;
update styles set weight=3100 where model_id=401574186 and weight = 9999;
update styles set weight=3340 where model_id=200748018 and weight = 9999;
update styles set weight=3900 where model_id=200739112 and weight = 9999;
update styles set weight=3459 where model_id=401590246 and weight = 9999;
update styles set weight=4300 where model_id=200696421 and weight = 9999;
update styles set weight=4000 where model_id=200735398 and weight = 9999;
update styles set weight=7000 where model_id=200691942 and weight = 9999;
update styles set weight=5000 where model_id=200742272 and weight = 9999;
update styles set weight=3450 where model_id=401642255 and weight = 9999;
update styles set weight=3250 where model_id=401640813 and weight = 9999;
update styles set weight=3700 where model_id=401642197 and weight = 9999;
update styles set weight=5000 where model_id=401647934 and weight = 9999;
update styles set weight=2500 where model_id=200732915 and weight = 9999;
update styles set weight=2500 where model_id=401630049 and weight = 9999;
update styles set weight=2500 where model_id=401629469 and weight = 9999;
update styles set weight=4000 where model_id=401628704 and weight = 9999;
update styles set weight=4000 where model_id=401627422 and weight = 9999;
update styles set weight=3400 where model_id=401647595 and weight = 9999;
update styles set weight=3400 where model_id=200732068 and weight = 9999;
update styles set weight=3400 where model_id=401645884 and weight = 9999;
update styles set weight=3500 where model_id=401646454 and weight = 9999;
update styles set weight=3700 where model_id=401646453 and weight = 9999;
update styles set weight=2820 where model_id=401637969 and weight = 9999;
update styles set weight=3200 where model_id=401647283 and weight = 9999;
update styles set weight=3500 where model_id=200727079; --and weight = 9999;
update styles set weight=3500 where model_id=200732915; --and weight = 9999;
update styles set weight=3340 where model_id=401641255 or model_id=200748018;
update styles set weight=3616 where model_id=401629469;
update engines set torque=105 where engine_id=401641260;
update engines set torque=156 where engine_id=401648036;
update engines set torque=147 where engine_id=401655405;
update engines set hp=111 where engine_id=401655405;
update engines set torque=294 where engine_id=401626583;
update engines set hp=149 where engine_id=401626583;
update engines set torque=713,hp=532 where eng_name = 'P90d';
update engines set torque=147,hp=111 where engine_id=401566599;
update engines set torque=325,hp=333 where engine_id=200737489 or engine_id=401645209;
update engines set torque=82,hp=73 where engine_id=401597751;
update engines set torque=105,hp=121 where engine_id=200707021 or engine_id=401612029;
update engines set torque=100,hp=89 where engine_id=401612067;
update engines set torque=177,hp=179 where engine_id=401630251;
update engines set torque=140,hp=154 where engine_id=200742474;
update engines set torque=105,hp=98 where engine_id=200771449;
update engines set torque=156 where engine_id=200747128;
update engines set torque=187,hp=107 where engine_id=401610733;
update engines set torque=184,hp=143 where engine_id=200740369;
update engines set torque=210,hp=109 where engine_id=200746186;
update engines set torque=156,hp=200 where engine_id=401583435;

Commit;
select unique models.nicename, styles.style_name,engines.engine_id, eng_name,hp,torque,msrp from models,styles,engines  where models.model_id = styles.model_id and styles.msrp < 40000 and styles.engine_id=engines.engine_id and torque < 1 and nicename not in ('rav4-hybrid','f-250-super-duty','f-350-super-duty','mkz','impala') order by msrp;
select style_id, models.model_id from styles,models where models.model_id=styles.style_id and models.nicename='prius-v';


select styles.style_id ,makes.nicename,models.nicename,submodel,style_name,volume,leg_room,head_room,shoulder_room 
from styles , interiors , makes, models 
where  styles.style_id=interiors.style_id
and makes.make_id=styles.make_id
and models.model_id=styles.model_id
and submodel in ('convertible','coupe')
--and makes.nicename = 'fiat'
--order by leg_room*shoulder_room desc;
order by leg_room desc;

       update engines set torque=.000001 where torque=0;
       commit;
       select distinct submodel from styles;
       
       select * from styles where make_id=200000238;
       select * from engines where engine_id=401566599;
       select unique eng_type from engines;
       
       update styles set zeroto60=7.4 where style_id in (401637629,401657963);
