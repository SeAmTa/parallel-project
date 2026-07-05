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


def _put_ordered_message(result_queue, log_sequence, log_lock, message):
    with log_lock:
        log_sequence.value += 1
        sequence_number = log_sequence.value

    result_queue.put(
        (sequence_number, message)
    )


def _collect_ordered_queue_messages(result_queue, expected_count):
    ordered_messages = []

    for index in range(expected_count):
        try:
            item = result_queue.get(timeout=2)

            if isinstance(item, tuple) and len(item) == 2:
                ordered_messages.append(item)
            else:
                ordered_messages.append(
                    (10_000 + index, item)
                )

        except queue.Empty:
            ordered_messages.append(
                (
                    10_000 + index,
                    "Warning: expected message was not received from child process"
                )
            )

    ordered_messages.sort(
        key=lambda item: item[0]
    )

    return [
        message
        for _, message in ordered_messages
    ]


def _safe_deposit_worker(
        worker_name,
        shared_balance,
        balance_lock,
        log_sequence,
        log_lock,
        result_queue
):
    current_process = multiprocessing.current_process()

    _put_ordered_message(
        result_queue,
        log_sequence,
        log_lock,
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    for deposit_number in range(1, 4):
        time.sleep(0.08)

        with balance_lock:
            old_balance = shared_balance.value
            new_balance = old_balance + 100
            shared_balance.value = new_balance

            _put_ordered_message(
                result_queue,
                log_sequence,
                log_lock,
                f"{worker_name} deposit {deposit_number}/3 changed balance {old_balance} -> {new_balance}"
            )

    _put_ordered_message(
        result_queue,
        log_sequence,
        log_lock,
        f"{worker_name} finished all locked deposits"
    )


def _limited_resource_worker(
        worker_name,
        resource_semaphore,
        active_counter,
        max_active_counter,
        counter_lock,
        log_sequence,
        log_lock,
        result_queue
):
    current_process = multiprocessing.current_process()

    _put_ordered_message(
        result_queue,
        log_sequence,
        log_lock,
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    _put_ordered_message(
        result_queue,
        log_sequence,
        log_lock,
        f"{worker_name} is waiting for a limited license slot"
    )

    with resource_semaphore:
        with counter_lock:
            active_counter.value += 1

            if active_counter.value > max_active_counter.value:
                max_active_counter.value = active_counter.value

            current_active = active_counter.value
            current_max = max_active_counter.value

            _put_ordered_message(
                result_queue,
                log_sequence,
                log_lock,
                f"{worker_name} entered limited resource. active_processes={current_active}, max_active_so_far={current_max}"
            )

        time.sleep(0.25)

        with counter_lock:
            active_counter.value -= 1
            remaining_active = active_counter.value

            _put_ordered_message(
                result_queue,
                log_sequence,
                log_lock,
                f"{worker_name} left limited resource. active_processes={remaining_active}"
            )

    _put_ordered_message(
        result_queue,
        log_sequence,
        log_lock,
        f"{worker_name} finished semaphore-controlled work"
    )


def _event_waiting_worker(worker_name, start_event, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    result_queue.put(
        f"{worker_name} is waiting for parent start_event"
    )

    start_event.wait()

    result_queue.put(
        f"{worker_name} received start_event and begins synchronized work"
    )

    time.sleep(0.15)

    result_queue.put(
        f"{worker_name} finished synchronized work after event signal"
    )


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    shared_balance = multiprocessing.Value("i", 0)
    balance_lock = multiprocessing.Lock()
    log_sequence = multiprocessing.Value("i", 0)
    log_lock = multiprocessing.Lock()

    processes = [
        multiprocessing.Process(
            target=_safe_deposit_worker,
            args=(
                "Cashier-A",
                shared_balance,
                balance_lock,
                log_sequence,
                log_lock,
                result_queue
            ),
            name="Cashier-A-Process"
        ),
        multiprocessing.Process(
            target=_safe_deposit_worker,
            args=(
                "Cashier-B",
                shared_balance,
                balance_lock,
                log_sequence,
                log_lock,
                result_queue
            ),
            name="Cashier-B-Process"
        ),
        multiprocessing.Process(
            target=_safe_deposit_worker,
            args=(
                "Cashier-C",
                shared_balance,
                balance_lock,
                log_sequence,
                log_lock,
                result_queue
            ),
            name="Cashier-C-Process"
        ),
    ]

    expected_balance = len(processes) * 3 * 100

    output.append(
        f"Parent process PID={os.getpid()} created shared_balance using multiprocessing.Value"
    )

    output.append(
        f"Initial shared_balance={shared_balance.value}, expected final balance={expected_balance}"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_ordered_queue_messages(
            result_queue,
            expected_count=15
        )
    )

    output.append(
        f"Final shared_balance in parent process={shared_balance.value}"
    )

    output.append(
        f"Expected final balance={expected_balance}"
    )

    for process in processes:
        output.append(
            f"Process status: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Locked shared Value synchronization workflow finished"
    )

    return {
        "method": "process",
        "section": 7,
        "scenario": 1,
        "title": "Synchronizing Shared Value with Process Lock",
        "problem":
            "شرح مسئله:\n"
            "چند Process همزمان باید موجودی یک حساب مشترک را افزایش دهند. اگر همزمان به مقدار مشترک دسترسی داشته باشند، "
            "باید بخش حساس کد کنترل شود تا مقدار نهایی قابل اعتماد باشد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Lock از یک multiprocessing.Value مشترک بین Processها محافظت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Lock برای محافظت از critical section هنگام تغییر shared memory بین Processها",
        "output": output,
        "explanation":
            "در این سناریو مقدار shared_balance با multiprocessing.Value ساخته شده است، بنابراین برخلاف متغیر معمولی، بین Processها قابل اشتراک‌گذاری است. "
            "هر Process چند بار مقدار balance را افزایش می‌دهد. عملیات خواندن مقدار قبلی، محاسبه مقدار جدید و نوشتن مقدار جدید داخل with balance_lock قرار گرفته است. "
            "برای اینکه ترتیب لاگ‌ها هم مطابق ترتیب واقعی ورود به بخش حساس نمایش داده شود، هر پیام child process با یک شماره ترتیب مشترک ثبت و سپس مرتب نمایش داده می‌شود. "
            "به همین دلیل در هر لحظه فقط یک Process وارد critical section می‌شود و مقدار نهایی با مقدار مورد انتظار برابر می‌ماند."
    }


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()

    resource_semaphore = multiprocessing.Semaphore(2)
    active_counter = multiprocessing.Value("i", 0)
    max_active_counter = multiprocessing.Value("i", 0)
    counter_lock = multiprocessing.Lock()
    log_sequence = multiprocessing.Value("i", 0)
    log_lock = multiprocessing.Lock()

    processes = [
        multiprocessing.Process(
            target=_limited_resource_worker,
            args=(
                f"Render-Worker-{worker_number}",
                resource_semaphore,
                active_counter,
                max_active_counter,
                counter_lock,
                log_sequence,
                log_lock,
                result_queue
            ),
            name=f"Render-Worker-{worker_number}-Process"
        )
        for worker_number in range(1, 6)
    ]

    output.append(
        f"Parent process PID={os.getpid()} created Semaphore with capacity=2"
    )

    output.append(
        "Five render worker processes will compete for only two license slots"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_ordered_queue_messages(
            result_queue,
            expected_count=25
        )
    )

    output.append(
        f"Maximum simultaneous processes inside limited resource={max_active_counter.value}"
    )

    for process in processes:
        output.append(
            f"Process status: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Semaphore process synchronization workflow finished"
    )

    return {
        "method": "process",
        "section": 7,
        "scenario": 2,
        "title": "Limiting Concurrent Processes with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "یک نرم‌افزار render فقط دو license همزمان دارد، اما پنج Process می‌خواهند وارد بخش render شوند. "
            "باید تضمین شود که بیشتر از دو Process همزمان از resource محدود استفاده نکنند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Semaphore تعداد Processهای همزمان داخل یک resource محدود را کنترل کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Semaphore برای capacity control بین چند Process",
        "output": output,
        "explanation":
            "در این سناریو Semaphore با ظرفیت ۲ ساخته شده است. پنج Process اجرا می‌شوند، اما فقط دو Process می‌توانند همزمان وارد بخش محدود شوند. "
            "هر Process قبل از ورود به resource باید semaphore را acquire کند و بعد از خروج آن را release کند. استفاده از with resource_semaphore همین کار را انجام می‌دهد. "
            "برای نمایش نتیجه، active_counter و max_active_counter با Value ذخیره شده‌اند. همچنین لاگ‌های مربوط به ورود و خروج از resource با یک شماره ترتیب مشترک ثبت می‌شوند تا خروجی خواناتر و قابل دفاع‌تر باشد. "
            "مقدار max_active_counter نشان می‌دهد حداکثر تعداد Processهای همزمان داخل resource از ۲ بیشتر نشده است."
    }


def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()
    start_event = multiprocessing.Event()

    processes = [
        multiprocessing.Process(
            target=_event_waiting_worker,
            args=(f"Startup-Worker-{worker_number}", start_event, result_queue),
            name=f"Startup-Worker-{worker_number}-Process"
        )
        for worker_number in range(1, 4)
    ]

    output.append(
        f"Parent process PID={os.getpid()} created multiprocessing.Event"
    )

    output.append(
        "Workers will start and then block until parent sets the event"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=6
        )
    )

    output.append(
        "Parent finished configuration loading and now sets start_event"
    )

    start_event.set()

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=6
        )
    )

    for process in processes:
        output.append(
            f"Process status: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Event-based process synchronization workflow finished"
    )

    return {
        "method": "process",
        "section": 7,
        "scenario": 3,
        "title": "Coordinating Process Start with Event",
        "problem":
            "شرح مسئله:\n"
            "چند Process worker زودتر start می‌شوند، اما نباید کار اصلی را شروع کنند تا parent تنظیمات اولیه سیستم را آماده کند. "
            "بعد از آماده شدن parent، همه workerها باید آزاد شوند و کار را شروع کنند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Event چند Process را منتظر نگه داشت و سپس همزمان آزاد کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Event برای one-to-many signaling بین parent process و چند child process",
        "output": output,
        "explanation":
            "در این سناریو چند Process start می‌شوند اما داخل worker روی start_event.wait متوقف می‌مانند. "
            "تا وقتی parent متد set را صدا نزده، هیچ worker وارد کار اصلی نمی‌شود. بعد از اینکه parent تنظیمات را آماده می‌کند، start_event.set اجرا می‌شود و همه Processهای منتظر آزاد می‌شوند. "
            "این سناریو با Lock و Semaphore فرق دارد، چون هدف محافظت از shared value یا محدود کردن ظرفیت نیست؛ هدف ارسال یک سیگنال شروع از parent به چند child process است."
    }