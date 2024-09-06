import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from cryptography.fernet import Fernet

# Класс для клиента с интерфейсом и шифрованием
class ClientGUI:
    def __init__(self, master, encryption_key):
        self.master = master
        self.master.title("Клиент Чата с Шифрованием")
        
        # Текстовое поле для вывода сообщений
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled')
        self.text_area.pack(pady=10, padx=10)

        # Поле для ввода сообщений
        self.entry = tk.Entry(master)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Кнопка отправки сообщения
        self.send_button = tk.Button(master, text="Отправить", command=self.send_message)
        self.send_button.pack(pady=5)

        # Сокет клиента и шифрование
        self.client_socket = None
        self.fernet = Fernet(encryption_key)

        # Подключение к серверу
        self.connect_to_server()

    # Подключение к серверу
    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 5003))  # Подключаемся к localhost на порту 5003
            self.log_message("Подключено к серверу.")
            
            # Запускаем поток для получения сообщений от сервера
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.log_message(f"Ошибка подключения: {e}")

    # Получение сообщений от сервера
    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    # Расшифровка сообщения
                    message = self.fernet.decrypt(encrypted_message).decode()
                    self.log_message(f"Сообщение от сервера: {message}")
            except Exception as e:
                self.log_message(f"Ошибка при получении сообщения: {e}")
                self.client_socket.close()
                break

    # Отправка сообщений на сервер
    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            try:
                # Шифрование сообщения
                encrypted_message = self.fernet.encrypt(message.encode())
                self.client_socket.send(encrypted_message)
                self.log_message(f"Вы: {message}")
                self.entry.delete(0, tk.END)
            except Exception as e:
                self.log_message(f"Ошибка при отправке сообщения: {e}")

    # Логирование сообщений в текстовое поле
    def log_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

# Запуск интерфейса клиента
def run_client(encryption_key):
    root = tk.Tk()
    gui = ClientGUI(root, encryption_key)
    root.mainloop()

if __name__ == "__main__":
    # Введите ключ шифрования, который был сгенерирован на сервере
    encryption_key = input("Введите ключ шифрования: ").encode()

    run_client(encryption_key)

