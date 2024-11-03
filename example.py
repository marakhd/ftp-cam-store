from camstore import FTPManager


if __name__ == "__main__":
    manager = FTPManager()
    # Добавление серверов (пример с фиктивными данными)
    manager.add_server("s2.camerasnp.ru", "sadmin", "Fhntv8900000", "video-station/<address>/<camera>/<year>/<m>/<d>")
    # Скачивание и конвертация видео с определённой камеры
    manager.download_camera_files("CAM10", "2024", "10", "26")