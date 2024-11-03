import os
from ftplib import error_perm
import subprocess
from typing import List, Dict

from .ftp_server import FTPServer

class FTPManager:
    def __init__(self):
        """
        Инициализация списка FTP-серверов.
        """
        self.servers: List[FTPServer] = []

    def add_server(self, host: str, user: str, password: str, folder_structure: str):
        """
        Добавление нового FTP-сервера в список.
        """
        server = FTPServer(host, user, password, folder_structure)
        self.servers.append(server)
        print(f"Added server {host}")

    def remove_server(self, host: str):
        """
        Удаление FTP-сервера из списка по имени хоста.
        """
        self.servers = [server for server in self.servers if server.host != host]
        print(f"Removed server {host}")

    def list_servers(self):
        """
        Вывод списка всех FTP-серверов.
        """
        for server in self.servers:
            print(f"Server: {server.host}, Folder structure: {server.folder_structure}")

    def download_camera_files(self, camera_name: str, year: str, month: str, day: str):
        """
        Синхронная загрузка файлов камеры с каждого FTP-сервера в зависимости от структуры папок.
        """
        for server in self.servers:
            self._download_files_from_server(server, camera_name, year, month, day)

    def _download_files_from_server(self, server: FTPServer, camera_name: str, year: str, month: str, day: str):
        """
        Вспомогательный метод для загрузки файлов с одного сервера (синхронная версия).
        """
        server.connect()

        local_folder = os.path.join("downloads", server.host, camera_name, year, month, day)
        os.makedirs(local_folder, exist_ok=True)

        try:
            # Получаем список всех адресов на сервере
            address_folders = server.client.list("video-station")
            
            # Перебираем все адреса
            for address_folder in address_folders:
                if address_folder.name:  # Папка должна соответствовать формату адреса
                    remote_path = os.path.join("video-station", address_folder.name, camera_name, year, month, day)
                    files = server.client.list(remote_path)
                    
                    for file in files:
                        filename = file.name
                        if filename.endswith(".dav"):
                            local_file_path = os.path.join(local_folder, filename.replace(".dav", ".mp4"))
                            server.download_file(os.path.join(remote_path, filename), local_file_path)
                            self.convert_dav_to_mp4(local_file_path)
                        elif filename.endswith(".mp4"):
                            local_file_path = os.path.join(local_folder, filename)
                            server.download_file(os.path.join(remote_path, filename), local_file_path)

        except error_perm as e:
            print(f"Error accessing path on {server.host}: {e}")


    @staticmethod
    def convert_dav_to_mp4(dav_file_path: str):
        """
        Конвертация файлов .dav в .mp4 с помощью ffmpeg.
        """
        mp4_file_path = dav_file_path.replace(".dav", ".mp4")
        command = ["ffmpeg", "-i", dav_file_path, mp4_file_path]
        try:
            subprocess.run(command, check=True)
            print(f"Converted {dav_file_path} to {mp4_file_path}")
            os.remove(dav_file_path)  # Удаление оригинального .dav файла после конвертации
        except subprocess.CalledProcessError as e:
            print(f"Error converting {dav_file_path} to MP4: {e}")