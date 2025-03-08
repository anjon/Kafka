import psycopg2
from psycopg2.extras import DictCursor

def fetch_data(cursor, table_name):
    query = f"""
        SELECT id, name, surname, age, gender, country, email
        FROM {table_name}
        ORDER BY id;
    """
    cursor.execute(query)
    return cursor.fetchall()

def compare_tables(conn):
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        persons_data = fetch_data(cursor, "persons")
        persons_sink_data = fetch_data(cursor, "persons_sink")

        persons_dict = {row['id']: row for row in persons_data}
        persons_sink_dict = {row['id']: row for row in persons_sink_data}

        mismatches = []
        match_count = 0
        all_ids = set(persons_dict.keys()).union(set(persons_sink_dict.keys()))

        for i, id_ in enumerate(all_ids, start=1):
            row1 = persons_dict.get(id_)
            row2 = persons_sink_dict.get(id_)

            if row1 != row2:
                mismatches.append((id_, row1, row2))
            else:
                match_count += 1
                if match_count % 10 == 0:
                    print(f"Matched {match_count} records so far...")

        return mismatches

def main():
    conn = psycopg2.connect(
        dbname="kafkadb",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )

    try:
        mismatches = compare_tables(conn)
        if mismatches:
            print("Mismatched records found:")
            for id_, row1, row2 in mismatches:
                print(f"ID: {id_}")
                print("Persons Table:", dict(row1) if row1 else "Missing")
                print("Persons Sink Table:", dict(row2) if row2 else "Missing")
                print("-" * 40)
        else:
            print("All records match between 2 tables!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
