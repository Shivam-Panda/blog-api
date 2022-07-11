import sqlite3 as sql
from sqlite3 import Error


def createConnection(db_file):
    conn = None
    
    try:
        conn = sql.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.commit()

    return conn

def createTables(conn, sql_instructions):
    try:
        c = conn.cursor()
        c.execute(sql_instructions)
    except Error as e:
        print(e)
    
def test():
    db = 'database.db'

    conn = createConnection(db)

    sql_inst_projects = '''
        CREATE TABLE IF NOT EXISTS projects (
            id integer PRIMARY KEY,
            name text NOT NULL,
            begin_date text,
            end_date text
        ); 
    '''

    if conn is not None:
        createTables(conn, sql_inst_projects)
        conn.commit()
    else:
        print('No Database Connection')

def main():
    db = 'database.db'
    
    conn = createConnection(db)
    
    project = ('Sample Project', '03-15-2022', '07-11-2022')
    s = createProject(conn, project) 
    print(s)

def createProject(conn, project):
    s = '''
        INSERT INTO projects(name, begin_date, end_date)
        VALUES(?,?,?) 
    '''

    cur = conn.cursor()
    cur.execute(s, project)

    conn.commit()
    return cur.lastrowid

def update_project(conn, project):
    s = '''
        UPDATE projects
        SET name = ?
            begin_date = ?
            end_date = ?
        WHERE id = ?
    '''
    cur = conn.cursor()
    cur.execute(s, project)

    conn.commit()
    return True

def delete_project(conn, id):
    s = 'DELETE from projects WHERE id=?'

    cur = conn.cursor()
    cur.execute(s, (id,))
    conn.commit()

def delete_all_projects(conn):
    s = 'DELETE from projects'

    cur = conn.cursor()
    cur.exeucte(s)
    conn.commit()

    
def get_all_projects(conn):
    cur = conn.cursor() 
    cur.execute('SELECT * from projects')

    rows = cur.fetchall()

    for row in rows:
        print(row)

def testinger():
    db = 'database.db'

    conn = createConnection(db)

    get_all_projects(conn)

if __name__ == '__main__':
    main()
    testinger()
