import psycopg2
class SearchTool():

    def get_inputs(self):
        operation = input("Search tools by 'barcode', 'name', or 'category': ")
        if(operation=='barcode'):
            search=input("Which barcode to search: ")
        elif(operation=='name'):
            search=input("Which name to search: ")
        elif(operation=='category'):
            search=input("Which category to search: ")
        else:
            print("Invalid search term")
        order = input("Sort by 'name' or 'category', default is 'name': ")
        if(order==""):
            order='name'
        direction=input("Sort 'asc'ending or 'desc'ending, default is 'asc'ending: ")
        if(direction==""):
            direction='asc'
        return operation,search,order,direction

    def execute(self, cur, conn, user):
        values = self.get_inputs()

        try:
            if(values[0]=='barcode'):
            # print(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.sharable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
                command = f"""SELECT tool.barcode,tool.name,tool.description,tool.shareable,tool.purchasedate,tool.purchaseprice,c.categoryname FROM tool 
                    FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                    LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                    WHERE tool.barcode={values[1]}"""
            elif(values[0]=='name'):
                command = f"""SELECT tool.barcode,tool.name,tool.description,tool.shareable,tool.purchasedate,tool.purchaseprice,c.categoryname FROM tool 
                    FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                    LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                    WHERE tool.name='{values[1]}'"""
            elif(values[0]=='category'):
                command = f"""SELECT tool.barcode,tool.name,tool.description,tool.shareable,tool.purchasedate,tool.purchaseprice,c.categoryname FROM tool 
                FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                WHERE c.categoryname='{values[1]}'"""

            if(values[2]=='name'):
                command += f" ORDER BY tool.name {values[3]};"
            elif(values[2]=='category'):
                command += f" ORDER BY c.categoryname {values[3]};"
            # print(command)
            result=cur.execute(command)
            conn.commit()

            rows = cur.fetchall()
            # print("The number of tools: ", cur.rowcount)
            for row in rows:
                print(row)
            # print(result)
            # check for valid results
            # if result is None:
            #     return ('[+][Request] Request Successful')

        except (psycopg2.DatabaseError) as e:
            conn.rollback()
            print(e)
            # if e.pgcode == "23505":
            #     return ('[!][Request] Duplicate Request')
            # elif e.pgcode == "25P02":
            #     return ("[!][Request] Tool Not Sharable")
        finally:
            cur.close()
            return ""

    def toString(self) -> str:
        return "none"

