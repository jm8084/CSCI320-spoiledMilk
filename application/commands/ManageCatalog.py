
class ManageCatalog():

    def __init__(self, cur):
        self.cur = cur
        pass

    def get_inputs(self):
        operation = input("Would you like to 'add', 'edit', or 'delete' a tool: ")

        if operation == 'add':
            user = input("Username: ")
            barcode = input("Tool barcode: ")
            name = input("Tool Name: ")
            description = input("Description: ")
            purchase_p = input("Purchase Price: x.xx ")
            purchase_d = input("Purchase Date: mm/dd/yyyy ")
            share = input("Shareable: Y/N ")

            # "INSERT INTO tool(barcode, name, description, shareable, purchaseDate, purchasePrice)
            # VALUES(barcode, name, description, purchase_p, purchase_d, share);"
            # "INSERT INTO catalog(barcode, username) VALUES(barcode, USERNAME???)"

            return operation, barcode, name, description, purchase_p, purchase_d, share, user

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

    def execute(self):

        values = self.get_inputs()

        if values[0] == 'add':
            try:
                result1 = self.cur.execute(f"INSERT INTO tool VALUES({values[1]}, {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]})")
                result2 = self.cur.execute(f"INSERT INTO catalog VALUES({values[1]}, {values[7]} )")
                # "INSERT INTO tool(barcode, name, description, shareable, purchaseDate, purchasePrice)
                # VALUES(barcode, name, description, purchase_p, purchase_d, share);"
                # "INSERT INTO catalog(barcode, username) VALUES(barcode, USERNAME???)"

                # check for valid results
                if result1 is None or result2 is None:
                    return 'add failed'
                else:
                    return self.toString(result1)

            except:
                print('add failed!')

        elif values[0] == 'edit':
            try:
                result = self.cur.execute(f"UPDATE tool SET {values[2]} = {values[3]} WHERE barcode = {values[1]}")
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
                result1 = self.cur.execute(f"DELETE FROM tool WHERE barcode = {values[1]}")
                result2 = self.cur.execute(f"DELETE FROM catalog WHERE barcode = {values[1]}")
                result3 = self.cur.execute(f"DELETE FROM tool_category WHERE barcode = {values[1]}")
                # "DELETE FROM tool WHERE barcode = bar"
                # "DELETE FROM catalog WHERE barcode = bar"
                # "DELETE FROM category WHERE barcode = bar"

                # check for valid results
                if (result1 is None or result2 is None or result3 is None):
                    return 'delete failed'
                else:
                    return self.toString(result1)
            except:
                print('delete failed!')

    def toString(self) -> str:
        return "none"

