from core import db
 
 
def test():
    rows = db.execute("SELECT * FROM books WHERE author='Jodi Picoult' FETCH FIRST ROW ONLY")
    for row in rows:
        print(row["title"])

    users = db.execute("SELECT * FROM users WHERE username='enda' FETCH FIRST ROW ONLY")
    for user in users:
        print('test')
        print(user["username"])
    


if __name__ == '__main__':
    test()