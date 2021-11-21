import psycopg2


class Request():

    def get_recomended(self, bc, cur):

        # get all other users that borrowed the tool
        cur.execute("SELECT DISTINCT username FROM request WHERE barcode = %s", (bc,))
        users = cur.fetchall()
        usrLen = len(users)


        barcodes = {}       # map {barcode : count}

        # for each users, add barcodes to map
        for u in users:
            cur.execute("SELECT DISTINCT barcode FROM request WHERE username = %s", (u))
            ubc = cur.fetchall()
            for b in ubc:
                if b in barcodes:
                    # update barcode count
                    count = barcodes[b]
                    barcodes[b] = count+1
                else:
                    # new barcode instance
                    barcodes.update({b: 1})

        bcList = sorted(barcodes.items(), key= lambda b:b[1])

        print('\n\t------\033[1m Also Borrowed \033[0m--------')
        print('| barcode | name :\t\t description')
        for b in bcList[::-1]:
            if b[1] >= usrLen/2:
                cur.execute("SELECT barcode, name, description FROM tool WHERE barcode = %s", (b[0]))
                tool = cur.fetchone()
                #print("EJM   " + tool[0] + bc)
                if tool[0] != bc:       # doesnt read tool request for some reason
                    print(f'| {tool[0]} | {tool[1]} :\t {tool[2]}')



    def get_inputs(self):
        barcode = input("Barcode of tool to borrow: ")
        daterequired = input("Date the tool is required YYYY-MM-DD: ")
        datereturned = input("Date to return the tool YYYY-MM-DD: ")

        return barcode, daterequired, datereturned

    def execute(self, cur,conn, user):
        values = self.get_inputs()

        try:
            # print(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.sharable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
            result = cur.execute(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.shareable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
            conn.commit()

            # print(result)
            # check for valid results
            if result is None:
                return ('\n[+][Request] Request Successful')

        except (psycopg2.DatabaseError) as e:
            conn.rollback()
            if e.pgcode == "23505":
                return ('[!][Request] Duplicate Request')
            elif e.pgcode == "25P02":
                return ("[!][Request] Tool Not Sharable")
        finally:
            self.get_recomended(int(values[0]), cur)
            cur.close()


    def toString(self,result) -> str:
        return result

