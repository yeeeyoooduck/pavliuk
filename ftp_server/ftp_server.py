import socket
import os
import shutil
import logging
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096

# Создание логгеров
connection_logger = logging.getLogger('connections')
auth_logger = logging.getLogger('auth')
file_operations_logger = logging.getLogger('file_operations')


def setup_logging():
    logging.basicConfig(filename='server.log', level=logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    connection_handler = logging.FileHandler('connections.log')
    connection_handler.setLevel(logging.INFO)
    connection_handler.setFormatter(formatter)
    connection_logger.addHandler(connection_handler)

    auth_handler = logging.FileHandler('auth.log')
    auth_handler.setLevel(logging.INFO)
    auth_handler.setFormatter(formatter)
    auth_logger.addHandler(auth_handler)

    file_operations_handler = logging.FileHandler('file_operations.log')
    file_operations_handler.setLevel(logging.INFO)
    file_operations_handler.setFormatter(formatter)
    file_operations_logger.addHandler(file_operations_handler)


def list_files(directory):
    return os.listdir(directory)


def create_folder(directory, folder_name):
    folder_path = os.path.join(directory, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    file_operations_logger.info(f"Папка '{folder_name}' создана в '{directory}'")


def delete_folder(folder_path):
    shutil.rmtree(folder_path)
    file_operations_logger.info(f"Папка '{folder_path}' удалена")


def delete_file(file_path):
    os.remove(file_path)
    file_operations_logger.info(f"Файл '{file_path}' удален")


def rename_file(old_name, new_name):
    os.rename(old_name, new_name)
    file_operations_logger.info(f"Файл '{old_name}' переименован в '{new_name}'")


def copy_file(src, dst):
    shutil.copyfile(src, dst)
    file_operations_logger.info(f"Файл '{src}' скопирован в '{dst}'")


def handle_client(client_socket, user_directory):
    current_dir = user_directory

    while True:
        request = client_socket.recv(BUFFER_SIZE).decode()
        if not request:
            break

        command, *args = request.split()

        if command == 'LIST':
            files = list_files(current_dir)
            response = json.dumps(files)
            client_socket.send(response.encode())

        elif command == 'CREATE_FOLDER':
            folder_name = args[0]
            create_folder(current_dir, folder_name)
            client_socket.send(f'Папка успешно создана')

        elif command == 'DELETE_FOLDER':
            folder_name = args[0]
            folder_path = os.path.join(current_dir, folder_name)
            delete_folder(folder_path)
            client_socket.send(f'Папка успешно удалена')

        elif command == 'DELETE_FILE':
            file_name = args[0]
            file_path = os.path.join(current_dir, file_name)
            delete_file(file_path)
            client_socket.send(f'Файл успешно удален')

        elif command == 'RENAME_FILE':
            old_name, new_name = args
            rename_file(os.path.join(current_dir, old_name), os.path.join(current_dir, new_name))
            client_socket.send(f'Файл успешно переименован')

        elif command == 'COPY_TO_SERVER':
            file_name, file_content = args
            with open(os.path.join(current_dir, file_name), 'wf') as f:
                f.write(file_content.encode())
            client_socket.send(f'Файл успешно скопирован на сервер')

        elif command == 'COPY_TO_CLIENT':
            file_name = args[0]
            with open(os.path.join(current_dir, file_name), 'rf') as f:
                file_content = f.read()
            client_socket.sendall(file_content)

        elif command == 'EXIT':
            break

    client_socket.close()


def main():
    setup_logging()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    connection_logger.info(f"[*] Ожидание подключений на {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        connection_logger.info(f"[*] Принято подключение от {client_address[0]}:{client_address[1]}")

        # Подключение пользователя
        # Для простоты, предполагаем, что после установления соединения клиент сразу отправляет свой логин
        user_login = client_socket.recv(BUFFER_SIZE).decode()
        user_directory = os.path.join(os.getcwd(), user_login)
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)
            file_operations_logger.info(f"Пользователь '{user_login}' зарегистрирован. Создана рабочая директория.")
        auth_logger.info(f"Пользователь '{user_login}' подключен с {client_address[0]}:{client_address[1]}")

        handle_client(client_socket, user_directory)


if __name__ == "__main__":
    main()
