import psycopg2
class OrganizeTools():

    def get_inputs(self):
        operation = input("Would you like to 'assign' a category or 'create' a category: ")

        if operation == 'assign':
            barcode = input("Barcode: ")
            cat_name = input("Category Name: ")
            return operation, barcode, cat_name

        elif operation == 'create':
            cat_name = input("Category Name: ")
            return operation, cat_name

    def execute(self, cur, conn, user):
        values = self.get_inputs()

        if values[0] == 'assign':
            try:
                result = cur.execute(f"""INSERT INTO tool_categories(barcode, categoryid) VALUES ('{values[1]}',
                    (SELECT categoryid from category WHERE category.categoryname='{values[2]}'))""")
                conn.commit()
                # check for valid results
                if result is None:
                    return "[+][Organize Tools]Assign successful"
            except (psycopg2.DatabaseError) as e:
                conn.rollback()
                print(e)
            finally:
                cur.close()

        if values[0] == 'create':
            try:
                result = cur.execute(f"INSERT INTO category (categoryname) VALUES ('{values[1]}')")
                conn.commit()
                # check for valid results
                if result is None:
                    return "[+][Organize Tools]Create successful"


            except (psycopg2.DatabaseError) as e:
                conn.rollback()
                print(e)
            finally:
                cur.close()

    def toString(self, result) -> str:
        return result

