import psycopg2


class Request():

    def get_inputs(self):
        barcode = input("Barcode of tool to borrow: ")
        daterequired = input("Date the tool is required YYYY-MM-DD: ")
        datereturned = input("Date to return the tool YYYY-MM-DD: ")

        return barcode, daterequired, datereturned

    def execute(self, cur,conn, user):
        values = self.get_inputs()

        try:
            # print(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.sharable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
            result = cur.execute(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.sharable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
            conn.commit()

            # print(result)
            # check for valid results
            if result is None:
                return ('[+][Request] Request Successful')

        except (psycopg2.DatabaseError) as e:
            conn.rollback()
            # print(e)
            if e.pgcode == "23505":
                return ('[!][Request] Duplicate Request')
            elif e.pgcode == "25P02":
                return ("[!][Request] Tool Not Sharable")
        finally:
            cur.close()


    def toString(self,result) -> str:
        return result

