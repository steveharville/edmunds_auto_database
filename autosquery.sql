-- Sample queries
-- copyright 2016 Steve Harville
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


       select distinct submodel from styles;
       
       select * from styles where make_id=200000238;
       select * from engines where engine_id=401566599;
       select unique eng_type from engines;
       
