create table Supplies
(
   ID                   NUMBER(3)            not null,
   Product_id           NUMBER(3),
   Quantity             NUMBER(5),
   Total                NUMBER(10),
   Delivery_date        DATE,
   Supplier_ID          NUMBER(3),
   constraint PK_SUPPLIES primary key (ID)
);
