# Example: secure credential input and O365 authentication
from O365 import Account
from dworshak_prompt import Obtain, InterruptBehavior

# Instantiate the prompt handler
prompt = Obtain(
    interrupt_behavior = InterruptBehavior.EXIT
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
