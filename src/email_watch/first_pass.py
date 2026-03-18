# Example: secure credential input and O365 authentication
from O365 import Account
from dworshak_prompt import Obtain

# Instantiate the prompt handler
prompt = Obtain()

# Ask for client credentials securely
CLIENT_ID = prompt.secret("Enter your O365 Client ID: ")
CLIENT_SECRET = prompt.secret("Enter your O365 Client Secret: ")

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
