from datetime import date

class InspectTools():

    def get_inputs(self):
        display = input("Would you like to see 'available', 'lent', 'borrowed', or 'all' tools (default is all): ")
        if display not in ['available','lent','borrowed']:
            display = 'all'
        return display

    def execute(self, cur, conn, user):
        display = self.get_inputs()
        try:
            if display == 'available' or display == 'all':
                print('Available:')
                # Select all shareable tools except when they're in the request table and request status = approved
                cur.execute(f"SELECT barcode, name, description, purchasedate, purchaseprice "
                            f"FROM tool WHERE shareable = 1 "
                            f"EXCEPT "
                            f"SELECT t.barcode, t.name, t.description, t.purchasedate, t.purchaseprice "
                            f"FROM (tool t INNER JOIN request r on t.barcode = r.barcode)"
                            f"WHERE r.status = 1 "
                            f"ORDER BY name ASC")

                # Print the header row
                print(f"\033[1m | barcode \t| tool name \t| description \t| purchasedate \t| purchaseprice\033[0m")

                for row in cur.fetchall():
                    # Print all the rows that are returned from the executed SELECT statement
                    print(f" | {row[0]}  \t\t| \t {row[1]}  \t| \t {row[2]}  \t|\t {row[3]}\t|\t {row[4]}")

            if display == 'lent' or display == 'all':
                print('Lent:')
                # Select needed data for any tool that is in the request table and the tool is owned by the user
                # and the status of that request is 1 or 'approved'
                cur.execute(f"SELECT r.username, r.daterequired, r.datereturned, "
                            f"t.barcode, t.name, t.description, t.purchasedate, t.purchaseprice FROM "
                            f"((catalog c INNER JOIN request r on c.barcode = r.barcode) "
                            f"INNER JOIN tool t on r.barcode = t.barcode) "
                            f"WHERE c.username = '{user['username']}' AND r.status = 1 "
                            f"ORDER BY r.daterequired ASC")

                # Print the header row
                print(f"\033[1m | borrower \t| date required \t| return date \t| barcode \t| name \t"
                      f"| description \t| purchase date \t| purchase price \033[0m")

                for row in cur.fetchall():
                    # Print all the rows that are returned from the executed SELECT statement
                    # If they are overdue, color the line red
                    if row[2] < date.today() :
                        print(f"\033[91m | {row[0]}  \t\t| \t {row[1]}  \t| \t {row[2]}  \t|\t {row[3]}\t|\t {row[4]} \t|\t"
                              f" {row[5]} \t|\t {row[6]} \t|\t {row[7]} \033[0m")
                    else:
                        print(f" | {row[0]}  \t\t| \t {row[1]}  \t| \t {row[2]}  \t|\t {row[3]}\t|\t {row[4]} \t|\t"
                              f" {row[5]} \t|\t {row[6]} \t|\t {row[7]}")

            if display == 'borrowed' or display == 'all':
                print('Borrowed:')
                # Select needed data for any tool that is in the request table and the tool is requested by the user
                # and the status of that request is 1 or 'approved'
                cur.execute(f"SELECT c.username, r.daterequired, r.datereturned, "
                            f"t.barcode, t.name, t.description, t.purchasedate, t.purchaseprice FROM "
                            f"((catalog c INNER JOIN request r on c.barcode = r.barcode) "
                            f"INNER JOIN tool t on r.barcode = t.barcode) "
                            f"WHERE r.username = '{user['username']}' AND r.status = 1 "
                            f"ORDER BY r.daterequired ASC")

                # Print the header row
                print(f"\033[1m | lender \t| date required \t| return date \t| barcode \t| name \t"
                      f"| description \t| purchase date \t| purchase price \033[0m")

                for row in cur.fetchall():
                    # Print all the rows that are returned from the executed SELECT statement
                    # If they are overdue, color the line red
                    if row[2] < date.today() :
                        print(f"\033[91m | {row[0]}  \t\t| \t {row[1]}  \t| \t {row[2]}  \t|\t {row[3]}\t|\t {row[4]} \t|\t"
                              f" {row[5]} \t|\t {row[6]} \t|\t {row[7]}\033[0m")
                    else:
                        print(f" | {row[0]}  \t\t| \t {row[1]}  \t| \t {row[2]}  \t|\t {row[3]}\t|\t {row[4]} \t|\t"
                              f" {row[5]} \t|\t {row[6]} \t|\t {row[7]}")

        except Exception as e:
            print("Error getting records")
            print(e)

        finally:
            cur.close()
            return ''

    def toString(self, rows) -> str:
        return ''

