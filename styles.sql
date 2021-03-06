-- copyright 2016 Steve Harville
--------------------------------------------------------
--  File created - Friday-August-12-2016   
--------------------------------------------------------
--------------------------------------------------------
--  DDL for Table STYLES
--------------------------------------------------------

  CREATE TABLE "STEVEHARVILLE"."STYLES" 
   (	"STYLE_ID" NUMBER, 
	"MODEL_ID" NUMBER, 
	"STYLE_NAME" VARCHAR2(200 BYTE), 
	"SUBMODEL" VARCHAR2(40 BYTE), 
	"ENGINE_ID" NUMBER, 
	"TRANS_ID" NUMBER, 
	"DRIV_WHEELS" VARCHAR2(20 BYTE), 
	"DOORS" NUMBER, 
	"MSRP" NUMBER, 
	"DELIV_CHARGE" NUMBER, 
	"WEIGHT" NUMBER, 
	"COMBINED" NUMBER, 
	"ZEROTO60" NUMBER, 
	"DRAG_CO" NUMBER, 
	"WIDTH" NUMBER, 
	"HEIGHT" NUMBER, 
	"LENGTH" NUMBER
   ) SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 
 NOCOMPRESS LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  DDL for Index STYLES_PK
--------------------------------------------------------

  CREATE UNIQUE INDEX "STEVEHARVILLE"."STYLES_PK" ON "STEVEHARVILLE"."STYLES" ("STYLE_ID", "MODEL_ID") 
  PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS" ;
--------------------------------------------------------
--  Constraints for Table STYLES
--------------------------------------------------------

  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("STYLE_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("MODEL_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("STYLE_NAME" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" ADD CONSTRAINT "STYLES_PK" PRIMARY KEY ("STYLE_ID", "MODEL_ID")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "USERS"  ENABLE;
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("ENGINE_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("TRANS_ID" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("DRIV_WHEELS" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("DOORS" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("MSRP" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("DELIV_CHARGE" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("SUBMODEL" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("WEIGHT" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("WIDTH" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("COMBINED" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("ZEROTO60" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("DRAG_CO" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("HEIGHT" NOT NULL ENABLE);
  ALTER TABLE "STEVEHARVILLE"."STYLES" MODIFY ("LENGTH" NOT NULL ENABLE);
--------------------------------------------------------
--  Ref Constraints for Table STYLES
--------------------------------------------------------

  ALTER TABLE "STEVEHARVILLE"."STYLES" ADD CONSTRAINT "MODEL_FK" FOREIGN KEY ("MODEL_ID")
	  REFERENCES "STEVEHARVILLE"."MODELS" ("MODEL_ID") ENABLE;
