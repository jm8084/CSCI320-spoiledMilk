import psycopg2
class ManageCatalog():

    def get_inputs(self):
        operation = input("Would you like to 'add', 'edit', or 'delete' a tool: ")

        if operation == 'add':
            # user = input("Username: ")
            barcode = input("Tool barcode: ")
            name = input("Tool Name: ")
            description = input("Description: ")
            purchase_p = input("Purchase Price: x.xx ")
            purchase_d = input("Purchase Date YYYY-MM-DD: ")
            share = 1

            # "INSERT INTO tool(barcode, name, description, shareable, purchaseDate, purchasePrice)
            # VALUES(barcode, name, description, purchase_p, purchase_d, share);"
            # "INSERT INTO catalog(barcode, username) VALUES(barcode, USERNAME???)"

            # return operation, barcode, name, description, purchase_p, purchase_d, share, user
            return operation, barcode, name, description, purchase_p, purchase_d, share

        elif operation == 'edit':
            bar = input('Tool barcode to edit: ')
            action = input(
                "What would you like to change? Enter one: name, description, shareable, purchaseDate, purchasePrice ")

            change = input("What do you want to change it to?")

            # "UPDATE tool SET action = change WHERE barcode = bar;

            return operation, bar, action, change

        elif operation == 'delete':
            bar = input("Enter barcode of tool to delete: ")

            # "DELETE FROM tool WHERE barcode = bar"
            # "DELETE FROM catalog WHERE barcode = bar"
            # "DELETE FROM category WHERE barcode = bar"

            return operation, bar

        else:
            operation = 'err'

    def execute(self, cur, conn, user):

        values = self.get_inputs()

        if values[0] == 'add':
            try:

                # return operation, barcode, name, description, purchase_p, purchase_d, share
                print(f"INSERT INTO tool(barcode,name,description,sharable,purchasedate,purchaseprice) VALUES({values[1]}, '{values[2]}', '{values[3]}', {values[6]}, '{values[5]}', '{values[4]}')")
                print(f"INSERT INTO catalog VALUES({values[1]}, {user['username']} )")
                result1 = cur.execute(f"INSERT INTO tool(barcode,name,description,sharable,purchasedate,purchaseprice) VALUES({values[1]}, '{values[2]}', '{values[3]}', {values[6]}, '{values[5]}', '{values[4]}')")
                result2 = cur.execute(f"INSERT INTO catalog VALUES({values[1]}, '{user['username']}' )")
                # "INSERT INTO tool(barcode, name, description, shareable, purchaseDate, purchasePrice)
                # VALUES(barcode, name, description, purchase_p, purchase_d, share);"
                # "INSERT INTO catalog(barcode, username) VALUES(barcode, USERNAME???)"
                conn.commit()
                # check for valid results
                print(result1)
                print(result2)
                # if result1 is None or result2 is None:
                #     return 'add failed'
                # else:
                #     return self.toString(result1)

            except (psycopg2.DatabaseError) as e:

                conn.rollback()

                # print(e)

            finally:
                cur.close()

        elif values[0] == 'edit':
            try:
                result = cur.execute(f"UPDATE tool SET {values[2]} = {values[3]} WHERE barcode = {values[1]}")
                # "UPDATE tool SET action = change WHERE barcode = bar;

                # check for valid results
                if result is None:
                    return 'edit failed'
                else:
                    return self.toString(result)
            except:
                print('edit failed!')
        elif values[0] == 'delete':
            try:
                # This statement is probably not correct (I need some requests in order to test)
                # Select the tool if its status is borrowed
                result = cur.execute(f"SELECT * FROM request WHERE barcode = {values[1]}, status = 'Borrowed'")
                if result is None:
                    result1 = cur.execute(f"DELETE FROM tool WHERE barcode = {values[1]}")
                    result2 = cur.execute(f"DELETE FROM catalog WHERE barcode = {values[1]}")
                    result3 = cur.execute(f"DELETE FROM tool_category WHERE barcode = {values[1]}")
                    result4 = cur.execute(f"DELETE FROM request WHERE barcode = {values[1]}")
                    # "DELETE FROM tool WHERE barcode = bar"
                    # "DELETE FROM catalog WHERE barcode = bar"
                    # "DELETE FROM category WHERE barcode = bar"
                    # "DELETE FROM request WHERE barcode = bar"

                    # check for valid results
                    if result1 is None or result2 is None or result3 is None:
                        return 'delete failed'
                    else:
                        return self.toString(result1)
                else:
                    return 'delete failed, tool is being borrowed'
            except:
                print('delete failed!')
        else:
            print('operation failed')

    def toString(self, result) -> str:
        return result

