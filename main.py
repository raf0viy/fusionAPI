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

    # Get client by ID command
    get_client_parser = subparsers.add_parser("get-client", help="Get a single client by ID")
    get_client_parser.add_argument("--id", type=int, required=True, help="The ID of the client to retrieve")

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

    # Update client command
    update_client_parser = subparsers.add_parser("update-client", help="Update an existing client")
    update_client_parser.add_argument("--id", type=int, required=True, help="The ID of the client to update")
    update_client_parser.add_argument("--name", help="Client's name")
    update_client_parser.add_argument("--lastname", help="Client's last name")
    update_client_parser.add_argument("--phone", help="Client's phone number")
    update_client_parser.add_argument("--email", help="Client's email address")
    update_client_parser.add_argument("--father", help="Client's father name")
    update_client_parser.add_argument("--points", type=int, help="Client's points")
    update_client_parser.add_argument("--id_network", type=int, help="Network ID")
    update_client_parser.add_argument("--id_group", type=int, help="Group ID")
    update_client_parser.add_argument("--gender", choices=['male', 'female'], help="Client's gender")
    update_client_parser.add_argument("--birthday", help="Client's birthday (Y-m-d)")
    update_client_parser.add_argument("--allow_sms", choices=['yes', 'no'], help="Allow SMS notifications")
    update_client_parser.add_argument("--card_number", help="Client's card number")

    # Delete client command
    delete_client_parser = subparsers.add_parser("delete-client", help="Delete a client by ID")
    delete_client_parser.add_argument("--id", type=int, required=True, help="The ID of the client to delete")

    # Refill client balance command
    refill_client_parser = subparsers.add_parser("refill-client", help="Refill a client's balance")
    refill_client_parser.add_argument("--id", type=int, required=True, help="The client's ID")
    refill_client_parser.add_argument("--amount", type=float, required=True, help="The amount to add")
    refill_client_parser.add_argument("--comment", type=str, required=True, help="A comment for the transaction")

    # Get client actions command
    subparsers.add_parser("get-client-actions", help="Get a list of available client actions")

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

        elif args.command == "get-client":
            try:
                client_info = client.get_client(args.id)
                print(json.dumps(client_info, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error getting client: {e}")

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

        elif args.command == "update-client":
            try:
                # Collect the optional arguments
                update_data = {
                    "name": args.name,
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
                # Filter out None values so we only send the fields to be updated
                update_data = {k: v for k, v in update_data.items() if v is not None}

                if not update_data:
                    print("Error: You must provide at least one field to update.")
                    return

                updated_client = client.update_client(args.id, **update_data)
                print("Client updated successfully:")
                print(json.dumps(updated_client, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error updating client: {e}")

        elif args.command == "delete-client":
            try:
                client.delete_client(args.id)
                print(f"Client with ID {args.id} deleted successfully.")
            except Exception as e:
                print(f"Error deleting client: {e}")

        elif args.command == "refill-client":
            try:
                result = client.refill_client_balance(args.id, args.amount, args.comment)
                print("Balance refilled successfully:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error refilling balance: {e}")
        
        elif args.command == "get-client-actions":
            try:
                actions = client.get_client_actions()
                print(json.dumps(actions, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"Error getting client actions: {e}")


if __name__ == "__main__":
    main()
