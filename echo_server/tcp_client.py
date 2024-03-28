import socket
import logging

# Настройка логгера
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def client():
    # Создание TCP сокета
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Запрос порта и хоста у пользователя
    host = input("Введите адрес сервера (по умолчанию localhost): ") or 'localhost'
    port = int(input("Введите номер порта (по умолчанию 8888): ") or '8888')

    try:
        # Соединение с сервером
        logging.info(f"[*] Соединение с сервером {host}:{port}")
        client_socket.connect((host, port))

        while True:
            # Считывание строки со стандартного ввода
            message = input("[*] Введите сообщение для отправки серверу ('exit' для завершения): ")
            if message.lower() == 'exit':
                break

            # Отправка данных серверу
            logging.info(f"[*] Отправка данных серверу: {message}")
            client_socket.sendall(message.encode())

            # Прием данных от сервера
            data = client_socket.recv(1024).decode()
            logging.info(f"[*] Прием данных от сервера: {data}")
            print(f"[*] Прием данных от сервера: {data}")

    finally:
        # Закрытие соединения с сервером
        logging.info("[*] Разрыв соединения с сервером...")
        client_socket.close()

if __name__ == '__main__':
    client()
