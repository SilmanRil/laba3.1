import os
import base64
import socket
import datetime
import threading


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))  # Связываем сокет с адресом и портом
    server_socket.listen(1)  # Ожидаем подключения от клиента
    print("Сервер запущен и ожидает подключения...")

    while True:
        client_socket, addr = server_socket.accept()  # Принимаем подключение
        print(f"Подключение от {addr}")

        # Отправляем текущую временную метку клиенту
        timestamp = datetime.datetime.now().isoformat()
        client_socket.sendall(timestamp.encode('utf-8'))

        client_socket.close()  # Закрываем соединение с клиентом


def check_key_exists(key_path):
    """Проверяет, существует ли файл ключа."""
    return os.path.exists(key_path)


def validate_key_format(key_path):
    """Проверяет, корректен ли формат ключа."""
    try:
        with open(key_path, "r", encoding='utf-8') as f:
            pem_data = f.readlines()

        # Проверяем, начинается ли файл с правильного заголовка
        if not (pem_data[0].startswith("-----BEGIN") and pem_data[-1].startswith("-----END")):
            return False

        # Декодируем содержимое ключа
        key_b64 = ''.join(line.strip() for line in pem_data[1:-1])
        key_bytes = base64.b64decode(key_b64)

        # Проверяем, что ключ имеет достаточную длину
        if len(key_bytes) < 128:  # Примерная минимальная длина для RSA
            return False

        return True
    except Exception as e:
        print(f"Ошибка при проверке формата ключа: {e}")
        return False


def main():
    private_key_path = "C:/Users/User/PycharmProjects/pythonProject8/private_key.pem"
    public_key_path = "C:/Users/User/PycharmProjects/pythonProject8/public_key.pem"

    # Проверка наличия закрытого ключа
    if check_key_exists(private_key_path):
        print(f"Файл закрытого ключа '{private_key_path}' найден.")
        if validate_key_format(private_key_path):
            print("Файл закрытого ключа имеет корректный формат.")
        else:
            print("Файл закрытого ключа имеет некорректный формат.")
    else:
        print(f"Файл закрытого ключа '{private_key_path}' не найден.")

    print()  # Для разделения выводов

    # Проверка наличия открытого ключа
    if check_key_exists(public_key_path):
        print(f"Файл открытого ключа '{public_key_path}' найден.")
        if validate_key_format(public_key_path):
            print("Файл открытого ключа имеет корректный формат.")
        else:
            print("Файл открытого ключа имеет некорректный формат.")
    else:
        print(f"Файл открытого ключа '{public_key_path}' не найден.")


if __name__ == "__main__":
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Запускаем основную функцию
    main()