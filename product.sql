create table Product
(
   ID                   NUMBER(3)            not null,
   Name                 VARCHAR2(127),
   Type                 VARCHAR2(127),
   Price                NUMBER(5),
   Quantity             NUMBER(5),
   Quantity_min         NUMBER(5),
   constraint PK_PRODUCT primary key (ID)
);