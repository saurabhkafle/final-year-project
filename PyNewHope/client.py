import socket
import pickle
from utils import encrypt_message, decrypt_message, hash_key
import newhope

def send_message(sock, message):
    serialized_message = pickle.dumps(message)
    message_length = len(serialized_message)
    sock.sendall(message_length.to_bytes(4, 'big') + serialized_message)

def receive_message(sock):
    raw_message_length = sock.recv(4)
    if not raw_message_length:
        return None
    message_length = int.from_bytes(raw_message_length, 'big')
    data = b''
    while len(data) < message_length:
        packet = sock.recv(message_length - len(data))
        if not packet:
            return None
        data += packet
    return pickle.loads(data)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 1234)
    client_socket.connect(server_address)


    client_message = "client's NewHope public key"
    send_message(client_socket, client_message)
    Bank_response = receive_message(client_socket)


    shared_key = b"Example shared key from NewHope"
    aes_key = hash_key(shared_key)
    print("Key exchange success. Shared AES key established.")
    print(f"Shared AES Key: {aes_key.hex()}")

    while True:
        message = input("client: ")
        if message.lower() == 'exit':
            break
        encrypted_message = encrypt_message(aes_key, message)
        send_message(client_socket, encrypted_message)

        encrypted_response = receive_message(client_socket)
        response = decrypt_message(aes_key, encrypted_response)
        print("Bank:", response)

    client_socket.close()

if __name__ == '__main__':
    main()
