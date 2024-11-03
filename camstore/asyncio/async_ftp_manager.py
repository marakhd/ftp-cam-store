import os
import aioftp
import asyncio
from typing import List, Dict

from .async_ftp_server import AsyncFTPServer


class AsyncFTPManager:
    def __init__(self):
        """
        Инициализация списка асинхронных FTP-серверов.
        """
        self.servers: List[AsyncFTPServer] = []

    def add_server(self, host: str, user: str, password: str, folder_structure: str):
        """
        Добавление нового асинхронного FTP-сервера в список.
        """
        server = AsyncFTPServer(host, user, password, folder_structure)
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
        Вывод списка всех асинхронных FTP-серверов.
        """
        for server in self.servers:
            print(f"Server: {server.host}, Folder structure: {server.folder_structure}")

    async def download_camera_files(self, camera_name: str, year: str, month: str, day: str):
        """
        Асинхронная загрузка файлов камеры с каждого FTP-сервера в зависимости от структуры папок.
        """
        tasks = []
        for server in self.servers:
            tasks.append(self._download_files_from_server(server, camera_name, year, month, day))

        await asyncio.gather(*tasks)

    async def _download_files_from_server(self, server: AsyncFTPServer, camera_name: str, year: str, month: str, day: str):
        """
        Вспомогательный метод для загрузки файлов с одного сервера.
        """
        await server.connect()

        try:
            # Получаем список всех папок на уровне адресов
            address_folders = await server.client.list(server.folder_structure.replace("<camera>", "") \
                                                                .replace("<year>", "") \
                                                                .replace("<m>", "") \
                                                                .replace("<d>", "").strip('/'))

            # Перебираем все папки с адресами
            for address in address_folders:
                adress_path = os.path.join(server.folder_structure, address.name).replace("<camera>", camera_name) \
                                                                                .replace("<year>", year) \
                                                                                .replace("<m>", month) \
                                                                                .replace("<d>", day)

                # Проверяем, доступна ли папка с записями камеры
                try:
                    files = await server.client.list(adress_path)
                    for file in files:
                        filename = file.name
                        if filename.endswith(".dav"):
                            local_file_path = os.path.join("downloads", server.host, camera_name, year, month, day, address.name, filename.replace(".dav", ".mp4"))
                            await server.download_file(os.path.join(adress_path, filename), local_file_path)
                            await self.convert_dav_to_mp4(local_file_path)
                        elif filename.endswith(".mp4"):
                            local_file_path = os.path.join("downloads", server.host, camera_name, year, month, day, address.name, filename)
                            await server.download_file(os.path.join(adress_path, filename), local_file_path)
                except aioftp.Error:
                    print(f"Access denied to {adress_path} on {server.host}")

        except aioftp.Error as e:
            print(f"Error listing folders on {server.host}: {e}")

    @staticmethod
    async def convert_dav_to_mp4(dav_file_path: str):
        """
        Асинхронная конвертация файлов .dav в .mp4 с помощью ffmpeg.
        """
        mp4_file_path = dav_file_path.replace(".dav", ".mp4")
        command = ["ffmpeg", "-i", dav_file_path, mp4_file_path]
        process = await asyncio.create_subprocess_exec(*command)
        await process.wait()
        print(f"Converted {dav_file_path} to {mp4_file_path}")
        os.remove(dav_file_path)  # Удаление оригинального .dav файла после конвертации
