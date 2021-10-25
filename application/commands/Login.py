
class Login():

    def __init__(self, cur):
        self.cur = cur
        pass

    def get_inputs(self):

        username = input('Username: ')
        password = input('Password: ')

        return((username, password))

    def execute(self):

        result = ''
        values = self.get_inputs()

        try:
            result = self.cur.execute(f"SELECT {values[0]} FROM usr WHERE password = {values[1]}")

            # check for valid results
            if(result is None):
                return 'login failed'
            else:
                return self.toString(result)

        except:
            print('login failed!')



    def toString(self, result) -> str:

        # extract & display results

        return result

