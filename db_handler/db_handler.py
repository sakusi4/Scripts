import mysql.connector


def select(db, table, conds={}):    
    query = f"""select * from {table} where 1 """
    if len(conds) > 0:
        query += f"""and {' and '.join([f'{k}="{conds[k]}"' for k in conds.keys()])} """

    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        print(result)
    
    cursor.close()


def insert(db, table, args={}):
    query = f"""insert into {table} ({','.join(args.keys())}) values ({",".join(f'"{v}"' for _, v in args.items())})"""

    cursor = db.cursor()
    cursor.execute(query)
    print(f"Inserted record ID: {cursor.lastrowid}")

    db.commit()
    cursor.close()


def update(db, table, updates={}, conds={}):
    query = f"""update {table} set {','.join([f'{k}="{updates[k]}"' for k in updates.keys()])} where 1 """
    if len(conds) > 0:
        query += f"""and {' and '.join([f'{k}="{conds[k]}"' for k in conds.keys()])} """            

    cursor = db.cursor()
    cursor.execute(query)
    print(f"{cursor.rowcount} rows affected.")

    db.commit()
    cursor.close()


if __name__ == '__main__':
    db = mysql.connector.connect(
        host="host",
        user="user",
        passwd="password",
        database="schema",
        port=3306
    )

    insert(db=db, table="user_action", 
        args={
            "email": "test@test", 
            "method": "PUT", 
            "endpoint": "ep", 
            "query": "asd",
            "payload": "test_payload"
        }
    )
    
    select(db=db, table="user_action", 
        conds={
            "email": "test@test", 
            "method": "PUT"
        }
    )
    
    update(db=db, table="user_action", 
        updates={
            "method": "POST"
        }, 
        conds = {
            "email": "test@test", 
            "method": "PUT"
        }
    )

    db.close()