drop table Supplier cascade constraints/
drop table Supplies cascade constraints/
drop table Product cascade constraints/
drop table LogsProduct/
drop table LogsSupplier/
drop table LogsSupplies/
create table Supplier
(
   ID                   NUMBER(3)            not null,
   Supplier_name        VARCHAR2(20),
   constraint PK_SUPPLIER primary key (ID)
)/
create table Supplies
(
   ID                   NUMBER(3)            not null,
   Product_id           NUMBER(3),
   Quantity             NUMBER(5),
   Total                NUMBER(10),
   Delivery_date        DATE,
   Supplier_ID          NUMBER(3),
   constraint PK_SUPPLIES primary key (ID)
)/
create table Product
(
   ID                   NUMBER(3)            not null,
   pName                 VARCHAR2(127),
   pType                 VARCHAR2(127),
   Price                NUMBER(5),
   Quantity             NUMBER(5),
   Quantity_min         NUMBER(5),
   constraint PK_PRODUCT primary key (ID)
)/
create table LogsSupplier
(
   ID                   NUMBER(3)            not null,
   ptime                DATE,
   ptype                VARCHAR2(500),
   before               VARCHAR2(500),
   after                VARCHAR2(500)
)/
create table LogsSupplies
(
   ID                   NUMBER(3)            not null,
   ptime                DATE,
   ptype                VARCHAR2(500),
   before               VARCHAR2(500),
   after                VARCHAR2(500)
)/
create table LogsProduct
(
   ID                   NUMBER(3)            not null,
   ptime                DATE,
   ptype                VARCHAR2(500),
   before               VARCHAR2(500),
   after                VARCHAR2(500)
)/
alter table Supplies
   add constraint FK_SUPPLIES_REFERENCE_SUPPLIER foreign key (Supplier_ID)
      references Supplier (ID)/
alter table Supplies
   add constraint FK_SUPPLIES_REFERENCE_PRODUCT foreign key (Product_id)
      references Product (ID)/
create or replace procedure insert_supplier(
   p_id            IN NUMBER,
   p_supplier_name IN VARCHAR2
)
is
begin
   insert into Supplier (ID, Supplier_name)
   values (p_id, p_supplier_name);
   commit;
end;
/
create or replace procedure insert_product(
   p_id            IN NUMBER,
   p_name          IN VARCHAR2,
   p_type          IN VARCHAR2,
   p_price         IN NUMBER,
   p_quantity      IN NUMBER,
   p_quantity_min  IN NUMBER
)
is
begin
   insert into Product (ID, pName, pType, Price, Quantity, Quantity_min)
   values (p_id, p_name, p_type, p_price, p_quantity, p_quantity_min);
   commit;
end;
/
create or replace procedure insert_supplies(
   p_id            IN NUMBER,
   p_product_id    IN NUMBER,
   p_quantity      IN NUMBER,
   p_total         IN NUMBER,
   p_delivery_date IN DATE,
   p_supplier_id   IN NUMBER
)
is
begin
   insert into Supplies (ID, Product_id, Quantity, Total, Delivery_date, Supplier_ID)
   values (p_id, p_product_id, p_quantity, p_total, p_delivery_date, p_supplier_id);
   commit;
end;
/
create or replace procedure update_supplier(
   p_id            IN NUMBER,
   p_supplier_name IN VARCHAR2
)
is
begin
   update Supplier
   set Supplier_name = p_supplier_name
   where ID = p_id;
   commit;
end;
/
create or replace procedure update_product(
   p_id            IN NUMBER,
   p_name          IN VARCHAR2,
   p_type          IN VARCHAR2,
   p_price         IN NUMBER,
   p_quantity      IN NUMBER,
   p_quantity_min  IN NUMBER
)
is
begin
   update Product
   set pName = p_name,
       pType = p_type,
       Price = p_price,
       Quantity = p_quantity,
       Quantity_min = p_quantity_min
   where ID = p_id;
   commit;
end;
/
create or replace procedure update_supplies(
   p_id            IN NUMBER,
   p_product_id    IN NUMBER,
   p_quantity      IN NUMBER,
   p_total         IN NUMBER,
   p_delivery_date IN DATE,
   p_supplier_id   IN NUMBER
)
is
begin
   update Supplies
   set Product_id = p_product_id,
       Quantity = p_quantity,
       Total = p_total,
       Delivery_date = p_delivery_date,
       Supplier_ID = p_supplier_id
   where ID = p_id;
   commit;
end;
/
create or replace procedure delete_from_supplier(
   p_id IN NUMBER
)
is
begin
   delete from Supplier
   where ID = p_id;
   commit;
end;
/
create or replace procedure delete_from_product(
   p_id IN NUMBER
)
is
begin
   delete from Product
   where ID = p_id;
   commit;
end;
/
create or replace procedure delete_from_supplies(
   p_id IN NUMBER
)
is
begin
   delete from Supplies
   where ID = p_id;
   commit;
end;
/
CREATE TRIGGER LoggerSupplier
  AFTER INSERT OR UPDATE OR DELETE ON supplier FOR EACH ROW
DECLARE
  data_before VARCHAR2(500);
  data_after VARCHAR2(500);
  max_id NUMBER(20);
BEGIN
    select max(id) into max_id from LogsSupplier;

    IF MAX_ID is NULL THEN
      max_id := 0;
    END IF;
  IF INSERTING THEN
    data_before := NULL;
    data_after := 'ID:' || :new.id || ' supplier_name:' || :new.supplier_name;

    INSERT INTO LogsSupplier(id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'INSERT', data_before, data_after);

  ELSIF UPDATING THEN

    data_before := 'ID:' || :old.id || ' supplier_name:' || :old.supplier_name;
    data_after := 'ID:' || :new.id || ' supplier_name:' || :new.supplier_name;

    INSERT INTO LogsSupplier(id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'UPDATE', data_before, data_after);

  ELSIF DELETING THEN

    data_before := 'ID:' || :old.id || ' supplier_name:' || :old.supplier_name;
    data_after := NULL;

    INSERT INTO LogsSupplier(id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'DELETE', data_before, data_after);

  END IF;

END;/
CREATE TRIGGER LoggerSupplies
  AFTER INSERT OR UPDATE OR DELETE ON Supplies
  FOR EACH ROW
DECLARE
  data_before VARCHAR2(500);
  data_after VARCHAR2(500);
  max_id NUMBER(20);
BEGIN
  SELECT max(id) INTO max_id FROM LogsSupplies;

  IF max_id IS NULL THEN
    max_id := 0;
  END IF;

  IF INSERTING THEN
    data_before := NULL;
    data_after := 'ID:' || :new.id || ' Product_id:' || :new.product_id ||
                  ' Quantity:' || :new.quantity || ' Total:' || :new.total ||
                  ' Delivery_date:' || :new.delivery_date || ' Supplier_ID:' || :new.supplier_id;

    INSERT INTO LogsSupplies (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'INSERT', data_before, data_after);

  ELSIF UPDATING THEN
    data_before := 'ID:' || :old.id || ' Product_id:' || :old.product_id ||
                   ' Quantity:' || :old.quantity || ' Total:' || :old.total ||
                   ' Delivery_date:' || :old.delivery_date || ' Supplier_ID:' || :old.supplier_id;
    data_after := 'ID:' || :new.id || ' Product_id:' || :new.product_id ||
                  ' Quantity:' || :new.quantity || ' Total:' || :new.total ||
                  ' Delivery_date:' || :new.delivery_date || ' Supplier_ID:' || :new.supplier_id;

    INSERT INTO LogsSupplies (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'UPDATE', data_before, data_after);

  ELSIF DELETING THEN
    data_before := 'ID:' || :old.id || ' Product_id:' || :old.product_id ||
                   ' Quantity:' || :old.quantity || ' Total:' || :old.total ||
                   ' Delivery_date:' || :old.delivery_date || ' Supplier_ID:' || :old.supplier_id;
    data_after := NULL;

    INSERT INTO LogsSupplies (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'DELETE', data_before, data_after);
  END IF;

END;/
CREATE TRIGGER LoggerProduct
  AFTER INSERT OR UPDATE OR DELETE ON Product
  FOR EACH ROW
DECLARE
  data_before VARCHAR2(500);
  data_after VARCHAR2(500);
  max_id NUMBER(20);
BEGIN
  SELECT max(id) INTO max_id FROM LogsProduct;

  IF max_id IS NULL THEN
    max_id := 0;
  END IF;

  IF INSERTING THEN
    data_before := NULL;
    data_after := 'ID:' || :new.id || ' pName:' || :new.pName || ' pType:' || :new.pType ||
                  ' Price:' || :new.Price || ' Quantity:' || :new.Quantity || ' Quantity_min:' || :new.Quantity_min;

    INSERT INTO LogsProduct (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'INSERT', data_before, data_after);

  ELSIF UPDATING THEN
    data_before := 'ID:' || :old.id || ' pName:' || :old.pName || ' pType:' || :old.pType ||
                   ' Price:' || :old.Price || ' Quantity:' || :old.Quantity || ' Quantity_min:' || :old.Quantity_min;
    data_after := 'ID:' || :new.id || ' pName:' || :new.pName || ' pType:' || :new.pType ||
                  ' Price:' || :new.Price || ' Quantity:' || :new.Quantity || ' Quantity_min:' || :new.Quantity_min;

    INSERT INTO LogsProduct (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'UPDATE', data_before, data_after);

  ELSIF DELETING THEN
    data_before := 'ID:' || :old.id || ' pName:' || :old.pName || ' pType:' || :old.pType ||
                   ' Price:' || :old.Price || ' Quantity:' || :old.Quantity || ' Quantity_min:' || :old.Quantity_min;
    data_after := NULL;

    INSERT INTO LogsProduct (id, ptime, pType, before, after)
    VALUES (max_id+1, SYSTIMESTAMP, 'DELETE', data_before, data_after);
  END IF;

END;
/
CREATE OR REPLACE PROCEDURE get_supplier_logs (
    p_start_time IN DATE DEFAULT NULL,
    p_end_time   IN DATE DEFAULT NULL,
    p_type       IN VARCHAR2 DEFAULT NULL
)
IS
BEGIN
    FOR rec IN (
        SELECT ID, ptime, pType, before, after
        FROM LogsSupplier
        WHERE (p_start_time IS NULL OR ptime >= p_start_time)
          AND (p_end_time IS NULL OR ptime <= p_end_time)
          AND (p_type IS NULL OR pType = p_type)
        ORDER BY ptime DESC
    ) LOOP
        DBMS_OUTPUT.PUT_LINE('ID: ' || rec.ID || ' | Time: ' || rec.ptime || ' | Type: ' || rec.pType ||
                             ' | Before: ' || rec.before || ' | After: ' || rec.after);
    END LOOP;
END;
/
CREATE OR REPLACE PROCEDURE get_supplies_logs (
    p_start_time IN DATE DEFAULT NULL,
    p_end_time   IN DATE DEFAULT NULL,
    p_type       IN VARCHAR2 DEFAULT NULL
)
IS
BEGIN
    FOR rec IN (
        SELECT ID, ptime, pType, before, after
        FROM LogsSupplies
        WHERE (p_start_time IS NULL OR ptime >= p_start_time)
          AND (p_end_time IS NULL OR ptime <= p_end_time)
          AND (p_type IS NULL OR pType = p_type)
        ORDER BY ptime DESC
    ) LOOP
        DBMS_OUTPUT.PUT_LINE('ID: ' || rec.ID || ' | Time: ' || rec.ptime || ' | Type: ' || rec.pType ||
                             ' | Before: ' || rec.before || ' | After: ' || rec.after);
    END LOOP;
END;
/
CREATE OR REPLACE PROCEDURE get_product_logs (
    p_start_time IN DATE DEFAULT NULL,
    p_end_time   IN DATE DEFAULT NULL,
    p_type       IN VARCHAR2 DEFAULT NULL
)
IS
BEGIN
    FOR rec IN (
        SELECT ID, ptime, pType, before, after
        FROM LogsProduct
        WHERE (p_start_time IS NULL OR ptime >= p_start_time)
          AND (p_end_time IS NULL OR ptime <= p_end_time)
          AND (p_type IS NULL OR pType = p_type)
        ORDER BY ptime DESC
    ) LOOP
        DBMS_OUTPUT.PUT_LINE('ID: ' || rec.ID || ' | Time: ' || rec.ptime || ' | Type: ' || rec.pType ||
                             ' | Before: ' || rec.before || ' | After: ' || rec.after);
    END LOOP;
END;/
CREATE OR REPLACE PROCEDURE generate_summary_report (
    p_flag1 IN BOOLEAN DEFAULT FALSE,   -- флаг сортировки по названию сущности
    p_flag2 IN BOOLEAN DEFAULT FALSE,   -- флаг сортировки по типу операции
    p_flag3 IN BOOLEAN DEFAULT FALSE    -- флаг сортировки по количеству операций
) IS
BEGIN
    -- Если флаг 1 (сортировка по названию сущности)
    IF p_flag1 THEN
        FOR rec IN (
            SELECT entity_name, operation_type, COUNT(*) AS operation_count
            FROM (
                SELECT 'Supplier' AS entity_name, pType AS operation_type FROM LogsSupplier
                UNION ALL
                SELECT 'Supplies' AS entity_name, pType AS operation_type FROM LogsSupplies
                UNION ALL
                SELECT 'Product' AS entity_name, pType AS operation_type FROM LogsProduct
            )
            GROUP BY entity_name, operation_type
            ORDER BY entity_name
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('Entity: ' || rec.entity_name ||
                                 ' | Operation Type: ' || rec.operation_type ||
                                 ' | Count: ' || rec.operation_count);
        END LOOP;
    END IF;

    -- Если флаг 2 (сортировка по типу операции)
    IF p_flag2 THEN
        FOR rec IN (
            SELECT entity_name, operation_type, COUNT(*) AS operation_count
            FROM (
                SELECT 'Supplier' AS entity_name, pType AS operation_type FROM LogsSupplier
                UNION ALL
                SELECT 'Supplies' AS entity_name, pType AS operation_type FROM LogsSupplies
                UNION ALL
                SELECT 'Product' AS entity_name, pType AS operation_type FROM LogsProduct
            )
            GROUP BY entity_name, operation_type
            ORDER BY operation_type
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('Entity: ' || rec.entity_name ||
                                 ' | Operation Type: ' || rec.operation_type ||
                                 ' | Count: ' || rec.operation_count);
        END LOOP;
    END IF;

    -- Если флаг 3 (сортировка по количеству операций)
    IF p_flag3 THEN
        FOR rec IN (
            SELECT entity_name, operation_type, COUNT(*) AS operation_count
            FROM (
                SELECT 'Supplier' AS entity_name, pType AS operation_type FROM LogsSupplier
                UNION ALL
                SELECT 'Supplies' AS entity_name, pType AS operation_type FROM LogsSupplies
                UNION ALL
                SELECT 'Product' AS entity_name, pType AS operation_type FROM LogsProduct
            )
            GROUP BY entity_name, operation_type
            ORDER BY operation_count DESC
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('Entity: ' || rec.entity_name ||
                                 ' | Operation Type: ' || rec.operation_type ||
                                 ' | Count: ' || rec.operation_count);
        END LOOP;
    END IF;
END;