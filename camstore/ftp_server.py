from ftplib import FTP, all_errors

class FTPServer:
    def __init__(self, host: str, user: str, password: str, folder_structure: str):
        """
        Инициализация параметров подключения к FTP и формата организации папок.
        """
        self.host = host
        self.user = user
        self.password = password
        self.folder_structure = folder_structure  # например, 'video-station/<camera>/<year>/<m>/<d>'
        self.connection = None

    def connect(self):
        """
        Установка соединения с FTP-сервером.
        """
        try:
            self.connection = FTP(self.host)
            self.connection.login(self.user, self.password)
            print(f"Connected to {self.host}")
        except all_errors as e:
            print(f"Error connecting to {self.host}: {e}")

    def disconnect(self):
        """
        Завершение соединения с FTP-сервером.
        """
        if self.connection:
            self.connection.quit()
            print(f"Disconnected from {self.host}")

    def upload_file(self, local_path: str, remote_path: str):
        """
        Загрузка файла на FTP-сервер.
        """
        if not self.connection:
            self.connect()
        with open(local_path, 'rb') as file:
            self.connection.storbinary(f'STOR {remote_path}', file)
            print(f"Uploaded {local_path} to {remote_path} on {self.host}")

    def download_file(self, remote_path: str, local_path: str):
        """
        Скачивание файла с FTP-сервера.
        """
        if not self.connection:
            self.connect()
        with open(local_path, 'wb') as file:
            self.connection.retrbinary(f'RETR {remote_path}', file.write)
            print(f"Downloaded {remote_path} to {local_path} from {self.host}")
