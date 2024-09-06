import socket
import threading
from cryptography.fernet import Fernet

# Функция для обработки зашифрованных сообщений от сервера
def receive_messages(client_socket, fernet):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if encrypted_message:
                # Расшифровка сообщения
                message = fernet.decrypt(encrypted_message).decode()
                print(f"Сообщение от сервера: {message}")
        except Exception as e:
            print(f"Ошибка при получении сообщения: {e}")
            client_socket.close()
            break

# Функция для отправки зашифрованных сообщений на сервер
def send_message(message, target_host, target_port, fernet):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_host, target_port))
        print(f"Подключен к серверу {target_host}:{target_port}")

        # Запуск потока для получения зашифрованных сообщений от сервера
        threading.Thread(target=receive_messages, args=(client_socket, fernet)).start()

        # Шифрование сообщения
        encrypted_message = fernet.encrypt(message.encode())
        client_socket.send(encrypted_message)
        print(f"Отправлено зашифрованное сообщение: {message}")

    except Exception as e:
        print(f"Ошибка при подключении или отправке сообщения: {e}")

if __name__ == "__main__":
    # Вставьте здесь тот же ключ шифрования, который был сгенерирован на сервере
    encryption_key = input("Введите ключ шифрования: ").encode()

    fernet = Fernet(encryption_key)

    while True:
        # Ввод сообщения для отправки на сервер
        message = input("Введите сообщение для отправки на сервер: ")
        # Используем localhost вместо IP-адреса сервера и порт (5003)
        send_message(message, "localhost", 5003, fernet)
