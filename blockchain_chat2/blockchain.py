import hashlib
import time

# Класс блока блокчейна
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

# Класс блокчейна
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    # Создаем генезис-блок (первый блок)
    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))

    # Вычисляем хеш для блока
    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + previous_hash + str(timestamp) + data
        return hashlib.sha256(value.encode()).hexdigest()

    # Получаем последний блок в цепочке
    def get_latest_block(self):
        return self.chain[-1]

    # Добавляем новый блок в цепочку
    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_index = latest_block.index + 1
        new_timestamp = time.time()
        new_hash = self.calculate_hash(new_index, latest_block.hash, new_timestamp, data)
        new_block = Block(new_index, latest_block.hash, new_timestamp, data, new_hash)
        self.chain

