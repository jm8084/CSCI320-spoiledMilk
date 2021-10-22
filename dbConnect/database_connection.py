import psycopg2
import dbConnect.myLogin as info
from sshtunnel import SSHTunnelForwarder
import dbConnect.create_tables as create_tables

dbName = 'p320_29'

try:

    with SSHTunnelForwarder(
    ('starbug.cs.rit.edu', 22),
    ssh_username=info.username,
    ssh_password=info.password,
    remote_bind_address=('localhost', 5432)) as server:

        server.start()
        print("SSH tunnel established")

        params = {
        'database': dbName,
        'user': info.username,
        'password': info.password,
        'host': 'localhost',
        'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        create_tables.create_tables(curs,conn)
        curs.close()
        conn.commit()

except:
    print("Connection failed")