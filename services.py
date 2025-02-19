# services.py

"""
Services module that holds shared data and helper functions used by the application.
In a real-world scenario, you would replace this with database queries, secure file
storage integrations, etc.
"""

# Example client data
clients_data = {
    "1234": {"name": "John Doe",  "email": "john@example.com"},
    "5678": {"name": "Jane Smith","email": "jane@example.com"}
}

def check_credentials(client_id_input: str) -> bool:
    """
    Checks if the client_id_input matches one of the known clients.
    For simplicity, we use the client ID itself as the 'password'.
    """
    return client_id_input in clients_data

def generate_mandate_download_link() -> str:
    """
    Returns a link to the mandate PDF. In a real app, you might
    generate this file dynamically, or pull from secure storage.
    """
    return "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
