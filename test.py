from core import db
 
 
def test():
    rows = db.execute("SELECT * FROM books ORDER BY title")
    for row in rows:
        print(row["title"])

    # create users table
    db.execute("CREATE TABLE IF NOT EXISTS users (\
                id Integer PRIMARY KEY, \
                username VARCHAR(20) NOT NULL UNIQUE, \
                email VARCHAR(120) NOT NULL UNIQUE, \
                password VARCHAR(255))")
    db.commit()
 

if __name__ == '__main__':
    test()