import psycopg2
import dbConnect.myLogin as info
import application.TMS as main
from sshtunnel import SSHTunnelForwarder


dbName = 'p320_29'

try:

    with SSHTunnelForwarder(
        ('starbug.cs.rit.edu', 22),
        ssh_username=info.username,
        ssh_password=info.password,
        remote_bind_address=('localhost', 5432)
    ) as server:

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
        print("Database connection established")

        main.application(conn)

except:
    print("Connection failed")


