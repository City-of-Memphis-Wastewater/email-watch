# Example: secure credential input and O365 authentication
from O365 import Account, FileSystemTokenBackend
from dworshak_prompt import Obtain, InterruptBehavior, PromptMode
import os
import logging
logger=logging.getLogger(__name__)

avoid_set = set()
DWO_AVOID_CONSOLE = os.environ.get('DWO_AVOID_CONSOLE')
if  DWO_AVOID_CONSOLE == "1":
    avoid_set.add(PromptMode.CONSOLE)
else:
    logger.warning("Use 'export DWO_AVOID_CONSOLE=1 to avoid the console, to make enable unhiding hidden input.'")
logger.debug(f"{avoid_set=}")
logger.debug(f"{DWO_AVOID_CONSOLE=}") 
    
# Instantiate the prompt handler
prompt = Obtain(
    interrupt_behavior = InterruptBehavior.EXIT,
    interface_avoid = avoid_set
)

# Ask for client credentials securely
CLIENT_ID = prompt.secret(service="o365",item="CLIENT_ID_PAVLOV_EMAIL_WATCH",message="Enter your O365 Client ID: ").value
CLIENT_SECRET = prompt.secret(service="o365",item="CLIENT_SECRET_PAVLOV_EMAIL_WATCH",message="Enter your O365 Client Secret: ").value

# Prepare credentials tuple
credentials = (CLIENT_ID, CLIENT_SECRET)

# Stores the token in a hidden folder
token_backend = FileSystemTokenBackend(token_path='.tokens', token_filename='microsoft_token.txt')
account = Account(credentials, tenant_id='consumers', token_backend=token_backend)

# Initialize O365 account
#account = Account(credentials, tenant_id='consumers')

# Authenticate (interactive for first-time login)
if not account.is_authenticated:
    account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read', 'offline_access'])

# Access mailbox and list folders
mailbox = account.mailbox()
folders = mailbox.list_folders()

print("Mailbox folders:")
for folder in folders:
    print("-", folder.name)
