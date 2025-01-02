### Connecting to the database
psql -U postgres -d financial_db

### Show all the data of the database table
select * from transactions;

### Update one data entry
update transactions set amount = amount + 100 where transaction_id = 'd05bd550-2842-4f13-b24a-e9aae2c9c4a9';

#### Alter table for showing before and after value
```sql
ALTER TABLE transactions REPLICA IDENTITY FULL;
update transactions set amount = amount + 150 where transaction_id = 'd05bd550-2842-4f13-b24a-e9aae2c9c4a9';
```

### Connector definition 
```json
{
  "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
  "connector.displayName": "PostgreSQL",
  "topic.prefix": "cdc",
  "database.user": "postgres",
  "database.dbname": "financial_db",
  "database.hostname": "postgres",
  "database.password": "********",
  "name": "postgres-fin-connector",
  "connector.id": "postgres",
  "plugin.name": "pgoutput"
}
```

### Update connectors
```shell
curl -H 'Content-Type: application/json' localhost:8083/connectors --data '
{
  "name": "postgres-fin-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "plugin.name": "pgoutput",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",  
    "database.password": "postgres",
    "database.dbname": "financial_db",
    "database.server.name": "postgres",
    "table.include.list": "public.transactions",
    "topic.prefix": "cdc",
    "decimal.handling.mode": "string" 
  }
}'
```

### List, Delete connectors 
```shell
curl -i -X GET localhost:8083/connectors/
curl -i -X DELETE localhost:8083/connectors/postgre-fin-conector
```

### Adding a column in the database 
```shell
ALTER TABLE transactions add column modified_by TEXT;
ALTER TABLE transactions add column modified_at TIMESTAMP;
```

### Creating a function for sql 
```shell
CREATE OR REPLACE FUNCTION record_change_user()
RETURNS TRIGGER AS $$
BEGIN
NEW.modified_by := current_user;
NEW.modified_at := CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Create a trigger for user update
```shell
CREATE TRIGGER trigger_record_user_update
BEFORE UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION record_change_user();

# We can check the triggers action by update one of the value
update transactions set amount = amount + 150 where transaction_id = 'd05bd550-2842-4f13-b24a-e9aae2c9c4a9';
```

### Let's drop the trigger 
```shell
drop trigger trigger_record_user_update
```

### Create another function for that trigger 
```shell
CREATE OR REPLACE FUNCTION record_changed_columns()
RETURNS TRIGGER AS $$
DECLARE
change_details JSONB;
BEGIN
change_details := '{}'::JSONB; -- empty json object
if NEW.amount IS DISTINCT FROM OLD.amount THEN 
change_details := jsonb_insert(change_details, '{amount}', json_build_object('old', OLD.amount, 'new', NEW.amount));
END IF;
-- adding the user and timestamp
change_details := change_details || jsonb_build_object('modified_by', current_user, 'modified_at', now());
--- update the change_info column
NEW.change_info := change_details;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Associate this function with the table column
```shell
ALTER TABLE transactions ADD COLUMN change_info JSONB;
select * from transactions
CREATE TRIGGER trigger_record_change_info
```

### Now create the trigger
```shell
CREATE TRIGGER trigger_record_change_info
BEFORE UPDATE ON TRANSACTIONS
FOR EACH ROW EXECUTE FUNCTION record_change_column();

select * from transactions;

update transactions set amount = 1000 where transaction_id = 'd05bd550-2842-4f13-b24a-e9aae2c9c4a9';
```