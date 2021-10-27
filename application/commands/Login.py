
class Login():

    def get_inputs(self):

        username = input('Username: ')
        password = input('Password: ')

        return((username, password))

    def execute(self, cur):

        values = self.get_inputs()

        try:
            cur.execute("SELECT * FROM usr WHERE username = %s AND password = %s", (values[0], values[1]))



        except:
            print('login failed!')


    def toString(self, result) -> str:

        # extract & display results

        return result

