import threading
import time


def scenario_1():
    output = []

    def download_file(file_name):
        current_thread = threading.current_thread()

        output.append(
            f"{file_name} started by {current_thread.name}"
        )

        time.sleep(0.4)

        output.append(
            f"{file_name} completed by {current_thread.name}"
        )

    threads = [
        threading.Thread(
            target=download_file,
            name="Download-Thread-Image",
            args=("image.png",)
        ),
        threading.Thread(
            target=download_file,
            name="Download-Thread-Video",
            args=("video.mp4",)
        ),
        threading.Thread(
            target=download_file,
            name="Download-Thread-Document",
            args=("document.pdf",)
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    output.append("All download threads completed")

    return {
        "method": "thread",
        "section": 2,
        "scenario": 1,
        "title": "Download Manager with Current Thread Detection",
        "problem":
            "شرح مسئله:\n"
            "یک برنامه مدیریت دانلود باید چند فایل را به صورت همزمان دریافت کند. "
            "برای بررسی لاگ‌ها لازم است مشخص شود هر فایل توسط کدام Thread پردازش شده است.\n\n"
            "سؤال:\n"
            "چگونه می‌توان داخل یک تابع فهمید همان لحظه کدام Thread در حال اجرای آن تابع است؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از threading.current_thread برای تشخیص Thread اجراکننده",
        "output": output,
        "explanation":
            "در این سناریو یک تابع مشترک به نام download_file توسط چند Thread مختلف اجرا می‌شود. "
            "داخل تابع با threading.current_thread مشخص می‌کنیم همان لحظه کدام Thread در حال اجرای آن تابع است. "
            "به همین دلیل در خروجی می‌توان دید هر فایل توسط چه Threadی شروع و کامل شده است."
    }


def scenario_2():
    output = []

    def handle_support_ticket(ticket_id, customer_type):
        current_thread = threading.current_thread()

        output.append(
            f"{current_thread.name} picked ticket {ticket_id} for a {customer_type} customer"
        )

        time.sleep(0.3)

        if "Senior" in current_thread.name:
            output.append(
                f"{current_thread.name} resolved high-priority ticket {ticket_id}"
            )
        else:
            output.append(
                f"{current_thread.name} resolved normal ticket {ticket_id}"
            )

    threads = [
        threading.Thread(
            target=handle_support_ticket,
            name="Senior-Support-Agent-Thread",
            args=("TCK-1001", "premium")
        ),
        threading.Thread(
            target=handle_support_ticket,
            name="Support-Agent-Thread-1",
            args=("TCK-1002", "regular")
        ),
        threading.Thread(
            target=handle_support_ticket,
            name="Support-Agent-Thread-2",
            args=("TCK-1003", "regular")
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Support ticket processing finished")

    return {
        "method": "thread",
        "section": 2,
        "scenario": 2,
        "title": "Support Center Routing Based on Current Thread Name",
        "problem":
            "شرح مسئله:\n"
            "در یک مرکز پشتیبانی، چند Thread نقش اپراتورهای پشتیبانی را دارند. "
            "یک اپراتور ارشد و چند اپراتور معمولی به صورت همزمان تیکت‌ها را بررسی می‌کنند. "
            "تابع پردازش تیکت برای همه آن‌ها مشترک است، اما باید بداند توسط کدام Thread اجرا شده است.\n\n"
            "سؤال:\n"
            "آیا می‌توان داخل یک تابع مشترک، بر اساس نام Thread فعلی رفتار متفاوتی انجام داد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از current_thread برای شناسایی Thread و تصمیم‌گیری بر اساس نام آن",
        "output": output,
        "explanation":
            "در این سناریو همه Threadها یک تابع مشترک را اجرا می‌کنند، اما داخل تابع با threading.current_thread نام Thread فعلی خوانده می‌شود. "
            "اگر نام Thread شامل Senior باشد، خروجی نشان می‌دهد تیکت با اولویت بالاتر توسط اپراتور ارشد رسیدگی شده است. "
            "این سناریو نشان می‌دهد current_thread فقط برای لاگ گرفتن نیست و می‌تواند برای تشخیص هویت Thread اجراکننده هم استفاده شود."
    }


def scenario_3():
    output = []

    controller_thread = threading.current_thread()

    output.append(
        f"Request handler is running in {controller_thread.name}"
    )

    def worker_task(task_name):
        current_thread = threading.current_thread()

        output.append(
            f"{task_name} started in {current_thread.name}"
        )

        time.sleep(0.3)

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
        f"{controller_thread.name} is creating worker threads"
    )

    for thread in threads:
        output.append(
            f"{controller_thread.name} started {thread.name}"
        )
        thread.start()

    for thread in threads:
        thread.join()
        output.append(
            f"{controller_thread.name} detected that {thread.name} has finished"
        )

    output.append(
        f"All workers finished. Control returned to {controller_thread.name}"
    )

    return {
        "method": "thread",
        "section": 2,
        "scenario": 3,
        "title": "Request Handler Thread and Worker Thread Detection",
        "problem":
            "شرح مسئله:\n"
            "در یک برنامه FastAPI، درخواست کاربر ابتدا توسط Thread اجراکننده endpoint پردازش می‌شود. "
            "سپس همان بخش چند Worker Thread برای انجام وظایف پس‌زمینه مانند پشتیبان‌گیری، ارسال ایمیل و تولید گزارش می‌سازد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان تشخیص داد خود endpoint در کدام Thread اجرا شده و هر وظیفه پس‌زمینه توسط کدام Worker Thread انجام شده است؟\n\n"
            "مفهوم مورد بررسی:\n"
            "تشخیص Thread فعلی در محیط FastAPI و Worker Threadها با threading.current_thread",
        "output": output,
        "explanation":
            "در این سناریو ابتدا با threading.current_thread مشخص می‌شود خود endpoint در چه Threadی اجرا شده است. "
            "در محیط FastAPI، چون endpoint به صورت def معمولی نوشته شده، ممکن است این Thread با نام AnyIO worker thread دیده شود. "
            "سپس چند Worker Thread ساخته می‌شوند و داخل هر Worker دوباره current_thread فراخوانی می‌شود. "
            "بنابراین خروجی هم Thread اجراکننده درخواست و هم Worker Threadهای ساخته‌شده را نشان می‌دهد."
    }