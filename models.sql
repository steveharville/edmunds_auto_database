-- copyright 2016 Steve Harville
--------------------------------------------------------
--  File created - Friday-August-12-2016   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table MODELS
--------------------------------------------------------

  CREATE TABLE "STEVEHARVILLE"."MODELS" 
   (	"MODEL_ID" NUMBER, 
	"MAKE_ID" NUMBER, 
	"YEAR" NUMBER, 
	"NICENAME" VARCHAR2(50 BYTE)
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  DDL for Index MODELS_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "STEVEHARVILLE"."MODELS_PK" ON "STEVEHARVILLE"."MODELS" ("MODEL_ID") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  Constraints for Table MODELS
--------------------------------------------------------

  ALTER TABLE "STEVEHARVILLE"."MODELS" MODIFY ("MODEL_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."MODELS" MODIFY ("MAKE_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."MODELS" MODIFY ("YEAR" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."MODELS" MODIFY ("NICENAME" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."MODELS" ADD CONSTRAINT "MODELS_PK" PRIMARY KEY ("MODEL_ID")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS"  ENABLE;
--------------------------------------------------------
--  Ref Constraints for Table MODELS
--------------------------------------------------------

  ALTER TABLE "STEVEHARVILLE"."MODELS" ADD CONSTRAINT "MAKE_FK" FOREIGN KEY ("MAKE_ID")
	  REFERENCES "STEVEHARVILLE"."MAKES" ("MAKE_ID") ENABLE;
