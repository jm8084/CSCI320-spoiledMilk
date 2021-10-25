from application.commands import Login, CreateAccount, ManageCatalog, OrganizeTools, CreateCategory, SearchTool, SortTools, Request, ManageRequests, AcceptRequest, DenyRequest, InspectTools, ReturnTool, DeleteTool
import dbConnect.database_connection as db_conn
import dbConnect.create_tables as tables


# ------ VARIABLES ---------
loggedIn = False
command = ''
command_map = {
}
user = {
    'email': ' ',
    'username': ' ',
    'first': ' ',
    'last': ' '
}

# ------- COMMANDS ---------
HELP = 'help'
LOGIN = 'login'
LOGOUT = 'logout'
EXIT = 'exit'
CREATE_ACCOUNT = 'create-account'
MANAGE_CATALOG = 'manage-catalog'
ORGANIZE_TOOLS = 'organize-tools'
CREATE_CATEGORY = 'create-category'
SEARCH_TOOL = 'search-tool'
SORT_TOOLS = 'sort-tools'
REQUEST = 'request-tool'
MANAGE_REQUESTS = 'manage-requests'
ACCEPT_REQUEST = 'accept-request'
DENY_REQUEST = 'deny-request'
INSPECT_TOOL = 'inspect-tool'
RETURN_TOOL = 'return-tool'
DELETE_TOOL = 'delete-tool'


# ------- CREATE TABLES -----------
def create_tables():

    conn = db_conn.connect()
    curs = conn.cursor()

    tables.create_tables(curs, conn)


# correlate commands to their proper execution
def set_commands(cur):
    print('...complete!')

    global command_map

    # map commands to operations
    command_map = {
        MANAGE_CATALOG: ManageCatalog.ManageCatalog(cur),
        ORGANIZE_TOOLS: OrganizeTools.OrganizeTools(cur),
        CREATE_CATEGORY: CreateCategory.CreateCategory(cur),
        SEARCH_TOOL: SearchTool.SearchTool(cur),
        SORT_TOOLS: SortTools.SortTools(cur),
        REQUEST: Request.Request(cur),
        MANAGE_REQUESTS: ManageRequests.ManageRequests(cur),
        ACCEPT_REQUEST: AcceptRequest.AcceptRequest(cur),
        DENY_REQUEST: DenyRequest.DenyRequest(cur),
        INSPECT_TOOL: InspectTools.InspectTools(cur),
        RETURN_TOOL: ReturnTool.ReturnTool(cur),
        DELETE_TOOL: DeleteTool.DeleteTool(cur)
    }

# break down input
def handle_command(cmd):

    response = ''

    try:
        if (loggedIn):
            response = command_map[cmd].execute()
        else:
            response = 'login before executing any commands!'
    except:
        response = f"\n...Invalid command!\nUse command '{HELP}' for user manual\n\n"

    return response

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

    man = f"""
     *********************\033[91m----- USER MANUAL -----\033[0m*********************
  
    \033[92m------- General Commands ------- \033[0m
    -\033[36m {HELP} \033[0m            : Display user manual
    -\033[36m {LOGIN} \033[0m
    -\033[36m {LOGOUT} \033[0m
    -\033[36m {CREATE_ACCOUNT} \033[0m 
    -\033[36m {EXIT} \033[0m            : kill application
     
    \033[92m------- User Commands ------- \033[0m
    -\033[36m {MANAGE_CATALOG} \033[0m  : add/edit/delete tools from your catalog
    -\033[36m {ORGANIZE_TOOLS} \033[0m  : organize your tools into categories 
    -\033[36m {CREATE_CATEGORY} \033[0m : create a tool category
    -\033[36m {SEARCH_TOOL} \033[0m     : search tools by barcode, name, or category (default: name)
    -\033[36m {SORT_TOOLS} \033[0m      : sort tools by name or category; ascending or descending
    -\033[36m {REQUEST} \033[0m 
    -\033[36m {MANAGE_REQUESTS} \033[0m 
    -\033[36m {ACCEPT_REQUEST} \033[0m 
    -\033[36m {DENY_REQUEST} \033[0m
    -\033[36m {INSPECT_TOOL} \033[0m
    -\033[36m {RETURN_TOOL} \033[0m
    -\033[36m {DELETE_TOOL} \033[0m
    *********************\033[91m--- End manual ---\033[0m*********************
    """

    return man

#
def login(cmd, cur):
    global loggedIn, user

    user_data = ''

    if(cmd == LOGIN):
        usr_data = Login.Login(cur).execute()
    else:
        usr_data = CreateAccount.CreateAccount(cur).execute()


    print('...logging in')
    loggedIn = True

#
def logout():
    global loggedIn

    print('...logging out')
    loggedIn = False

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
    while(command != EXIT):

        command = input('--> ')

        if(command == EXIT):
            print('bye!')
        elif(command == HELP):
            print(prompt())
        elif(command == LOGIN or command == CREATE_ACCOUNT):
            login( command, cur)
        elif(command == LOGOUT):
            logout()
        else:
            print(handle_command(command))

    # close db & cursor connection
    cur.close()
    conn.close()


application()