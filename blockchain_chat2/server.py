import socket
import threading
from cryptography.fernet import Fernet
from blockchain import Blockchain  # Импортируем блокчейн

# Класс для организации чата с использованием блокчейна и шифрованием
class BlockchainChat:
    def __init__(self, encryption_key):
        self.clients = []  # Список подключенных клиентов
        self.blockchain = Blockchain()  # Инициализация блокчейна
        self.fernet = Fernet(encryption_key)  # Инициализация шифрования с ключом

    # Запуск сервера
    def start_server(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Сервер запущен на {host}:{port}, ожидаем подключения клиентов...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Подключен клиент с адресом: {addr}")
            self.clients.append(client_socket)
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

    # Обработка клиента
    def handle_client(self, client_socket, addr):
        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if encrypted_message:
                    # Расшифровка сообщения
                    message = self.fernet.decrypt(encrypted_message).decode()
                    # Добавляем сообщение от клиента в блокчейн
                    self.blockchain.add_block(message)
                    print(f"Новое сообщение от {addr}: {message}")

                    # Шифрование ответа
                    response = self.fernet.encrypt(f"Сообщение добавлено в блокчейн: {message}".encode())
                    client_socket.send(response)
                else:
                    break
            except Exception as e:
                print(f"Ошибка при получении сообщения от {addr}: {e}")
                break
        client_socket.close()

    # Функция для отправки сообщения всем клиентам от сервера
    def send_message_to_clients(self, message):
        # Добавляем сообщение сервера в блокчейн
        self.blockchain.add_block(message)
        print(f"Сообщение от сервера добавлено в блокчейн: {message}")

        # Отправляем зашифрованное сообщение всем клиентам
        encrypted_message = self.fernet.encrypt(message.encode())
        for client_socket in self.clients:
            try:
                client_socket.send(encrypted_message)
                print(f"Отправлено сообщение: {message}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения клиенту: {e}")
                self.clients.remove(client_socket)

    # Функция для просмотра состояния блокчейна (без изменений)
    def blockchain_status(self):
        print("\n=== Статус блокчейна ===")
        print(f"Количество блоков: {len(self.blockchain.chain)}")
        print(f"Последний хэш: {self.blockchain.get_latest_block().hash}")
        print("=========================")

    # Функция для проверки валидности блокчейна (без изменений)
    def validate_blockchain(self):
        print("\n=== Проверка целостности блокчейна ===")
        if self.blockchain.is_chain_valid():
            print("Блокчейн валиден.")
        else:
            print("Обнаружена ошибка в блокчейне!")
        print("=========================")

    # Функция для просмотра логов всех блоков (без изменений)
    def view_blockchain(self):
        print("\n=== Логи блокчейна (цепочка блоков) ===")
        for block in self.blockchain.chain:
            print(f"Индекс: {block.index}")
            print(f"Предыдущий хэш: {block.previous_hash}")
            print(f"Сообщение (данные): {block.data}")
            print(f"Текущий хэш: {block.hash}")
            print(f"Время: {block.timestamp}")
            print("="*30)

# Основная логика программы
if __name__ == "__main__":
    # Генерация и печать ключа шифрования (используйте этот ключ на клиенте)
    encryption_key = Fernet.generate_key()
    print(f"Ключ шифрования: {encryption_key.decode()}")

    chat = BlockchainChat(encryption_key)

    # Запуск сервера в отдельном потоке
    server_thread = threading.Thread(target=chat.start_server, args=("localhost", 5003))
    server_thread.start()

    # Сервер может отправлять сообщения клиентам и просматривать блокчейн
    while True:
        command = input("Введите команду ('send', 'view', 'status', 'validate'): ").strip()
        if command == "send":
            message = input("Введите сообщение для отправки клиентам: ")
            chat.send_message_to_clients(message)
        elif command == "view":
            chat.view_blockchain()
        elif command == "status":
            chat.blockchain_status()
        elif command == "validate":
            chat.validate_blockchain()
        else:
            print("Неверная команда! Введите 'send', 'view', 'status' или 'validate'.")
