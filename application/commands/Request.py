
class Request():

    def get_inputs(self):
        barcode = input("Barcode of tool to borrow: ")
        username = input("Your username: ")
        daterequired = input("Date the tool is required YYYY-MM-DD: ")
        datereturned = input("Date to return the tool YYYY-MM-DD: ")

        return barcode,username,daterequired,datereturned

    def execute(self, cur):
        values = self.get_inputs()

        if values[0] == 'assign':
            try:
                result = self.cur.execute(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES{values[0]}, {values[1]},{0},{values[2]},{values[3]} )")

                # check for valid results
                if result is None:
                    return self.toString(result)
                else:
                    return self.toString(result)
            except:
                print('request failed!')


    def toString(self,result) -> str:
        return result

