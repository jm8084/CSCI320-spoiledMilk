import psycopg2
from sshtunnel import SSHTunnelForwarder

try:

    with SSHTunnelForwarder(
    ('[1] starbug.cs.rit.edu', 22),
    ssh_username="YOUR_CS_USERNAME",
    ssh_password="YOUR_CS_PASSWORD",
    remote_bind_address=('localhost', 5432)) as server:

        server.start()
        print("SSH tunnel established")

        params = {
        'database': 'YOUR_CS_USERNAME',
        'user': 'YOUR_CS_USERNAME',
        'password': 'YOUR_CS_PASSWORD',
        'host': 'localhost',
        'port': server.local_bind_port
        }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

except:
    print("Connection failed")