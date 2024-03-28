import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 4096


def main():
    # Устанавливаем соединение с сервером
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Отправляем логин пользователя на сервер
    user_login = input("Введите ваш логин: ")
    client_socket.send(user_login.encode())

    # Обработка команд пользователя
    while True:
        print("Доступные команды:")
        print("1. LIST - просмотреть список файлов и папок в текущей директории")
        print("2. CREATE_FOLDER <имя_папки> - создать папку")
        print("3. DELETE_FOLDER <имя_папки> - удалить папку")
        print("4. DELETE_FILE <имя_файла> - удалить файл")
        print("5. RENAME_FILE <старое_имя> <новое_имя> - переименовать файл")
        print("6. COPY_TO_SERVER <имя_файла> <содержимое_файла> - скопировать файл на сервер")
        print("7. COPY_TO_CLIENT <имя_файла> - скопировать файл с сервера")
        print("8. EXIT - выход")

        command = input("Введите команду: ")
        client_socket.send(command.encode())

        if command == 'EXIT':
            break

        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)

    client_socket.close()


if __name__ == "__main__":
    main()
