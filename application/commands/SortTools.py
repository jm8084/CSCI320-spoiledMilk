import psycopg2
class SortTools():

    def get_inputs(self):
        type = input("Sort Tools by 'name' or 'category': ")

        if type=='name':
            order = input("Sort names 'asc'ending or 'desc'ending: ")
        elif type =='category':
            order = input("Sort category 'asc'ending or 'desc'ending: ")
        else:
            print("[!][Sort] Invalid input")
        return type,order

    def execute(self, cur, conn, user):
        values = self.get_inputs()

        try:
            if(values[0]=='name'):
                # print(f"SELECT * FROM tool FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode LEFT OUTER JOIN category c on tc.categoryid = c.categoryid ORDER BY tool.name {values[1]};")
                cur.execute(f"SELECT * FROM tool FULL OUTER JOIN tool_categories tc on tool.barcode = tc.barcode LEFT OUTER JOIN category c on tc.categoryid = c.categoryid ORDER BY tool.name {values[1]};")
            elif(values[0]=='category'):
                # print(f"SELECT * FROM tool INNER JOIN tool_categories tc on tool.barcode = tc.barcode INNER JOIN category c on tc.categoryid = c.categoryid ORDER BY c.categoryname {values[1]};")
                cur.execute(f"SELECT * FROM tool INNER JOIN tool_categories tc on tool.barcode = tc.barcode INNER JOIN category c on tc.categoryid = c.categoryid ORDER BY c.categoryname {values[1]};")

            rows = cur.fetchall()
            # print("The number of tools: ", cur.rowcount)
            for row in rows:
                print(row)

        except (psycopg2.DatabaseError) as e:
            conn.rollback()
            print(e)
        finally:
            cur.close()
            return ""

    def toString(self) -> str:
        return ""

