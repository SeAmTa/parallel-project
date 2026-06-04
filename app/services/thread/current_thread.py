import threading
import time


def scenario_1():
    output = []

    def download_file(file_name):
        current_thread = threading.current_thread()

        output.append(
            f"{file_name} download started by {current_thread.name}"
        )

        time.sleep(0.5)

        output.append(
            f"{file_name} download completed by {current_thread.name}"
        )

    threads = [
        threading.Thread(target=download_file, args=("image.png",)),
        threading.Thread(target=download_file, args=("video.mp4",)),
        threading.Thread(target=download_file, args=("document.pdf",)),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 1,
        "title": "Multi-file Download System",
        "output": output,
        "explanation":
            "در این سناریو یک برنامه دانلود، سه فایل را همزمان دانلود می‌کند. با استفاده از threading.current_thread مشخص می‌شود هر فایل توسط کدام thread پردازش شده است."
    }


def scenario_2():
    output = []

    def download_file(file_name):
        current_thread = threading.current_thread()

        output.append(
            f"{current_thread.name} started downloading {file_name}"
        )

        time.sleep(0.5)

        output.append(
            f"{current_thread.name} finished downloading {file_name}"
        )

    threads = [
        threading.Thread(
            target=download_file,
            name="Image-Downloader",
            args=("image.png",)
        ),
        threading.Thread(
            target=download_file,
            name="Video-Downloader",
            args=("video.mp4",)
        ),
        threading.Thread(
            target=download_file,
            name="Document-Downloader",
            args=("document.pdf",)
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 2,
        "title": "Named Downloader Threads",
        "output": output,
        "explanation":
            "در این سناریو برای هر دانلودر یک نام مشخص انتخاب شده است. این کار باعث می‌شود لاگ‌های برنامه خواناتر شوند و مشخص باشد هر فایل توسط کدام thread دانلود شده است."
    }


def scenario_3():
    output = []

    def download_file(file_name, file_size, download_time):
        current_thread = threading.current_thread()

        output.append(
            f"{current_thread.name} started {file_name} ({file_size} MB)"
        )

        time.sleep(download_time)

        output.append(
            f"{current_thread.name} completed {file_name} after {download_time} seconds"
        )

    threads = [
        threading.Thread(
            target=download_file,
            name="Small-File-Thread",
            args=("icon.png", 2, 0.2)
        ),
        threading.Thread(
            target=download_file,
            name="Medium-File-Thread",
            args=("report.pdf", 25, 0.6)
        ),
        threading.Thread(
            target=download_file,
            name="Large-File-Thread",
            args=("movie.mp4", 700, 1)
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 3,
        "title": "Download System with Different File Sizes",
        "output": output,
        "explanation":
            "در این سناریو فایل‌ها اندازه‌های متفاوتی دارند و زمان دانلود آن‌ها متفاوت است. خروجی نشان می‌دهد هر thread چه فایلی را شروع و چه زمانی تمام کرده است."
    }