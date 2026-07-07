import multiprocessing
import os
import queue
import time


def _collect_queue_messages(result_queue, expected_count, timeout=1):
    messages = []

    for _ in range(expected_count):
        try:
            messages.append(
                result_queue.get(timeout=timeout)
            )
        except queue.Empty:
            messages.append(
                "Warning: expected message was not received from child process before timeout"
            )
            break

    return messages


def _background_logger_worker(result_queue, heartbeat_count):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Background logger started in process name='{current_process.name}', PID={os.getpid()}, daemon={current_process.daemon}"
    )

    for heartbeat_number in range(1, heartbeat_count + 1):
        time.sleep(0.15)

        result_queue.put(
            f"Background logger heartbeat {heartbeat_number}"
        )

    result_queue.put(
        "Background logger finished controlled heartbeat demo and entered idle background mode"
    )

    while True:
        time.sleep(1)


def _foreground_report_worker(result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Foreground report process started with name='{current_process.name}', PID={os.getpid()}, daemon={current_process.daemon}"
    )

    for step in range(1, 4):
        time.sleep(0.20)

        result_queue.put(
            f"Foreground report process completed step {step}/3"
        )

    result_queue.put(
        "Foreground report process finished all required work"
    )


def _nested_child_worker(local_queue):
    current_process = multiprocessing.current_process()

    local_queue.put(
        f"Nested child process executed with name='{current_process.name}', PID={os.getpid()}, daemon={current_process.daemon}"
    )


def _supervisor_worker(result_queue):
    current_process = multiprocessing.current_process()
    supervisor_name = current_process.name

    result_queue.put(
        f"{supervisor_name} started with PID={os.getpid()}, daemon={current_process.daemon}"
    )

    try:
        local_queue = multiprocessing.Queue()

        nested_process = multiprocessing.Process(
            target=_nested_child_worker,
            args=(local_queue,),
            name=f"Nested-Child-Of-{supervisor_name}"
        )

        nested_process.start()

        result_queue.put(
            f"{supervisor_name} started nested child process with PID={nested_process.pid}"
        )

        try:
            nested_message = local_queue.get(timeout=2)
        except queue.Empty:
            nested_message = "Warning: nested child message was not received"

        result_queue.put(
            nested_message
        )

        nested_process.join()

        result_queue.put(
            f"{supervisor_name} joined nested child with exit code {nested_process.exitcode}"
        )

    except Exception as error:
        result_queue.put(
            f"{supervisor_name} could not start a nested child process: {type(error).__name__}: {error}"
        )


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    background_process = multiprocessing.Process(
        target=_background_logger_worker,
        args=(result_queue, 3),
        name="Daemon-Background-Logger"
    )

    background_process.daemon = True

    output.append(
        f"Parent process PID={os.getpid()} created background process name='{background_process.name}'"
    )

    output.append(
        f"Daemon flag before start: {background_process.daemon}"
    )

    background_process.start()

    output.append(
        f"Parent started daemon process with PID={background_process.pid}"
    )

    output.append(
        "Parent continues immediately and does not wait for the endless background process to finish"
    )

    try:
        output.extend(
            _collect_queue_messages(
                result_queue,
                expected_count=5,
                timeout=1
            )
        )

        output.append(
            f"Parent checked daemon process is_alive={background_process.is_alive()}"
        )

    finally:
        if background_process.is_alive():
            output.append(
                "Parent terminates daemon process for API cleanup"
            )

            background_process.terminate()
            background_process.join(timeout=1)

        if background_process.is_alive():
            output.append(
                "Daemon process did not stop after terminate, parent kills it"
            )

            background_process.kill()
            background_process.join(timeout=1)

        result_queue.close()
        result_queue.cancel_join_thread()

    output.append(
        f"Daemon process exit code after cleanup: {background_process.exitcode}"
    )

    return {
        "method": "process",
        "section": 3,
        "scenario": 1,
        "title": "Daemon Background Process with Controlled Cleanup",
        "problem":
            "شرح مسئله:\n"
            "یک سیستم نیاز دارد یک logger در پس‌زمینه اجرا شود و چند heartbeat تولید کند. "
            "Process اصلی نباید منتظر پایان طبیعی این کار بماند، چون چنین workerهایی معمولاً طولانی‌مدت اجرا می‌شوند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان یک Process را به صورت daemon/background اجرا کرد و در پایان سناریو آن را به شکل کنترل‌شده پاک‌سازی کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از daemon=True برای اجرای background process و انجام cleanup کنترل‌شده در محیط API",
        "output": output,
        "explanation":
            "در این سناریو Process فرزند با daemon=True ساخته می‌شود. Worker چند heartbeat کنترل‌شده تولید می‌کند و سپس وارد حالت background idle می‌شود. "
            "Parent بعد از start منتظر پایان طبیعی worker نمی‌ماند و فقط تعداد مشخصی پیام از Queue دریافت می‌کند. "
            "چون داخل API نباید Process اضافی زنده باقی بماند، parent در پایان سناریو ابتدا terminate و در صورت نیاز kill را اجرا می‌کند. "
            "این نسخه برای اجرای داخل Docker و FastAPI امن‌تر است، چون هیچ join بدون timeout و هیچ انتظار بی‌نهایت ندارد."
    }


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()

    foreground_process = multiprocessing.Process(
        target=_foreground_report_worker,
        args=(result_queue,),
        name="NonDaemon-Foreground-Report"
    )

    output.append(
        f"Parent process PID={os.getpid()} created foreground process name='{foreground_process.name}'"
    )

    output.append(
        f"Daemon flag before start: {foreground_process.daemon}"
    )

    foreground_process.start()

    output.append(
        f"Parent started non-daemon process with PID={foreground_process.pid}"
    )

    output.append(
        "Parent calls join because this process has a finite required result"
    )

    foreground_process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=5
        )
    )

    output.append(
        f"Non-daemon process exit code: {foreground_process.exitcode}"
    )

    output.append(
        "Parent continued only after the foreground report process finished"
    )

    return {
        "method": "process",
        "section": 3,
        "scenario": 2,
        "title": "Non-Daemon Process Waiting with Join",
        "problem":
            "شرح مسئله:\n"
            "یک گزارش مالی باید حتماً کامل تولید شود و parent فقط بعد از پایان کامل آن اجازه ادامه دارد. "
            "این کار نباید مثل یک daemon بی‌پایان در پس‌زمینه رها شود.\n\n"
            "سؤال:\n"
            "تفاوت یک Process معمولی non-daemon با یک daemon process در مدیریت پایان کار چیست؟\n\n"
            "مفهوم مورد بررسی:\n"
            "اجرای non-daemon process و استفاده از join برای انتظار تا پایان قطعی کار",
        "output": output,
        "explanation":
            "در این سناریو Process به صورت پیش‌فرض non-daemon است، یعنی daemon flag آن False است. "
            "این worker کار محدودی دارد و باید خروجی نهایی آن کامل شود. به همین دلیل parent بعد از start کردن Process، join را صدا می‌زند و تا پایان آن منتظر می‌ماند. "
            "این سناریو با سناریوی اول فرق دارد، چون اینجا هدف اجرای پس‌زمینه بی‌پایان نیست؛ هدف انجام یک کار محدود و انتظار برای نتیجه قطعی است."
    }


def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()

    supervisors = [
        ("NonDaemon-Supervisor", False),
        ("Daemon-Supervisor", True),
    ]

    for supervisor_name, daemon_flag in supervisors:
        supervisor_process = multiprocessing.Process(
            target=_supervisor_worker,
            args=(result_queue,),
            name=supervisor_name
        )

        supervisor_process.daemon = daemon_flag

        output.append(
            f"Parent created supervisor name='{supervisor_process.name}', daemon={supervisor_process.daemon}"
        )

        supervisor_process.start()

        output.append(
            f"Parent started supervisor name='{supervisor_process.name}' with PID={supervisor_process.pid}"
        )

        supervisor_process.join()

        expected_messages = 4

        if daemon_flag:
            expected_messages = 2

        output.extend(
            _collect_queue_messages(
                result_queue,
                expected_count=expected_messages
            )
        )

        output.append(
            f"Parent joined supervisor name='{supervisor_process.name}' with exit code {supervisor_process.exitcode}"
        )

    output.append(
        "Daemon child creation restriction demonstration finished"
    )

    return {
        "method": "process",
        "section": 3,
        "scenario": 3,
        "title": "Daemon Process Cannot Create Child Processes",
        "problem":
            "شرح مسئله:\n"
            "یک supervisor process قرار است یک child process دیگر بسازد. باید بررسی شود آیا این کار برای Process معمولی و daemon process یکسان است یا نه.\n\n"
            "سؤال:\n"
            "آیا یک daemon process می‌تواند خودش child process جدید ایجاد کند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محدودیت daemon processها در multiprocessing؛ daemon process اجازه ساخت process فرزند ندارد",
        "output": output,
        "explanation":
            "در این سناریو ابتدا یک NonDaemon-Supervisor اجرا می‌شود و می‌تواند یک nested child process بسازد. "
            "بعد یک Daemon-Supervisor اجرا می‌شود و همان کار را امتحان می‌کند. در multiprocessing، daemon process اجازه ندارد child process جدید ایجاد کند؛ "
            "بنابراین هنگام start کردن nested child خطا رخ می‌دهد. این سناریو با دو سناریوی قبلی فرق دارد، چون به جای اجرای background یا join ساده، یکی از محدودیت‌های مهم daemon processها را نشان می‌دهد."
    }