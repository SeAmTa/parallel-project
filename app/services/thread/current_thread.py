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
    output_lock = threading.Lock()

    def log(message):
        with output_lock:
            output.append(message)

    def nested_worker(parent_thread_name):
        current = threading.current_thread()

        log(f"Nested-Worker is running in thread: {current.name}")
        log(f"Nested-Worker was created by: {parent_thread_name}")

        time.sleep(0.05)

        log(f"Nested-Worker finished in thread: {threading.current_thread().name}")

    def supervisor_worker():
        current = threading.current_thread()
        main = threading.main_thread()

        log(f"Supervisor is running in thread: {current.name}")
        log(f"Python main thread is: {main.name}")
        log(f"Is Supervisor the Python MainThread? {current is main}")

        child = threading.Thread(
            target=nested_worker,
            args=(current.name,),
            name="Nested-Worker"
        )

        log(f"{current.name} is creating Nested-Worker")

        child.start()
        child.join()

        log(f"{current.name} joined Nested-Worker")

    caller_thread = threading.current_thread()

    log(f"Scenario function is currently running in thread: {caller_thread.name}")

    supervisor = threading.Thread(
        target=supervisor_worker,
        name="Supervisor-Thread"
    )

    log("Starting Supervisor-Thread from scenario function")

    supervisor.start()
    supervisor.join()

    log("Supervisor-Thread completed")

    return {
        "method": "thread",
        "section": 2,
        "scenario": 3,
        "title": "Tracking current_thread in Nested Threads",
        "problem": (
            "یک برنامه یک Thread ناظر ایجاد می‌کند و آن Thread ناظر نیز یک Thread داخلی "
            "دیگر می‌سازد. هر بخش از اجرا باید بتواند تشخیص دهد کدام Thread در همان لحظه "
            "در حال اجرای کد است."
        ),
        "output": output,
        "explanation": (
            "در این سناریو از threading.current_thread() در سه سطح مختلف استفاده شده است: "
            "تابع اصلی سناریو، Thread ناظر، و Thread داخلی. در ابتدای سناریو مشخص می‌شود "
            "تابع سناریو در کدام Thread در حال اجراست. سپس Supervisor-Thread ساخته می‌شود "
            "و داخل آن با current_thread() نام Thread ناظر خوانده می‌شود. همچنین با "
            "threading.main_thread() نشان داده می‌شود که Thread ناظر الزاماً همان MainThread "
            "پایتون نیست. در مرحله بعد، Supervisor-Thread یک Nested-Worker می‌سازد و نام خودش "
            "را به عنوان parent_thread_name به آن می‌دهد. Nested-Worker نیز با current_thread() "
            "تشخیص می‌دهد خودش در کدام Thread اجرا می‌شود و همچنین نشان می‌دهد توسط کدام Thread "
            "ساخته شده است. نکته اصلی این است که current_thread() همیشه Threadی را برمی‌گرداند "
            "که همان لحظه خط فعلی کد را اجرا می‌کند، نه الزاماً MainThread."
        )
    }