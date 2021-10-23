from application.commands import CreateAccount, ManageCatalog, OrganizeTools, CreateCategory, SearchTool, SortTools, Request, ManageRequests, AcceptRequest, DenyRequest, InspectTools, ReturnTool, DeleteTool
import dbConnect.database_connection as db_conn

# ------ VARIABLES ---------
loggedIn = False
command = ''
command_map = {
}

#
def set_commands(cur):
    print('...complete!')

    global command_map

    # map commands to operations
    command_map = {
        "manage category": ManageCatalog.ManageCatalog(cur),
        "organize tools": OrganizeTools.OrganizeTools(cur),
        "create category": CreateCategory.CreateCategory(cur),
        "search tool": SearchTool.SearchTool(cur),
        "request": Request.Request(cur),
        "manage request": ManageRequests.ManageRequests(cur),
        "accept request": AcceptRequest.AcceptRequest(cur),
        "deny request": DenyRequest.DenyRequest(cur),
        "inspect tools": InspectTools.InspectTools(cur),
        "return tool": ReturnTool.ReturnTool(cur),
        "delete tool": DeleteTool.DeleteTool(cur)
    }

# break down input
def handle_command(cmd):

    try:
        if (loggedIn):
            command_map[cmd]
        else:
            print('login before executing any commands!')
    except:
        print('invalid command')
        prompt()

    return ''

# display all commands / instructions on screen
def prompt():

    # PURPLE = '\033[95m'
    # CYAN = '\033[96m'
    # DARKCYAN = '\033[36m'
    # BLUE = '\033[94m'
    # GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    # RED = '\033[91m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'
    # END = '\033[0m'

    man = """
         *********************\033[91m----- USER MANUAL -----\033[0m*********************
         
        \033[1m Command format: \033[0m
        -> \033[36m command name \033[0m [required param] {filter options}
      
        \033[92m------- General Commands ------- \033[0m
        -\033[36m help \033[0m
            Display user manual
        -\033[36m login \033[0m [username. password]
        -\033[36m logout \033[0m
        -\033[36m create account \033[0m [first name, last name, username, email, password]
        -\033[36m exit \033[0m 
            kill application
         
        \033[92m------- User Commands ------- \033[0m
        -\033[36m manage catalog \033[0m
            add/edit/delete tools from your catalog
        -\033[36m organize tools \033[0m
            organize your tools into categories 
        -\033[36m create category \033[0m [name]
            create a tool category
        -\033[36m search tool \033[0m {barcode, name, category} 
            search tools by barcode, name, or category (default: name)
        -\033[36m sort tools \033[0m [{name, category}, {ascending, descending}] 
            sort tools by name or category; ascending or descending
        -\033[36m request \033[0m 
        -\033[36m manage requests \033[0m {made, received} 
        -\033[36m accept request \033[0m [request ID] 
        -\033[36m deny request \033[0m [request ID] 
        -\033[36m inspect tools \033[0m
        -\033[36m return tool \033[0m [barcode] 
        -\033[36m delete tool \033[0m [barcode] 
        
        *********************\033[91m--- End manual ---\033[0m*********************
    """

    return man

#
def login():
    print('logging in')


#
def logout():
    print('logging out')
    pass

#
def application():

    global command
    # connect to db & get cursor
    conn = db_conn.connect()
    cur = conn.cursor()

    # init command list
    set_commands(cur)

    # display user manual at startup
    print(prompt())

    # while command not exit
    while(command != 'exit'):

        command = input(' -> ')

        if(command == 'exit'):
            print('bye!')
        elif(command == 'help'):
            print(prompt())
        elif(command == 'create account'):
            CreateAccount.CreateAccount(cur).parse(command)
        elif(command == 'login'):
            login()
        elif(command == 'logout'):
            logout()
        else:
            handle_command(command)

    # close db & cursor connection
    cur.close()
    conn.close()


application()
