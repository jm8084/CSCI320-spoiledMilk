from datetime import date

class ToolsStatistics():

    def get_inputs(self):
        pass


    def execute(self, cur, conn, user):
        # display = self.get_inputs()
        try:
            # if display == 'available' or display == 'all':

            # Select all shareable tools except when they're in the request table and request status = approved
            cur.execute(f"""SELECT COUNT(t.barcode), t.barcode, t.name
                            FROM ((catalog c INNER JOIN request r on c.barcode = r.barcode)
                            INNER JOIN tool t on r.barcode = t.barcode)
                            WHERE r.username = '{user['username']}' AND (r.status = 1 OR r.status=3)
                            GROUP BY t.barcode
                            ORDER BY COUNT(t.barcode) DESC""")

            # Print the header row
            rows = cur.fetchmany(10)
            print(f"Top 10 Most Frequently borrowed tools")
            print(f"\033[1m | order \t| frequency \t| barcode \t| tool name \033[0m")
            idx=1
            for row in rows:
                print(f" | {idx}.  \t\t| \t {row[0]}  \t\t| \t {row[1]}  \t|\t {row[2]}")
                idx +=1



                # Select needed data for any tool that is in the request table and the tool is owned by the user
                # and the status of that request is 1 or 'approved'
            cur.execute(f"""SELECT t.barcode, t.name,AVG(r.datereturned - r.daterequired) as lent_time,
                            (CURRENT_DATE - t.purchasedate)-SUM(r.datereturned - r.daterequired) as available_time,
                            cast(SUM(r.datereturned - r.daterequired) as float) / cast(((CURRENT_DATE - t.purchasedate)-SUM(r.datereturned - r.daterequired))as float) as ratio
                            FROM ((catalog c INNER JOIN request r on c.barcode = r.barcode)
                            INNER JOIN tool t on r.barcode = t.barcode)
                            WHERE c.username = '{user['username']}' AND (r.status = 1 OR r.status = 3)
                            GROUP BY t.barcode
                            ORDER BY ratio DESC""")

            rows = cur.fetchmany(10)
            print(f"Top 10 Most Frequently lent tools")
            print(f"\033[1m | order \t| average days lent \t| days available \t| % of time lent \t| barcode \t\t| tool name \033[0m")
            idx = 1
            for row in rows:
                print(f" | {idx}.  \t\t| \t {row[2]:5.2f}  \t\t\t| \t {row[3]:5}  \t\t|\t {row[4]*100:5.2f} \t\t\t| \t {row[0]:7}  \t| \t {row[1]}")
                idx += 1

        except Exception as e:
            print("Error getting records")
            print(e)

        finally:
            cur.close()
            return ''

    def toString(self, rows) -> str:
        return ''

