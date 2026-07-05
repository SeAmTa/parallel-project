import multiprocessing
import os
import queue
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


def _long_running_report_worker(result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Long report process started with name='{current_process.name}', PID={os.getpid()}"
    )

    for step in range(1, 3):
        time.sleep(0.15)

        result_queue.put(
            f"Long report process completed warm-up step {step}/2"
        )

    result_queue.put(
        "Long report process entered a long-running loop and will not finish soon"
    )

    while True:
        time.sleep(0.25)


def _graceful_stop_worker(stop_event, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Graceful worker started with name='{current_process.name}', PID={os.getpid()}"
    )

    for cycle in range(1, 3):
        time.sleep(0.15)

        result_queue.put(
            f"Graceful worker completed work cycle {cycle}/2"
        )

    result_queue.put(
        "Graceful worker is now waiting for parent stop event"
    )

    while not stop_event.is_set():
        time.sleep(0.05)

    result_queue.put(
        "Graceful worker observed stop event and starts cleanup"
    )

    time.sleep(0.10)

    result_queue.put(
        "Graceful worker cleanup completed and exits normally"
    )


def _quick_service_worker(service_name, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{service_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(0.25)

    result_queue.put(
        f"{service_name} completed its normal workload"
    )

    result_queue.put(
        f"{service_name} finished normally"
    )


def _stuck_service_worker(service_name, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{service_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(0.15)

    result_queue.put(
        f"{service_name} became unresponsive and entered an endless loop"
    )

    while True:
        time.sleep(0.25)


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_long_running_report_worker,
        args=(result_queue,),
        name="Long-Running-Report-Process"
    )

    output.append(
        f"Parent process PID={os.getpid()} created process name='{process.name}'"
    )

    process.start()

    output.append(
        f"Parent started process name='{process.name}' with PID={process.pid}"
    )

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=4
        )
    )

    output.append(
        "Parent waits with join(timeout=0.3) instead of waiting forever"
    )

    process.join(timeout=0.3)

    output.append(
        f"Process alive after timeout: {process.is_alive()}"
    )

    if process.is_alive():
        output.append(
            "Parent terminates the process because it exceeded the allowed time"
        )

        process.terminate()
        process.join()

    output.append(
        f"Process exit code after terminate: {process.exitcode}"
    )

    output.append(
        "Timeout-based termination workflow finished"
    )

    return {
        "method": "process",
        "section": 4,
        "scenario": 1,
        "title": "Terminating a Long-Running Process After Timeout",
        "problem":
            "شرح مسئله:\n"
            "یک گزارش طولانی در Process جداگانه اجرا شده است، اما بیشتر از زمان مجاز طول می‌کشد. "
            "Process اصلی نباید برای همیشه منتظر بماند و باید بعد از timeout آن را متوقف کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با join(timeout) تشخیص داد یک Process هنوز زنده است و سپس آن را terminate کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از join(timeout)، is_alive و terminate برای متوقف کردن Process طولانی",
        "output": output,
        "explanation":
            "در این سناریو parent یک Process طولانی را start می‌کند. سپس با join(timeout=0.3) فقط مدت محدودی منتظر می‌ماند. "
            "چون Process هنوز زنده است، parent با is_alive آن را تشخیص می‌دهد و با terminate متوقفش می‌کند. "
            "exitcode صفر نیست، چون Process به شکل طبیعی تمام نشده و توسط parent متوقف شده است. "
            "این روش برای کارهایی مناسب است که اگر بیش از حد طول کشیدند باید اجباری متوقف شوند."
    }


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()
    stop_event = multiprocessing.Event()

    process = multiprocessing.Process(
        target=_graceful_stop_worker,
        args=(stop_event, result_queue),
        name="Graceful-Stoppable-Process"
    )

    output.append(
        f"Parent process PID={os.getpid()} created process name='{process.name}'"
    )

    process.start()

    output.append(
        f"Parent started process name='{process.name}' with PID={process.pid}"
    )

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=4
        )
    )

    output.append(
        "Parent sends cooperative stop signal with multiprocessing.Event"
    )

    stop_event.set()

    process.join(timeout=2)

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=2
        )
    )

    output.append(
        f"Process alive after graceful stop: {process.is_alive()}"
    )

    output.append(
        f"Process exit code after graceful stop: {process.exitcode}"
    )

    output.append(
        "Graceful stop workflow finished without terminate"
    )

    return {
        "method": "process",
        "section": 4,
        "scenario": 2,
        "title": "Gracefully Stopping a Process with Event",
        "problem":
            "شرح مسئله:\n"
            "یک worker در Process جداگانه کار می‌کند، اما بهتر است به جای terminate اجباری، با یک سیگنال نرم متوقف شود "
            "تا فرصت cleanup داشته باشد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان به جای کشتن اجباری Process، با multiprocessing.Event از آن خواست خودش تمیز خارج شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "توقف cooperative با Event و تفاوت آن با terminate اجباری",
        "output": output,
        "explanation":
            "در این سناریو parent از terminate استفاده نمی‌کند. به جای آن یک multiprocessing.Event مشترک به worker داده می‌شود. "
            "Worker بعد از انجام چند cycle منتظر stop_event می‌ماند. وقتی parent متد set را صدا می‌زند، worker سیگنال را می‌بیند، cleanup انجام می‌دهد و به شکل طبیعی خارج می‌شود. "
            "به همین دلیل exitcode برابر ۰ است. این سناریو با سناریوی اول فرق دارد، چون توقف از نوع cooperative و امن‌تر است."
    }


def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()

    processes = [
        multiprocessing.Process(
            target=_quick_service_worker,
            args=("Analytics-Service", result_queue),
            name="Analytics-Service-Process"
        ),
        multiprocessing.Process(
            target=_stuck_service_worker,
            args=("Billing-Service", result_queue),
            name="Billing-Service-Process"
        ),
        multiprocessing.Process(
            target=_quick_service_worker,
            args=("Email-Service", result_queue),
            name="Email-Service-Process"
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} starts three service processes"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    time.sleep(0.45)

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=8
        )
    )

    billing_process = None

    for process in processes:
        if process.name == "Billing-Service-Process":
            billing_process = process
            break

    if billing_process is not None and billing_process.is_alive():
        output.append(
            "Parent detected Billing-Service-Process is still alive and appears stuck"
        )

        output.append(
            "Parent terminates only Billing-Service-Process and keeps other processes untouched"
        )

        billing_process.terminate()

    for process in processes:
        process.join()

    for process in processes:
        output.append(
            f"Final process status: name='{process.name}', PID={process.pid}, exitcode={process.exitcode}"
        )

    output.append(
        "Selective process termination workflow finished"
    )

    return {
        "method": "process",
        "section": 4,
        "scenario": 3,
        "title": "Selective Termination of One Stuck Process",
        "problem":
            "شرح مسئله:\n"
            "سه سرویس در سه Process جداگانه اجرا شده‌اند. دو سرویس به شکل عادی تمام می‌شوند، اما یکی از سرویس‌ها گیر می‌کند. "
            "Parent باید فقط همان Process مشکل‌دار را terminate کند و اجازه دهد بقیه Processها عادی تمام شوند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان در میان چند Process فقط Process گیرکرده را شناسایی و terminate کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "مدیریت چند Process، انتخاب Process مشکل‌دار، terminate انتخابی و بررسی exitcode هر Process",
        "output": output,
        "explanation":
            "در این سناریو سه Process همزمان اجرا می‌شوند. Analytics-Service و Email-Service کار خود را تمام می‌کنند، اما Billing-Service وارد حلقه بی‌پایان می‌شود. "
            "Parent ابتدا لاگ‌های Processها را جمع‌آوری می‌کند، سپس بررسی می‌کند کدام Process هنوز زنده مانده است. "
            "چون Billing-Service-Process هنوز زنده است، parent فقط همان Process را terminate می‌کند و بقیه Processها را دست‌نخورده می‌گذارد. "
            "در انتها exitcode هر Process گزارش می‌شود. Processهایی که عادی تمام شده‌اند exitcode صفر دارند، اما Process terminate شده exitcode غیرصفر دارد. "
            "این سناریو با سناریوهای قبلی فرق دارد، چون هدف کشتن همه Processها نیست؛ هدف terminate انتخابی یک Process مشکل‌دار در بین چند Process است."
    }