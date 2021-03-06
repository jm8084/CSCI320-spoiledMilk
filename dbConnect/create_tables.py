import psycopg2




def create_tables(curs,conn):
    # """ create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE category (
            categoryID SERIAL PRIMARY KEY,
            categoryName VARCHAR(100) UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE tool (
            barcode INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            shareable INTEGER,
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
                        REFERENCES tool (barcode)
                        ON DELETE CASCADE,
                categoryID INTEGER,
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
                        REFERENCES tool (barcode)
                        ON DELETE CASCADE,
                username VARCHAR(20),
                CONSTRAINT fk_username
                    FOREIGN KEY (username)
                        REFERENCES usr (username)
            )
        """,
        """
            CREATE TABLE request (
                barcode INTEGER NOT NULL,
                CONSTRAINT fk_barcode
                    FOREIGN KEY (barcode)
                        REFERENCES tool (barcode),
                username VARCHAR(20) NOT NULL,
                CONSTRAINT fk_username
                    FOREIGN KEY (username)
                        REFERENCES usr (username),
                status INTEGER NOT NULL,
                dateRequired DATE NOT NULL,
                dateReturned DATE NOT NULL,
                PRIMARY KEY (barcode,username,dateRequired,dateReturned)
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
            curs.close()
            conn.close()
