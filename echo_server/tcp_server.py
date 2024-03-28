import socket
import logging

# Настройка логгера
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def server():
    # Создание TCP сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Запрос порта и хоста у пользователя
    host = input("Введите адрес сервера (по умолчанию localhost): ") or 'localhost'
    port = int(input("Введите номер порта (по умолчанию 8888): ") or '8888')

    # Привязка сокета к указанному адресу и порту
    while True:
        try:
            server_socket.bind((host, port))
            logging.info(f"[*] Запуск сервера на {host}:{port}")
            print(f"[*] Запуск сервера на {host}:{port}")
            break
        except OSError:
            print(f"[*] Порт {port} уже занят. Попробуйте другой порт.")
            port = int(input("Введите номер порта: "))

    # Начало прослушивания порта
    server_socket.listen(5)
    logging.info("[*] Начало прослушивания порта...")

    while True:
        # Ожидание подключения клиента
        print("[*] Ожидание подключения клиента...")
        connection, client_address = server_socket.accept()
        logging.info(f"[*] Подключение клиента: {client_address}")

        try:
            while True:
                data = connection.recv(1024).decode()
                if not data:
                    logging.info(f"[*] Отключение клиента: {client_address}")
                    print(f"[*] Отключение клиента: {client_address}")
                    break

                logging.info(f"[*] Прием данных от клиента {client_address}: {data}")
                print(f"[*] Прием данных от клиента {client_address}: {data}")

                # Отправка данных клиенту
                logging.info(f"[*] Отправка данных клиенту {client_address}: {data}")
                connection.sendall(data.encode())
        finally:
            # Закрытие соединения
            connection.close()

if __name__ == '__main__':
    server()
