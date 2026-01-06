import argparse
import os
import json
from fusionpos.client import FusionPOSClient

AUTH_FILE = "auth.json"

def save_auth_info(token, domain):
    with open(AUTH_FILE, "w") as f:
        json.dump({"token": token, "domain": domain}, f)

def load_auth_info():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return None

def main():
    parser = argparse.ArgumentParser(description="FusionPOS API client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Login command
    login_parser = subparsers.add_parser("login", help="Login to get an auth token")
    login_parser.add_argument("--domain", required=True, help="Your FusionPOS domain (e.g., 'mycompany')")
    login_parser.add_argument("--username", required=True, help="Your FusionPOS username")
    login_parser.add_argument("--password", required=True, help="Your FusionPOS password")

    # Get clients command
    subparsers.add_parser("get-clients", help="Get all clients")

    # Add client command
    add_client_parser = subparsers.add_parser("add-client", help="Add a new client")
    add_client_parser.add_argument("--name", required=True, help="Client's name")
    add_client_parser.add_argument("--lastname", help="Client's last name")
    add_client_parser.add_argument("--phone", help="Client's phone number")
    add_client_parser.add_argument("--email", help="Client's email address")
    # Add other optional fields from SaveClientDto as needed
    add_client_parser.add_argument("--father", help="Client's father name")
    add_client_parser.add_argument("--points", type=int, help="Client's points")
    add_client_parser.add_argument("--id_network", type=int, required=True, help="Network ID (required)")
    add_client_parser.add_argument("--id_group", type=int, required=True, help="Group ID (required)")
    add_client_parser.add_argument("--gender", choices=['male', 'female'], help="Client's gender")
    add_client_parser.add_argument("--birthday", help="Client's birthday (Y-m-d)")
    add_client_parser.add_argument("--allow_sms", choices=['yes', 'no'], help="Allow SMS notifications")
    add_client_parser.add_argument("--card_number", help="Client's card number")


    args = parser.parse_args()

    if args.command == "login":
        try:
            client = FusionPOSClient(domain=args.domain)
            client.login(args.username, args.password)
            save_auth_info(client.token, args.domain)
            print(f"Authentication info saved to {AUTH_FILE}")
        except Exception as e:
            print(f"Error during login: {e}")
            return
    else:
        # For other commands, load auth info
        auth_info = load_auth_info()
        if not auth_info:
            print("You are not logged in. Please run 'python main.py login --domain <domain> --username <user> --password <pass>' first.")
            return
        
        client = FusionPOSClient(domain=auth_info["domain"])
        client.token = auth_info["token"]

        if args.command == "get-clients":
            try:
                clients = client.get_clients()
                print(json.dumps(clients, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error getting clients: {e}")

        elif args.command == "add-client":
            try:
                # Collect the optional arguments
                client_data = {
                    "lastname": args.lastname,
                    "phone": args.phone,
                    "email": args.email,
                    "father": args.father,
                    "points": args.points,
                    "id_network": args.id_network,
                    "id_group": args.id_group,
                    "gender": args.gender,
                    "birthday": args.birthday,
                    "allow_sms": args.allow_sms,
                    "card_number": args.card_number,
                }
                # Filter out None values
                client_data = {k: v for k, v in client_data.items() if v is not None}
                
                new_client = client.add_client(name=args.name, **client_data)
                print("Client added successfully:")
                print(json.dumps(new_client, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error adding client: {e}")


if __name__ == "__main__":
    main()
