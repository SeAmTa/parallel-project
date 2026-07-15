import multiprocessing
import os
import queue
import sys
import time


def _collect_queue_messages(result_queue, expected_count):
    messages = []

    for _ in range(expected_count):
        try:
            messages.append(
                result_queue.get(timeout=2)
            )
        except queue.Empty:
            messages.append(
                "Warning: expected message was not received from child process"
            )

    return messages


def _identity_report_worker(task_name, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Task '{task_name}' is running inside process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(0.25)

    result_queue.put(
        f"Task '{task_name}' finished inside process name='{current_process.name}'"
    )


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    default_named_process = multiprocessing.Process(
        target=_identity_report_worker,
        args=("default-name-report", result_queue)
    )

    custom_named_process = multiprocessing.Process(
        target=_identity_report_worker,
        args=("custom-name-report", result_queue),
        name="Custom-Process"
    )

    processes = [
        default_named_process,
        custom_named_process,
    ]

    for process in processes:
        output.append(
            f"Parent created process object with name='{process.name}'"
        )

        process.start()

        output.append(
            f"Parent started process name='{process.name}' with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=4
        )
    )

    for process in processes:
        output.append(
            f"Parent joined process name='{process.name}' with exit code {process.exitcode}"
        )

    return {
        "method": "process",
        "section": 2,
        "scenario": 1,
        "title": "Default and Custom Process Names",
        "problem":
            "شرح مسئله:\n"
            "وقتی چند Process ساخته می‌شود، تشخیص اینکه هر خروجی مربوط به کدام Process است اهمیت دارد. "
            "یک Process می‌تواند نام پیش‌فرض داشته باشد و یک Process دیگر می‌تواند با نام سفارشی ساخته شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان نام یک Process را مشخص کرد و همان نام را داخل Process فرزند با current_process خواند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از name در multiprocessing.Process و خواندن نام Process با multiprocessing.current_process",
        "output": output,
        "explanation":
            "در این سناریو دو Process ساخته می‌شود. یکی بدون name ساخته شده و Python برای آن یک نام پیش‌فرض مثل Process-1 تعیین می‌کند. "
            "Process دوم با name سفارشی ساخته شده است. داخل تابع worker، با multiprocessing.current_process نام Process جاری خوانده می‌شود. "
            "این سناریو پایه‌ای‌ترین کاربرد naming را نشان می‌دهد: نام Process برای لاگ‌گیری، شناسایی و خوانایی خروجی‌ها استفاده می‌شود."
    }


def _role_based_worker(result_queue):
    current_process = multiprocessing.current_process()
    process_name = current_process.name

    result_queue.put(
        f"{process_name} started with PID={os.getpid()}"
    )

    time.sleep(0.20)

    if "Compressor" in process_name:
        files = ["image.png", "menu.pdf", "report.csv"]

        result_queue.put(
            f"{process_name} compressed {len(files)} files"
        )

    elif "Validator" in process_name:
        records = ["order-1", "order-2", "order-3", "order-4"]

        result_queue.put(
            f"{process_name} validated {len(records)} records"
        )

    elif "Notifier" in process_name:
        notifications = ["email", "sms"]

        result_queue.put(
            f"{process_name} sent {len(notifications)} notifications"
        )

    else:
        result_queue.put(
            f"{process_name} has no matching role"
        )


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()

    process_names = [
        "Compressor-Process",
        "Validator-Process",
        "Notifier-Process",
    ]

    processes = []

    for process_name in process_names:
        process = multiprocessing.Process(
            target=_role_based_worker,
            args=(result_queue,),
            name=process_name
        )

        processes.append(process)

        output.append(
            f"Parent created role-based process name='{process.name}'"
        )

        process.start()

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=len(processes) * 2
        )
    )

    for process in processes:
        output.append(
            f"Parent joined {process.name} with exit code {process.exitcode}"
        )

    output.append(
        "Role-based process workflow finished"
    )

    return {
        "method": "process",
        "section": 2,
        "scenario": 2,
        "title": "Role-Based Behavior Using Process Names",
        "problem":
            "شرح مسئله:\n"
            "چند Process از یک تابع worker مشترک استفاده می‌کنند، اما هرکدام باید نقش متفاوتی انجام دهند؛ "
            "یکی فشرده‌سازی فایل، یکی اعتبارسنجی داده و یکی ارسال اعلان.\n\n"
            "سؤال:\n"
            "آیا می‌توان از نام Process برای تشخیص نقش آن و اجرای رفتار متفاوت داخل همان worker مشترک استفاده کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از current_process().name برای اجرای branchهای متفاوت داخل یک target function مشترک",
        "output": output,
        "explanation":
            "در این سناریو همه Processها یک target function مشترک دارند، اما نام هر Process متفاوت است. "
            "داخل worker، نام Process جاری با multiprocessing.current_process().name خوانده می‌شود و بر اساس آن رفتار متفاوت اجرا می‌شود. "
            "مثلاً Compressor-Process عملیات فشرده‌سازی، Validator-Process اعتبارسنجی و Notifier-Process ارسال اعلان را انجام می‌دهد. "
            "این سناریو با سناریوی اول فرق دارد، چون نام Process فقط برای لاگ نیست؛ بلکه در تصمیم‌گیری اجرایی هم استفاده می‌شود."
    }


def _named_health_check_worker(result_queue, should_fail):
    current_process = multiprocessing.current_process()
    process_name = current_process.name

    result_queue.put(
        f"{process_name} started health check with PID={os.getpid()}"
    )

    time.sleep(0.25)

    if should_fail:
        result_queue.put(
            f"{process_name} detected a critical error and exits with code 2"
        )

        sys.exit(2)

    result_queue.put(
        f"{process_name} completed health check successfully"
    )

    
def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()

    process_specs = [
        ("Payment-Health-Process", False),
        ("Cache-Health-Process", False),
        ("Search-Health-Process", True),
    ]

    processes = []

    for process_name, should_fail in process_specs:
        process = multiprocessing.Process(
            target=_named_health_check_worker,
            args=(result_queue, should_fail),
            name=process_name
        )

        processes.append(process)

        output.append(
            f"Parent started monitoring target process name='{process.name}'"
        )

        process.start()

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=len(processes) * 2
        )
    )

    failed_processes = []

    for process in processes:
        output.append(
            f"Monitor result: process name='{process.name}', PID={process.pid}, exitcode={process.exitcode}"
        )

        if process.exitcode != 0:
            failed_processes.append(process.name)

    output.append(
        f"Failed processes identified by name: {failed_processes}"
    )

    output.append(
        "Named process monitoring workflow finished"
    )

    return {
        "method": "process",
        "section": 2,
        "scenario": 3,
        "title": "Monitoring Process Exit Codes by Name",
        "problem":
            "شرح مسئله:\n"
            "چند Process برای بررسی سلامت سرویس‌ها اجرا می‌شوند. یکی از آن‌ها با خطا تمام می‌شود. "
            "Parent باید بعد از پایان همه Processها تشخیص دهد کدام Process مشکل داشته است.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با استفاده از نام Process و exitcode، Process خطادار را در خروجی مانیتورینگ مشخص کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از process.name همراه با process.exitcode برای debug و monitoring چند Process",
        "output": output,
        "explanation":
            "در این سناریو هر Process یک نام مشخص دارد و parent بعد از join کردن Processها exitcode آن‌ها را بررسی می‌کند. "
            "دو Process با exitcode برابر 0 تمام می‌شوند، اما Search-Health-Process با sys.exit(2) خاتمه پیدا می‌کند. "
            "چون هر Process نام مشخص دارد، parent می‌تواند دقیقاً گزارش دهد کدام Process شکست خورده است. "
            "این سناریو با دو سناریوی قبلی فرق دارد، چون naming اینجا برای monitoring و خطایابی بعد از پایان Processها استفاده می‌شود."
    }