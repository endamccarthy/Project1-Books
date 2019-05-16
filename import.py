import psycopg2
import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
 
 
def create_tables():
    # import environment variables relating to the heroku database
    if not os.getenv("HEROKU_DATABASE_URL") \
       or not os.getenv("HEROKU_DATABASE_HOST") \
       or not os.getenv("HEROKU_DATABASE_DATABASE") \
       or not os.getenv("HEROKU_DATABASE_USER") \
       or not os.getenv("HEROKU_DATABASE_PASSWORD"):
        raise RuntimeError("HEROKU_DATABASE settings are not set")
    HEROKU_DATABASE_URL = os.getenv("HEROKU_DATABASE_URL")
    HEROKU_DATABASE_HOST = os.getenv("HEROKU_DATABASE_HOST")
    HEROKU_DATABASE_DATABASE = os.getenv("HEROKU_DATABASE_DATABASE")
    HEROKU_DATABASE_USER = os.getenv("HEROKU_DATABASE_USER")
    HEROKU_DATABASE_PASSWORD = os.getenv("HEROKU_DATABASE_PASSWORD")

    # create tables in the PostgreSQL database
    commands = (
        """
        CREATE TABLE IF NOT EXISTS books (
            isbn VARCHAR(13) PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INTEGER NOT NULL
        )
        """)
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host=HEROKU_DATABASE_HOST,database=HEROKU_DATABASE_DATABASE, user=HEROKU_DATABASE_USER, password=HEROKU_DATABASE_PASSWORD)
        cur = conn.cursor()
        # create table
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    # start up database
    engine = create_engine(HEROKU_DATABASE_URL)
    db = scoped_session(sessionmaker(bind=engine))

    # open csv file and write each row into database
    with open('core/static/books.csv', mode='r') as csv_file:
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