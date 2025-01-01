import requests

BASE_URL = "http://127.0.0.1:5000"

def close_server(lobby_code):
    """
    Sends a POST request to close a server.
    """
    payload = {"lobby_code": lobby_code}
    response = requests.post(f"{BASE_URL}/close", json=payload)
    if response.ok:
        print(f"Server '{lobby_code}' closed successfully.")
    else:
        print(f"Failed to close server: {response.status_code} - {response.json()}")


def get_servers():
    """
    Sends a GET request to retrieve the list of active servers.
    """
    response = requests.get(f"{BASE_URL}/servers")
    if response.ok:
        servers = response.json().get('servers', [])
        if servers:
            print("Active servers:")
            for server in servers:
                print(f"- Lobby Name: {server.get('lobby_name', 'Unknown')}, "
                      f"Lobby Code: {server.get('lobby_code', 'N/A')}, "
                      f"Players: {server.get('current_players', 0)}/{server.get('max_players', 0)}, "
                      f"18+: {'Yes' if server.get('18plus', False) else 'No'}")
        else:
            print("No active servers.")
    else:
        print(f"Failed to retrieve servers: {response.status_code} - {response.json()}")


def close_server_by_code():
    """
    Prompts the user to input a lobby code and closes the corresponding server.
    """
    lobby_code = input("Enter the lobby code of the server you want to close: ")
    close_server(lobby_code)


if __name__ == "__main__":
    print("\nClosing a server by user input...")
    close_server_by_code()

    print("\nRetrieving active servers after closing a server...")
    get_servers()
