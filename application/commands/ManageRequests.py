# from application.commands import AcceptRequest, DenyRequest
import psycopg2
from datetime import date

request_status=['pending','accepted','denied','completed','deleted']

class ManageRequests():

    def get_inputs(self, cur, usr):

        # requests made or received?
        cmd = input('View made (m) or received (r)? : ')

        return cmd

    def execute(self, cur, conn, user):

        # query & display all requests
        res = self.get_inputs(cur, user['username'])

        try:
            if ((res == 'm') or (res == 'made')):
                # view my requests
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.daterequired,r.datereturned, r.status FROM request r, tool t WHERE r.username = %s AND r.barcode = t.barcode", (user['username'],))
                print("\033[1m | barcode \t| tool name \t| date required \t| date returned \t| status\033[0m")
                requests = cur.fetchall()
                idx=0
                for i in requests:
                    print(f" {idx}| {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  \t|\t {i[3]}\t|\t {request_status[i[4]]}\t|")
                    idx+=1
                # return ''

                action = input("Would you like to return a tool 'yes' or 'no', default 'no' : ")
                if (action==""):
                    action='no'
                    return ""

                if (action=='yes'):
                    index = input("What is the index of the request for the tool you want to return: ")
                    selected_request = requests[int(index)]
                    # print(selected_request)
                    return_date = date.today().strftime("%Y-%m-%d")
                    try:
                        stat_result = cur.execute(
                            f"UPDATE request SET status = 3 WHERE barcode = {selected_request[0]} AND username = '{user['username']}' AND daterequired = '{selected_request[2]}' AND datereturned = '{selected_request[3]}'")

                        conn.commit()
                        date_result = cur.execute(
                            f"UPDATE request SET datereturned = '{return_date}' WHERE barcode = {selected_request[0]} AND username = '{user['username']}' AND daterequired = '{selected_request[2]}' AND status = 3")

                        conn.commit()

                        # print(stat_result)
                        # print(date_result)
                        # check for valid results
                        if (stat_result is None) and (date_result is None):
                            return '[+][Manage Request]Return Tool successful'

                    except (psycopg2.DatabaseError) as e:

                        conn.rollback()

                        print(e)

            elif ((res == 'r') or (res == 'received')):
                # view requests for my tools
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.username, r.daterequired, r.datereturned, r.status FROM request r, catalog c, tool t WHERE r.barcode = c.barcode AND r.barcode = t.barcode AND c.username = %s", (user['username'],))
                print("\033[1m index| barcode \t| tool name \t| from \t| date required \t| date returned\t |status\033[0m")
                idx=0
                requests=cur.fetchall()

                for i in requests:
                    print(f" {idx}| {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  \t| \t {i[3]} \t|\t {i[4]}\t|\t {request_status[i[5]]}\t|")
                    idx+=1

                action = input("Would you like to accept (a) or deny (d) a request? : ")

                if action == 'a' or action == 'A' or action == 'accept' or action == 'Accept':
                        # accept
                    index = input("What is the index of the request you would like to accept: ")
                    due_date = input("Change the due date of the tool, leave blank to not change YYYY-MM-DD: ")
                    try:
                        selected_request=requests[int(index)]
                        if(due_date==""):
                            due_date=selected_request[4]

                        stat_result = cur.execute(
                             f"UPDATE request SET status = 1 WHERE barcode = {selected_request[0]} AND username = '{selected_request[2]}' AND daterequired = '{selected_request[3]}' AND datereturned = '{selected_request[4]}'")

                        conn.commit()
                        date_result = cur.execute(
                             f"UPDATE request SET datereturned = '{due_date}' WHERE barcode = {selected_request[0]} AND username = '{selected_request[2]}' AND daterequired = '{selected_request[3]}' AND status = 1")

                        conn.commit()

                        # print(stat_result)
                        # print(date_result)
                        # check for valid results
                        if (stat_result is None) and (date_result is None):
                            return '[+][Manage Request]Approve request successful'

                    except (psycopg2.DatabaseError) as e:

                        conn.rollback()

                        print(e)

                elif action == 'd' or action == 'D' or action == 'deny' or action == 'Deny':
                        # deny
                    index = input("What is the index of the request you would like to deny: ")
                    try:
                        selected_request = requests[int(index)]
                        result = cur.execute(
                            f"UPDATE request SET status = 2 WHERE barcode = {selected_request[0]} AND username = '{selected_request[2]}' AND daterequired = '{selected_request[3]}' AND datereturned = '{selected_request[4]}'")

                        conn.commit()

                        # print(result)
                        # check for valid results
                        if result is None:
                            return '[+][Manage Request]Deny request successful'

                    except (psycopg2.DatabaseError) as e:

                        conn.rollback()

                        print(e)
        except(psycopg2.DatabaseError) as e:
            print(e)
            return 'X'
        finally:
            cur.close()

    def toString(self) -> str:
        return ""

