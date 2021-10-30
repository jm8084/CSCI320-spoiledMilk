
class Login():

    def get_inputs(self):

        username = input('Username: ')
        password = input('Password: ')

        return((username, password))

    def execute(self, cur):

        values = self.get_inputs()

        try:
            cur.execute("SELECT email, username, firstname, lastname FROM usr WHERE username = %s AND password = %s", (values[0], values[1]))
            return self.toString(cur.fetchone())

        except:
            print('login failed!')


    def toString(self, result):

        print('Hi ',result[2])

        return result

