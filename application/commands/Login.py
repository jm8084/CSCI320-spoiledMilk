
from datetime import datetime

class Login():

    def get_inputs(self):

        username = input('Username: ')
        password = input('Password: ')

        return((username, password))

    def execute(self, cur, conn):

        values = self.get_inputs()

        try:
            cur.execute("SELECT email, username, firstname, lastname FROM usr WHERE username = %s AND password = %s", (values[0], values[1]))
            result = cur.fetchone()

            try:
                cur.execute("UPDATE usr SET lastaccessdate = %s WHERE username = %s AND password = %s",
                            (datetime.now(), values[0], values[1]))
                conn.commit()
            except:
                print('Unable to update access datetime.')
                conn.rollback()

            return self.toString(result)

        except:
            print('login failed!')


        finally:
            cur.close()


    def toString(self, result):

        print('Hi ',result[2])

        return result

