import psycopg2

request_status = ['pending', 'accepted', 'denied', 'completed', 'deleted']

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
            if((action=='name')or(action=='description')):
                change = input("What do you want to change it to?")
            elif(action=='shareable'):
                change = input("What do you want to change it to 'yes' or 'no'?")
                if (change=='yes'):
                    change=1
                elif (change=='no'):
                    change=0
            elif(action=='purchaseDate'):
                change = input("What do you want to change it to YYYY-MM-DD?")
            elif(action=='purchasePrice'):
                change = input("What do you want to change it to x.xx?")


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
                # print(f"INSERT INTO tool(barcode,name,description,sharable,purchasedate,purchaseprice) VALUES({values[1]}, '{values[2]}', '{values[3]}', {values[6]}, '{values[5]}', '{values[4]}')")
                # print(f"INSERT INTO catalog VALUES({values[1]}, {user['username']} )")
                result1 = cur.execute(f"INSERT INTO tool(barcode,name,description,shareable,purchasedate,purchaseprice) VALUES({values[1]}, '{values[2]}', '{values[3]}', {values[6]}, '{values[5]}', '{values[4]}')")
                result2 = cur.execute(f"INSERT INTO catalog VALUES({values[1]}, '{user['username']}' )")
                # "INSERT INTO tool(barcode, name, description, shareable, purchaseDate, purchasePrice)
                # VALUES(barcode, name, description, purchase_p, purchase_d, share);"
                # "INSERT INTO catalog(barcode, username) VALUES(barcode, USERNAME???)"
                conn.commit()
                # check for valid results
                if (result1 is None) and (result2 is None):
                    return "[+][Manage Catalog]Add tool successful"
                # if result1 is None or result2 is None:
                #     return 'add failed'
                # else:
                #     return self.toString(result1)

            except (psycopg2.DatabaseError) as e:

                conn.rollback()

                print(e)

                if e.pgcode == "23505":
                    return ('[!][Manage Catalog] Duplicate Barcode')

            finally:
                cur.close()

        elif values[0] == 'edit':
            try:
                # print(f"UPDATE tool SET {values[2]} = {values[3]} WHERE barcode = {values[1]}")
                result = cur.execute(f"UPDATE tool SET {values[2]} = {values[3]} WHERE barcode = {values[1]}")

                conn.commit()
                # "UPDATE tool SET action = change WHERE barcode = bar;
                # print(result)
                # check for valid results
                if result is None:
                    return '[+][Manage Catalog]Edit tool successful'
                # else:
                #     return self.toString(result)
            except (psycopg2.DatabaseError) as e:

                conn.rollback()

                print(e)


            finally:
                cur.close()
        elif values[0] == 'delete':
            try:
                # This statement is probably not correct (I need some requests in order to test)
                # Select the tool if its status is borrowed

                # result = cur.execute(f"SELECT * FROM request WHERE barcode = {values[1]}, status = 'Borrowed'")
                # if result is None:

                # check request table if barcode is active, update status otherwise
                cur.execute(f"SELECT barcode, username, status FROM request WHERE barcode = %s", (values[1],))
                result0 = cur.fetchall()
                if result0:
                    delete = True
                    for i in result0:
                        # if pending or accepted
                        if i[2] < 2:
                            print("\033[1mCan't delete tool\033[0m")
                            print(f"Tool: {i[0]} \nTool status: {request_status[i[2]]} \nFrom: {i[1]} \n")
                            delete = False
                        elif delete:
                            cur.execute(f"UPDATE request SET status = %s WHERE barcode = %s", (4, i[0]))

                    if delete:
                        cur.execute(f"DELETE FROM catalog WHERE barcode = %s AND username = %s", (values[1], user['username']))
                        print(f'Tool barcode {values[1]} deleted!')
                    else:
                        conn.rollback()
                    # result4 = cur.execute(f"DELETE FROM request WHERE barcode = {values[1]}")


                # result = cur.execute(f"SELECT * FROM request WHERE barcode = {values[1]}, status = 'Borrowed'")
                # if result is None:
                #     result1 = cur.execute(f"DELETE FROM tool WHERE barcode = {values[1]}")
                #     result4 = cur.execute(f"DELETE FROM request WHERE barcode = {values[1]}")
                    # "DELETE FROM tool WHERE barcode = bar"
                    # "DELETE FROM catalog WHERE barcode = bar"
                    # "DELETE FROM category WHERE barcode = bar"
                    # "DELETE FROM request WHERE barcode = bar"

                    # check for valid results
            #         if result1 is None or result2 is None or result3 is None:
            #             return 'delete failed'
            #         else:
            #             return self.toString(result1)
            #     else:
            #         return 'delete failed, tool is being borrowed'
            # except:
            #     print('delete failed!')



                conn.commit()
                # "UPDATE tool SET action = change WHERE barcode = bar;
                #print(result1)
                # check for valid results
                # if result is None:
                #     return '[+][Manage Catalog]Edit tool successful'
                # else:
                #     return self.toString(result)
            except (psycopg2.DatabaseError) as e:

                conn.rollback()

                print(e)


            finally:
                cur.close()
        else:
            print('operation failed')

    def toString(self, result) -> str:
        return result

