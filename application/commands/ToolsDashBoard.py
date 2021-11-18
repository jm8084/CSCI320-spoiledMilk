# from datetime import date

class ToolsDashBoard():

    def get_inputs(self):
        pass
        # display = input("Would you like to see 'available', 'lent', 'borrowed', or 'all' tools (default is all): ")
        # if display not in ['available','lent','borrowed']:
        #     display = 'all'
        # return display

    def execute(self, cur, conn, user):
        # display = self.get_inputs()
        try:
            # if display == 'available' or display == 'all':

            # Select all shareable tools except when they're in the request table and request status = approved
            cur.execute(f"""SELECT c.barcode FROM (tool t INNER JOIN catalog c on t.barcode = c.barcode) 
                            WHERE c.username='{user['username']}' AND t.shareable = 1 EXCEPT
                            SELECT t.barcode FROM (tool t INNER JOIN request r on t.barcode = r.barcode)
                            WHERE r.status = 1""")

            # Print the header row
            rows = cur.fetchall()
            print(f"Available: {len(rows)}")


                # Select needed data for any tool that is in the request table and the tool is owned by the user
                # and the status of that request is 1 or 'approved'
            cur.execute(f"""SELECT t.barcode FROM
                        ((catalog c INNER JOIN request r on c.barcode = r.barcode)
                        INNER JOIN tool t on r.barcode = t.barcode)
                        WHERE c.username = '{user['username']}' AND r.status = 1""")

            rows = cur.fetchall()
            print(f"Lent: {len(rows)}")
                # Print the header row

            # Select needed data for any tool that is in the request table and the tool is requested by the user
            # and the status of that request is 1 or 'approved'
            cur.execute(f"""SELECT t.barcode
                        FROM ((catalog c INNER JOIN request r on c.barcode = r.barcode)
                        INNER JOIN tool t on r.barcode = t.barcode)
                        WHERE r.username = '{user['username']}' AND r.status = 1""")

            rows = cur.fetchall()
            print(f"Borrowed: {len(rows)}")

        except Exception as e:
            print("Error getting records")
            print(e)

        finally:
            cur.close()
            return ''

    def toString(self, rows) -> str:
        return ''

