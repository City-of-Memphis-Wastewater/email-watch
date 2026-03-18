# Example: secure credential input and O365 authentication
from O365 import Account
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
CLIENT_ID = prompt.secret(service="o365",item="CLIENT_ID",message="Enter your O365 Client ID: ").value
CLIENT_SECRET = prompt.secret(service="o365",item="CLIENT_SECRET",message="Enter your O365 Client Secret: ").value

# Prepare credentials tuple
credentials = (CLIENT_ID, CLIENT_SECRET)

# Initialize O365 account
account = Account(credentials)

# Authenticate (interactive for first-time login)
if not account.is_authenticated:
    account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read'])

# Access mailbox and list folders
mailbox = account.mailbox()
folders = mailbox.list_folders()

print("Mailbox folders:")
for folder in folders:
    print("-", folder.name)
