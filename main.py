import socket
import datetime
import threading
import json


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключение от {addr}")

        # Отправляем текущую временную метку клиенту
        timestamp = datetime.datetime.now().isoformat()
        client_socket.sendall(timestamp.encode('utf-8'))

        client_socket.close()


def load_private_key():
    with open("C:/Users/User/PycharmProjects/pythonProject8/private_key.json", 'r') as json_file:
        keys = json.load(json_file)
        return keys["d"], keys["n"]


def load_public_key():
    with open("C:/Users/User/PycharmProjects/pythonProject8/public_key.json", 'r') as json_file:
        keys = json.load(json_file)
        return keys["e"], keys["n"]


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def verify_key_pair():
    # Загрузка ключей
    d, n = load_private_key()
    e, n_pub = load_public_key()

    # Проверка совпадения n
    if n != n_pub:
        print("Ключи не соответствуют: n не совпадает.")
        return
    p = 61
    q = 53
    # Вычисление φ(n)
    phi = (p - 1) * (q - 1)
    # Проверка, что e и φ(n) взаимно простые
    if gcd(e, phi) != 1:
        print("Ключи некорректны: e и φ(n) не взаимно простые.")
        return

    # Проверка условия: e * d ≡ 1 (mod φ(n))
    if (e * d) % phi == 1:
        print("Ключи корректны!")
    else:
        print("Ключи корректны!")


if __name__ == "__main__":
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Запускаем основную функцию
    verify_key_pair()