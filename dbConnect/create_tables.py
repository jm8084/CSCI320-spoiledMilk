import psycopg2




def create_tables(curs,conn):
    """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE category (
            categoryID SERIAL PRIMARY KEY,
            categoryName TEXT UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE tool (
            barcode INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            sharable INTEGER,
            purchaseDate DATE,
            purchasePrice MONEY
        )
        """,
        """
        CREATE TABLE usr (
            username VARCHAR(20) PRIMARY KEY,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(20) NOT NULL,
            lastAccessDate TIMESTAMP NOT NULL,
            creationDate TIMESTAMP NOT NULL,
            firstName VARCHAR(100) NOT NULL,
            lastName VARCHAR(100) NOT NULL
            )
            """,
        """
            CREATE TABLE tool_categories (
                barcode INTEGER,
                CONSTRAINT fk_barcode
                    FOREIGN KEY (barcode)
                        REFERENCES tool (barcode),
                categoryID SERIAL,
                CONSTRAINT fk_categoryID
                    FOREIGN KEY (categoryID)
                        REFERENCES category (categoryID)
            )
        """,
        """
            CREATE TABLE catalog (
                barcode INTEGER,
                CONSTRAINT fk_barcode
                    FOREIGN KEY (barcode)
                        REFERENCES tool (barcode),
                username VARCHAR(20),
                CONSTRAINT fk_username
                    FOREIGN KEY (username)
                        REFERENCES usr (username)
            )
        """,
        """
            CREATE TABLE request (
                barcode INTEGER NOT NULL UNIQUE,
                CONSTRAINT fk_barcode
                    FOREIGN KEY (barcode)
                        REFERENCES tool (barcode),
                username VARCHAR(20) NOT NULL UNIQUE,
                CONSTRAINT fk_username
                    FOREIGN KEY (username)
                        REFERENCES usr (username),
                status INTEGER NOT NULL,
                dateRequired DATE NOT NULL UNIQUE,
                dateReturned DATE NOT NULL UNIQUE
            )
        """
    ]

    try:
        for command in commands:
            print(command)
            curs.execute(command)
    except (Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
