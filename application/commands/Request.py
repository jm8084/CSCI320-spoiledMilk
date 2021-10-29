
class Request():

    def get_inputs(self):
        barcode = input("Barcode of tool to borrow: ")
        username = input("Your username: ")
        daterequired = input("Date the tool is required YYYY-MM-DD: ")
        datereturned = input("Date to return the tool YYYY-MM-DD: ")

        return barcode,username,daterequired,datereturned

    def execute(self, cur):
        values = self.get_inputs()

        try:
            print(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES({values[0]}, '{values[1]}',{0},'{values[2]}','{values[3]}' )")
            result = self.cur.execute(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES({values[0]}, '{values[1]}',{0},'{values[2]}','{values[3]}' )")
            #cur.close()
            # check for valid results
            if result is None:
                return ('request failed!')
            else:
                return self.toString(result)
        except:
            print('request failed!')


    def toString(self,result) -> str:
        return result

