from application.commands import AcceptRequest, DenyRequest
import psycopg2

request_status=['pending','accepted','denied','completed']

class ManageRequests():

    def get_inputs(self, cur, usr):

        # requests made or received?
        cmd = input('View made (m) or received (r)? : ')

        try:
            if cmd == 'm' or cmd == 'made':
                # view my requests
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.daterequired,r.datereturned, r.status FROM request r, tool t WHERE r.username = %s AND r.barcode = t.barcode", (usr,))
                print("\033[1m | barcode \t| tool name \t| date required \t| date returned \t| status\033[0m")
                for i in cur.fetchall():
                    print(f" | {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  \t|\t {i[3]}\t|\t {request_status[i[4]]}\t|")

                return 'M'

            elif cmd == 'r' or cmd == 'received':
                # view requests for my tools
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.username, r.daterequired, r.datereturned, r.status FROM request r, catalog c, tool t WHERE r.barcode = c.barcode AND r.barcode = t.barcode AND c.username = %s", (usr,))
                print("\033[1m index| barcode \t| tool name \t| from \t| date required \t| date returned\t |status\033[0m")
                idx=0
                for i in cur.fetchall():
                    print(f" {idx}| {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  \t| \t {i[3]} \t|\t {i[4]}\t|\t {request_status[i[5]]}\t|")
                    idx+=1

                return 'R'
        except(psycopg2.DatabaseError) as e:
            print(e)
            return 'X'
        finally:
            cur.close()


    def execute(self, cur, conn, user):

        # query & display all requests
        res = self.get_inputs(cur, user['username'])

        # cur.close()

        if res == 'R':
            action = input("Would you like to accept (a) or deny (d) a request? : ")

            if action == 'a' or action == 'A' or action == 'accept' or action == 'Accept':
                #accept
                AcceptRequest.AcceptRequest().execute(conn.cursor(), conn, user)
            elif action == 'd' or action == 'D' or action == 'deny' or action == 'Deny':
                #deny
                DenyRequest.DenyRequest().execute(conn.cursor(), conn, user)
        elif res == 'X':
            print('error! try again')



    def toString(self) -> str:
        return "none"

