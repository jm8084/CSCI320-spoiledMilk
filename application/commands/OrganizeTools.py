
class OrganizeTools():

    def __init__(self, cur):
        self.cur = cur
        pass

    def get_inputs(self):
        operation = input("Would you like to 'assign' a category or 'create' a category: ")

        if operation == 'assign':
            barcode = input("Barcode: ")
            cat_name = input("Category Name: ")
            return operation, barcode, cat_name

        elif operation == 'create':
            cat_name = input("Category Name: ")
            return operation, cat_name

    def execute(self):
        values = self.get_inputs()

        if values[0] == 'assign':
            try:
                cat_id = self.cur.execute(f"SELECT categoryid from category WHERE categoryname = {values[2]}")
                result = self.cur.execute(f"INSERT INTO tool_categories (barcode, categoryid) VALUES({values[1]}, {cat_id} )")

                # check for valid results
                if result is None:
                    return 'assign failed'
                else:
                    return self.toString(result)
            except:
                print('assign failed!')

        if values[0] == 'create':
            try:
                result = self.cur.execute(f"INSERT INTO category (categoryname) VALUES ({values[1]})")

                # check for valid results
                if result is None:
                    return "create failed"
                else:
                    return self.toString(result)
            except:
                print("create failed!")

    def toString(self, result) -> str:
        return result

