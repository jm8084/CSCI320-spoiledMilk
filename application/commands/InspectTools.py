
class InspectTools():

    def get_inputs(self):
        display = input("Would you like to see 'available', 'lent', 'borrowed', or 'all' tools (default is all): ")
        if display not in ['available','lent','borrowed']:
        # if display != 'available' or display != 'lent' or display != 'borrowed':
            display = 'all'
        return display

    def execute(self, cur, conn, user):
        # TODO: Colouring or other overdue notifier
        # Red - \033[91m
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
                for row in cur.fetchall():
                    print(row)
            if display == 'lent' or display == 'all':
                print('Lent:')
                cur.execute(f"SELECT r.username, r.daterequired, r.datereturned, t.* FROM "
                            f"((catalog c INNER JOIN request r on c.barcode = r.barcode) "
                            f"INNER JOIN tool t on r.barcode = t.barcode) "
                            f"WHERE c.username = '{user['username']}' AND r.status = 1 "
                            f"ORDER BY r.daterequired ASC")
                for row in cur.fetchall():
                    print(row)
            if display == 'borrowed' or display == 'all':
                print('Borrowed:')
                cur.execute(f"SELECT c.username, r.daterequired, r.datereturned, t.* FROM "
                            f"((catalog c INNER JOIN request r on c.barcode = r.barcode) "
                            f"INNER JOIN tool t on r.barcode = t.barcode) "
                            f"WHERE r.username = '{user['username']}' AND r.status = 1 "
                            f"ORDER BY r.daterequired ASC")
                for row in cur.fetchall():
                    print(row)
        except Exception as e:
            print("Error getting records")
            print(e)
        finally:
            cur.close()
            return ''

    def toString(self, rows) -> str:
        return ''

