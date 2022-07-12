import json
import sqlite3 as sql
from sqlite3 import Error

from flask import Flask, request

# Init Functions

file_name = 'data.db'

def createConnection():
    conn = None
    
    try:
        conn = sql.connect(file_name)
    except Error as e:
        print(e)
    
    return conn

def createTables(conn, sql_instructions):
    try:
        c = conn.cursor()
        c.execute(sql_instructions)
    except Error as e:
        print(e)

def initTables():
    conn = createConnection()

    sql_inst_post = '''
        CREATE TABLE IF NOT EXISTS posts (
            id integer PRIMARY KEY,
            title text NOT NULL,
            author text NOT NULL,
            timestamp text NOT NULL,
            likes integer NOT NULL,
            body text NOT NULL   
        ); 
    '''

    sql_inst_comment = '''
        CREATE TABLE IF NOT EXISTS comments (
            id integer PRIMARY KEY,
            author text NOT NULL,
            body text NOT NULL,
            timestamp text NOT NULL,
            postId integer NOT NULL
        ); 
    '''

    if conn is not None:
        createTables(conn, sql_inst_post)
        createTables(conn, sql_inst_comment)

app = Flask(__name__)

def makePost(conn, title, author, timestamp, body):
    s = '''
        INSERT INTO posts(title, author, timestamp, likes, body) 
        VALUES(?,?,?,?,?)
    '''

    cur = conn.cursor()
    cur.execute(s, (title, author, timestamp, 0, body))

    conn.commit()
    return cur.lastrowid

def makeComment(conn, author, body, timestamp, postId):
    s = '''
        INSERT INTO comments(author, timestamp, body, postId) 
        VALUES(?,?,?,?)
    '''

    cur = conn.cursor()
    cur.execute(s, (author, timestamp, body, postId))

    conn.commit()
    return cur.lastrowid

def getAllPosts(conn):
    s = '''SELECT * from posts'''

    cur = conn.cursor()
    cur.execute(s)

    rows = cur.fetchall()

    return rows

def getAllComments(conn, postId):
    s = '''SELECT * from comments WHERE postId=?'''

    cur = conn.cursor()
    cur.execute(s, (postId,))

    rows = cur.fetchall()

    return rows

def likePost(conn, id):
    getter = '''SELECT * from posts WHERE id=?'''

    cur = conn.cursor()
    cur.execute(getter, (id,))

    rows = cur.fetchall()
    cur_likes = rows[0][4]

    setter = '''
        UPDATE posts
        SET likes = ? 
        WHERE id = ?
    '''

    cur.execute(setter, (cur_likes + 1, id))

    conn.commit()
    return cur_likes + 1

def authorPosts(conn, author):
    s = '''SELECT * from posts WHERE author=?'''

    cur = conn.cursor()
    cur.execute(s, (author,))

    rows = cur.fetchall()

    return rows

def reset(conn):
    s = 'DELETE from posts'
    s1 = 'DELETE from comments'

    cur = conn.cursor()
    cur.execute(s)
    cur.execute(s1)

    conn.commit()

    return True

# Testing All Functions
# def test():
#     conn = createConnection('database.db')

#     id = makePost(conn, "Sample Post", "om", "05-16-2022", "This is the body of the sample post")
#     makeComment(conn, "Om1", "This is a comment", "05-17-2022", id)
    
#     print(getAllPosts(conn))
#     print(getAllComments(conn,id))

#     likePost(conn, id)
    
#     print(getAllPosts(conn))

#     reset(conn)

#     print(getAllPosts(conn))
#     print(getAllComments(conn, id))

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/getAllPosts')
def allPosts():
    conn = createConnection()
    posts = getAllPosts(conn)
    return posts

@app.route('/likePost/<id>')
def putLikePost(id):
    conn = createConnection()
    return likePost(conn, id)

@app.route('/getComments/<postId>')
def getComments(postId):
    conn = createConnection()
    comments = getAllComments(conn, postId)
    return comments

@app.route('/getPosts/<author>')
def getAuthorPosts(author):
    conn = createConnection()
    posts = authorPosts(conn, author)
    return posts

@app.route('/reset')
def hard_reset():
    conn = createConnection()
    reset(conn)
    return True

@app.route('/makePost', methods=['POST'])
def createPost():
    data = json.loads(request.data)
    conn = createConnection()
    return makePost(conn, data['title'], data['author'], data['time'], data['body'])

@app.route('/makeComment', methods=['POST'])
def createComment():
    data = json.loads(request.data)
    conn = createConnection()
    return makeComment(conn, data['author'], data['body'], data['time'], data['postId'])
    
# if __name__ == '__main__':
#     conn = createConnection('database.db')
#     reset(conn)
#     test()

# Hard Reset

if __name__ == '__main__':
    conn = createConnection()
    initTables()
    reset(conn)
