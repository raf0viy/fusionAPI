import requests

class FusionPOSClient:
    def __init__(self, domain):
        self.base_url = f"https://{domain}.fusionpos.ru/"
        self.token = None

    def login(self, username, password):
        """Logs in to the FusionPOS API and saves the token."""
        url = f"{self.base_url}api/v2/auth"
        credentials = {"username": username, "password": password}
        response = requests.post(url, json=credentials)
        response.raise_for_status()  # Raise an exception for bad status codes
        self.token = response.json().get("token")
        if not self.token:
            raise Exception("Authentication failed, token not received.")
        print("Login successful.")

    def _get_auth_headers(self):
        if not self.token:
            raise Exception("You must log in before making API calls.")
        return {"Authorization": f"Bearer {self.token}"}

    def get_clients(self):
        """Gets all clients."""
        url = f"{self.base_url}api/v2/clients"
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_client(self, client_id):
        """Gets a single client by their ID."""
        url = f"{self.base_url}api/v2/clients/{client_id}"
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def add_client(self, name, lastname=None, phone=None, email=None, **kwargs):
        """Adds a new client."""
        url = f"{self.base_url}api/v2/clients"
        headers = self._get_auth_headers()
        client_data = {"name": name}
        if lastname:
            client_data["lastname"] = lastname
        if phone:
            client_data["phone"] = phone
        if email:
            client_data["email"] = email
        client_data.update(kwargs)
        
        response = requests.post(url, headers=headers, json=client_data)
        
        if response.status_code == 422:
            try:
                error_details = response.json()
                raise Exception(f"Data Validation Failed: {error_details}")
            except requests.exceptions.JSONDecodeError:
                # Fallback if the error response is not JSON
                response.raise_for_status()

        response.raise_for_status()
        return response.json()

    def update_client(self, client_id, **kwargs):
        """Updates an existing client."""
        url = f"{self.base_url}api/v2/clients/{client_id}"
        headers = self._get_auth_headers()
        
        response = requests.patch(url, headers=headers, json=kwargs)
        
        if response.status_code == 422:
            try:
                error_details = response.json()
                raise Exception(f"Data Validation Failed: {error_details}")
            except requests.exceptions.JSONDecodeError:
                response.raise_for_status()

        response.raise_for_status()
        return response.json()

    def delete_client(self, client_id):
        """Deletes a client by their ID."""
        url = f"{self.base_url}api/v2/clients/action/delete"
        headers = self._get_auth_headers()
        data = {"id": client_id}
        
        response = requests.patch(url, headers=headers, json=data)
        
        response.raise_for_status()
        return response.json()

    def refill_client_balance(self, client_id, amount, comment):
        """Refills a client's balance."""
        url = f"{self.base_url}api/v2/clients/{client_id}/refill"
        headers = self._get_auth_headers()
        data = {"amount": amount, "comment": comment}
        
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code == 422:
            try:
                error_details = response.json()
                raise Exception(f"Data Validation Failed: {error_details}")
            except requests.exceptions.JSONDecodeError:
                response.raise_for_status()

        response.raise_for_status()
        return response.json()

    def get_client_actions(self):
        """Gets the list of available client actions."""
        url = f"{self.base_url}api/v2/clients/actions"
        headers = self._get_auth_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

