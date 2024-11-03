import asyncio

from camstore.asyncio import AsyncFTPManager


async def main():
    manager = AsyncFTPManager()
    
    # Добавление одного сервера с использованием объекта
    server_info = {
        'host': 's1.example.com',
        'user': 'user1',
        'password': 'pass1',
        'folder_structure': 'video-station/<camera>/<year>/<m>/<d>'
    }
    await manager.add_server_from_object(server_info)
    
    # Добавление нескольких серверов с использованием списка объектов
    servers_info = [
        {
            'host': 's2.example.com',
            'user': 'user2',
            'password': 'pass2',
            'folder_structure': 'video-station/<adress>/<camera>/<year>/<m>/<d>'
        },
        {
            'host': 's3.example.com',
            'user': 'user3',
            'password': 'pass3',
            'folder_structure': 'video-station/<camera>/<year>/<m>/<d>'
        },
        {
            'host': 's4.example.com',
            'user': 'user4',
            'password': 'pass4',
            'folder_structure': 'video-station/<camera>/<year>/<m>/<d>'
        }
    ]
    await manager.add_server(servers_info)

    # Список добавленных серверов
    manager.list_servers()

    # Асинхронная загрузка и конвертация видео с определённой камеры
    await manager.download_camera_files("CAM10", "2024", "10", "26")

# Запуск асинхронного основного цикла
if __name__ == "__main__":
    asyncio.run(main())