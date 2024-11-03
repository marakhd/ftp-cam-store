import aioftp


class AsyncFTPServer:
    def __init__(self, host: str, user: str, password: str, folder_structure: str):
        """
        Инициализация параметров подключения к FTP и формата организации папок.
        """
        self.host = host
        self.user = user
        self.password = password
        self.folder_structure = folder_structure
        self.client = aioftp.Client.context()

    async def connect(self):
        """
        Установка асинхронного соединения с FTP-сервером.
        """
        await self.client.connect(self.host)
        await self.client.login(self.user, self.password)
        print(f"Connected to {self.host}")

    async def disconnect(self):
        """
        Завершение асинхронного соединения с FTP-сервером.
        """
        await self.client.quit()
        print(f"Disconnected from {self.host}")

    async def upload_file(self, local_path: str, remote_path: str):
        """
        Асинхронная загрузка файла на FTP-сервер.
        """
        await self.client.upload(local_path, remote_path)
        print(f"Uploaded {local_path} to {remote_path} on {self.host}")

    async def download_file(self, remote_path: str, local_path: str):
        """
        Асинхронное скачивание файла с FTP-сервера.
        """
        await self.client.download(remote_path, local_path)
        print(f"Downloaded {remote_path} to {local_path} from {self.host}")