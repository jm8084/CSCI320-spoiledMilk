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

        return operation,search

    def execute(self, cur, conn, user):
        values = self.get_inputs()

        try:
            if(values[0]=='barcode'):
            # print(f"INSERT INTO request(barcode, username,status,daterequired,datereturned) VALUES((SELECT barcode from tool WHERE tool.barcode={values[0]} and tool.sharable=1), '{user['username']}',{0},'{values[1]}','{values[2]}' )")
                result = cur.execute(f"""SELECT * FROM tool 
                    FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                    LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                    WHERE tool.barcode={values[1]} ORDER BY tool.name asc;
                    """)
            elif(values[0]=='name'):
                result = cur.execute(f"""SELECT * FROM tool 
                    FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                    LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                    WHERE tool.name='{values[1]}' ORDER BY tool.name asc;
                    """)
            elif(values[0]=='category'):
                result = cur.execute(f"""SELECT * FROM tool 
                FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode 
                LEFT OUTER JOIN category c on tc.categoryid = c.categoryid
                WHERE c.categoryname='{values[1]}' ORDER BY tool.name asc;
                """)
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

