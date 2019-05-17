import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
 
def create_tables():
    # import environment variables relating to the heroku database
    if not os.getenv("HEROKU_DATABASE_URL"):
        raise RuntimeError("HEROKU_DATABASE_URL is not set")
    HEROKU_DATABASE_URL = os.getenv("HEROKU_DATABASE_URL")
    
    # start up database
    engine = create_engine(HEROKU_DATABASE_URL)
    db = scoped_session(sessionmaker(bind=engine))

    # create books table
    db.execute("CREATE TABLE IF NOT EXISTS books (\
                isbn VARCHAR(13) PRIMARY KEY, \
                title VARCHAR(127) NOT NULL, \
                author VARCHAR(63) NOT NULL, \
                year INTEGER NOT NULL)")
    db.commit()

    # open csv file and insert each row into books table
    with open('core/static/books1.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",
                    {"isbn":row["isbn"], 
                     "title":row["title"], 
                     "author":row["author"], 
                     "year":row["year"]})
        db.commit()
 

if __name__ == '__main__':
    create_tables()