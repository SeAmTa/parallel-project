import threading
import time


def scenario_1():
    output = []

    def download_file(file_name):
        current_thread = threading.current_thread()

        output.append(
            f"{file_name} started by {current_thread.name}"
        )

        time.sleep(0.5)

        output.append(
            f"{file_name} completed by {current_thread.name}"
        )

    threads = [
        threading.Thread(
            target=download_file,
            name="Download-Thread-1",
            args=("image.png",)
        ),
        threading.Thread(
            target=download_file,
            name="Download-Thread-2",
            args=("video.mp4",)
        ),
        threading.Thread(
            target=download_file,
            name="Download-Thread-3",
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
        "scenario": 1,
        "title": "Download Manager with Current Thread Detection",
        "output": output,
        "explanation":
            "در این سناریو چند فایل به صورت همزمان دانلود می‌شوند. داخل تابع download_file با threading.current_thread مشخص می‌کنیم همان لحظه کدام Thread در حال اجرای تابع است."
    }


def scenario_2():
    output = []

    def background_download(file_name):
        current_thread = threading.current_thread()

        output.append(
            f"{current_thread.name} started downloading {file_name}"
        )

        time.sleep(1)

        output.append(
            f"{current_thread.name} finished downloading {file_name}"
        )

    threads = [
        threading.Thread(
            target=background_download,
            name="Monitor-Download-Image",
            args=("image.png",)
        ),
        threading.Thread(
            target=background_download,
            name="Monitor-Download-Video",
            args=("video.mp4",)
        ),
        threading.Thread(
            target=background_download,
            name="Monitor-Download-Document",
            args=("document.pdf",)
        ),
    ]

    for thread in threads:
        thread.start()

    time.sleep(0.2)

    output.append("Active threads detected by monitoring dashboard:")

    active_threads = threading.enumerate()

    for active_thread in active_threads:
        output.append(
            f"- {active_thread.name}"
        )

    for thread in threads:
        thread.join()

    output.append("Monitoring dashboard finished checking active threads")

    return {
        "method": "thread",
        "section": 2,
        "scenario": 2,
        "title": "Thread Monitoring Dashboard with enumerate",
        "output": output,
        "explanation":
            "در این سناریو چند Thread در حال دانلود فایل هستند و همزمان با threading.enumerate لیست Threadهای فعال گرفته می‌شود. این سناریو نشان می‌دهد چطور می‌توان برای مانیتورینگ یا دیباگ، Threadهای فعال برنامه را مشاهده کرد."
    }


def scenario_3():
    output = []

    main_thread = threading.current_thread()

    output.append(
        f"Program started in {main_thread.name}"
    )

    def worker_task(task_name):
        current_thread = threading.current_thread()

        output.append(
            f"{task_name} started in {current_thread.name}"
        )

        time.sleep(0.4)

        output.append(
            f"{task_name} completed in {current_thread.name}"
        )

    threads = [
        threading.Thread(
            target=worker_task,
            name="Worker-Backup-Thread",
            args=("Database Backup",)
        ),
        threading.Thread(
            target=worker_task,
            name="Worker-Email-Thread",
            args=("Email Notification",)
        ),
        threading.Thread(
            target=worker_task,
            name="Worker-Report-Thread",
            args=("Report Generation",)
        ),
    ]

    output.append(
        "MainThread is responsible for creating and starting worker threads"
    )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"All workers finished. Control returned to {main_thread.name}"
    )

    return {
        "method": "thread",
        "section": 2,
        "scenario": 3,
        "title": "Main Thread and Worker Thread Detection",
        "output": output,
        "explanation":
            "در این سناریو ابتدا Thread اصلی برنامه با threading.current_thread تشخیص داده می‌شود. سپس چند Worker Thread ساخته و اجرا می‌شوند. خروجی نشان می‌دهد MainThread وظیفه ایجاد و مدیریت Workerها را دارد و Workerها وظایف جداگانه را انجام می‌دهند."
    }