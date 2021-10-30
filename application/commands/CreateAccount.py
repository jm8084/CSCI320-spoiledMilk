
from datetime import datetime
import psycopg2
import dbConnect.insert_data as insert

class CreateAccount():

    def get_inputs(self):
        username = input('Username: ')
        email    = input('Email: ')
        password = input('Password: ')
        fname    = input('First Name: ')
        lname    = input('Last Name: ')

        return (username,email,password,fname,lname)

    def execute(self, cur, conn):

        values = self.get_inputs()

        try:
            cur.execute(f"INSERT INTO usr "
                        f"(username, email, password, lastaccessdate, creationdate, firstname, lastname) "
                        f"VALUES ('{values[0]}', '{values[1]}', '{values[2]}', '{datetime.now()}', "
                        f"'{datetime.now()}', '{values[3]}', '{values[4]}')")
            conn.commit()
            return self.toString(values)
        except psycopg2.IntegrityError as error:
            print("This username is already in use.  Login to that account or use another username.")
            conn.rollback()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Create account failed!')
            conn.rollback()

    def toString(self, values):
        print('Account created successfully and you will be automatically logged in.')
        print('Welcome, ' + values[3] + '.')
        return values

