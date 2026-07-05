import threading
import time


def scenario_1():
    output = []
    output_lock = threading.Lock()

    opening_event = threading.Event()

    def log(message):
        with output_lock:
            output.append(message)

    def employee_task(employee_name):
        log(
            f"{employee_name} arrived and prepared the workstation"
        )

        log(
            f"{employee_name} is waiting for the opening signal"
        )

        opening_event.wait()

        log(
            f"{employee_name} received the opening signal and started serving customers"
        )

    employees = [
        "Cashier-Thread",
        "Barista-Thread",
        "Kitchen-Thread",
    ]

    threads = []

    for employee_name in employees:
        thread = threading.Thread(
            target=employee_task,
            args=(employee_name,),
            name=employee_name
        )

        threads.append(thread)
        thread.start()

    time.sleep(0.3)

    log(
        "Main thread sets the opening_event. All waiting employees can start now."
    )

    opening_event.set()

    for thread in threads:
        thread.join()

    log(
        f"opening_event.is_set() = {opening_event.is_set()}"
    )

    log(
        "Coffee shop opening workflow finished"
    )

    return {
        "method": "thread",
        "section": 8,
        "scenario": 1,
        "title": "One-to-Many Start Signal with Event",
        "problem":
            "شرح مسئله:\n"
            "چند کارمند کافه آماده شروع کار هستند، اما هیچ‌کدام نباید قبل از اعلام رسمی باز شدن کافه شروع به سرویس‌دهی کنند. "
            "همه Threadها باید منتظر یک سیگنال مشترک بمانند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با یک سیگنال واحد چند Thread منتظر را همزمان آزاد کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از threading.Event برای ارسال سیگنال شروع از یک Thread به چند Thread دیگر",
        "output": output,
        "explanation":
            "در این سناریو چند Thread با متد wait روی یک Event مشترک منتظر می‌مانند. "
            "تا زمانی که main thread متد set را روی Event صدا نزند، Threadها ادامه پیدا نمی‌کنند. "
            "بعد از set شدن Event، همه Threadهای منتظر آزاد می‌شوند و اجرای خود را ادامه می‌دهند. "
            "این سناریو کاربرد Event برای ارسال یک start signal مشترک را نشان می‌دهد."
    }


def scenario_2():
    output = []
    output_lock = threading.Lock()

    shutdown_event = threading.Event()
    worker_iterations = {}

    def log(message):
        with output_lock:
            output.append(message)

    def background_worker(worker_name, work_delay):
        iteration = 0

        log(
            f"{worker_name} started background loop"
        )

        while not shutdown_event.is_set():
            iteration += 1

            log(
                f"{worker_name} processed background job #{iteration}"
            )

            time.sleep(work_delay)

        worker_iterations[worker_name] = iteration

        log(
            f"{worker_name} detected shutdown_event and stopped cleanly after {iteration} jobs"
        )

    workers = [
        ("Cache-Cleanup-Thread", 0.15),
        ("Metrics-Collector-Thread", 0.20),
        ("Notification-Worker-Thread", 0.18),
    ]

    threads = []

    for worker_name, work_delay in workers:
        thread = threading.Thread(
            target=background_worker,
            args=(worker_name, work_delay),
            name=worker_name
        )

        threads.append(thread)
        thread.start()

    time.sleep(0.65)

    log(
        "Main thread requests graceful shutdown by setting shutdown_event"
    )

    shutdown_event.set()

    for thread in threads:
        thread.join()

    log(
        f"Final worker iteration counts: {worker_iterations}"
    )

    log(
        "All background workers stopped gracefully"
    )

    return {
        "method": "thread",
        "section": 8,
        "scenario": 2,
        "title": "Graceful Shutdown Signal with Event",
        "problem":
            "شرح مسئله:\n"
            "چند Worker پس‌زمینه در حال انجام کارهای تکراری هستند. برنامه نباید آن‌ها را ناگهانی متوقف کند، "
            "بلکه باید یک سیگنال توقف ارسال شود تا هر Worker بعد از پایان iteration فعلی خودش به شکل تمیز متوقف شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند Thread در حال اجرا را با یک سیگنال مشترک و بدون توقف ناگهانی خاموش کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Event به عنوان shutdown signal و بررسی وضعیت آن با is_set",
        "output": output,
        "explanation":
            "در این سناریو Event برای شروع کار استفاده نمی‌شود، بلکه برای توقف کنترل‌شده استفاده می‌شود. "
            "هر Worker در یک loop کار می‌کند و در ابتدای هر iteration وضعیت shutdown_event را با is_set بررسی می‌کند. "
            "وقتی main thread متد set را صدا می‌زند، همه Workerها متوجه درخواست shutdown می‌شوند، از loop خارج می‌شوند و بعد از ثبت وضعیت نهایی متوقف می‌شوند. "
            "این روش برای graceful shutdown در Threadهای پس‌زمینه کاربرد دارد."
    }


def scenario_3():
    output = []
    output_lock = threading.Lock()

    data_ready_event = threading.Event()

    def log(message):
        with output_lock:
            output.append(message)

    def report_worker(worker_name, timeout):
        log(
            f"{worker_name} is waiting for data_ready_event with timeout={timeout:.2f} seconds"
        )

        event_received = data_ready_event.wait(timeout=timeout)

        if event_received:
            log(
                f"{worker_name} received data_ready_event before timeout and generated the report"
            )
        else:
            log(
                f"{worker_name} timed out and used fallback cached data"
            )

    timeout_thread = threading.Thread(
        target=report_worker,
        args=("Fast-Report-Thread", 0.25),
        name="Fast-Report-Thread"
    )

    waiting_thread = threading.Thread(
        target=report_worker,
        args=("Detailed-Report-Thread", 0.80),
        name="Detailed-Report-Thread"
    )

    timeout_thread.start()
    waiting_thread.start()

    time.sleep(0.40)

    log(
        "Main thread prepared fresh data and sets data_ready_event"
    )

    data_ready_event.set()

    timeout_thread.join()
    waiting_thread.join()

    log(
        f"data_ready_event.is_set() = {data_ready_event.is_set()}"
    )

    log(
        "Report generation workflow finished"
    )

    return {
        "method": "thread",
        "section": 8,
        "scenario": 3,
        "title": "Event Wait with Timeout and Fallback",
        "problem":
            "شرح مسئله:\n"
            "دو Thread برای تولید گزارش به داده تازه نیاز دارند. یکی از گزارش‌ها فقط مدت کوتاهی منتظر می‌ماند و اگر داده آماده نشود "
            "باید از داده cached استفاده کند. گزارش دیگر می‌تواند مدت بیشتری منتظر بماند و در صورت آماده شدن داده تازه از آن استفاده کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان کاری کرد که یک Thread فقط مدت محدودی منتظر Event بماند و در صورت نرسیدن سیگنال مسیر جایگزین اجرا شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از wait(timeout) و بررسی مقدار برگشتی آن برای تصمیم‌گیری بین مسیر اصلی و fallback",
        "output": output,
        "explanation":
            "در این سناریو از wait(timeout) استفاده شده است. این متد اگر Event قبل از پایان timeout فعال شود مقدار True برمی‌گرداند، "
            "اما اگر زمان انتظار تمام شود و Event هنوز set نشده باشد مقدار False برمی‌گرداند. "
            "Fast-Report-Thread فقط ۰.۲۵ ثانیه منتظر می‌ماند و چون Event دیرتر set می‌شود، مسیر fallback را اجرا می‌کند. "
            "Detailed-Report-Thread زمان بیشتری منتظر می‌ماند و بعد از set شدن Event مسیر اصلی تولید گزارش را اجرا می‌کند. "
            "پس این سناریو کاربرد Event برای انتظار محدود و تصمیم‌گیری بر اساس timeout را نشان می‌دهد."
    }