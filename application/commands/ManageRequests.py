from application.commands import AcceptRequest, DenyRequest


class ManageRequests():

    def get_inputs(self, cur, usr):

        # requests made or received?
        cmd = input('View made (m) or received (r)? : ')

        try:
            if cmd == 'm' or cmd == 'made':
                # view my requests
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.daterequired FROM request r, tool t WHERE r.username = %s AND r.barcode = t.barcode", (usr,))
                print("\033[1m | barcode \t| tool name \t| date required \033[0m")
                for i in cur.fetchall():
                    print(f" | {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  |")

                return 'M'

            elif cmd == 'r' or cmd == 'received':
                # view requests for my tools
                cur.execute("SELECT DISTINCT r.barcode, t.name, r.username, r.daterequired FROM request r, catalog c, tool t WHERE r.barcode = c.barcode AND r.barcode = t.barcode c.username = %s", (usr,))
                print("\033[1m | barcode \t| tool name \t| from \t| date required \033[0m")
                for i in cur.fetchall():
                    print(f" | {i[0]}  \t\t| \t {i[1]}  \t| \t {i[2]}  \t| \t {i[3]} |")

                return 'R'
        except:
            return 'X'


    def execute(self, cur, conn, user):

        # query & display all requests
        res = self.get_inputs(cur, user['username'])

        cur.close()

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

