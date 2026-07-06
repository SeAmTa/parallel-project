import multiprocessing
import os
import queue
import time
from datetime import datetime

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


def _barrier_managed_worker(
    worker_name,
    arrival_delay,
    synchronizer,
    serializer_lock,
    release_timestamp,
    result_queue
):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(arrival_delay)

    result_queue.put(
        f"{worker_name} reached the barrier after {arrival_delay:.2f} seconds and is now waiting"
    )

    synchronizer.wait()

    with serializer_lock:
        if release_timestamp.value == 0.0:
            release_timestamp.value = time.time()

        timestamp = datetime.fromtimestamp(release_timestamp.value).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        result_queue.put(
            f"process {current_process.name} passed the barrier at {timestamp}"
        )

    result_queue.put(
        f"{worker_name} continues only after all barrier-managed processes have arrived"
    )


def _process_without_barrier(worker_name, arrival_delay, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(arrival_delay)

    timestamp = datetime.fromtimestamp(time.time()).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    result_queue.put(
        f"process {current_process.name} has no barrier and continued immediately at {timestamp}"
    )

    result_queue.put(
        f"{worker_name} finished without waiting for other processes"
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
    synchronizer = multiprocessing.Barrier(2)
    serializer_lock = multiprocessing.Lock()
    release_timestamp = multiprocessing.Value("d", 0.0)

    processes = [
        multiprocessing.Process(
            target=_barrier_managed_worker,
            args=(
                "Barrier-Worker-1",
                0.25,
                synchronizer,
                serializer_lock,
                release_timestamp,
                result_queue,
            ),
            name="p1 - test_with_barrier",
        ),
        multiprocessing.Process(
            target=_barrier_managed_worker,
            args=(
                "Barrier-Worker-2",
                0.60,
                synchronizer,
                serializer_lock,
                release_timestamp,
                result_queue,
            ),
            name="p2 - test_with_barrier",
        ),
        multiprocessing.Process(
            target=_process_without_barrier,
            args=("Free-Worker-1", 0.10, result_queue),
            name="p3 - test_without_barrier",
        ),
        multiprocessing.Process(
            target=_process_without_barrier,
            args=("Free-Worker-2", 0.15, result_queue),
            name="p4 - test_without_barrier",
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created multiprocessing.Barrier with parties=2"
    )
    output.append(
        "Processes p1 and p2 are synchronized by the barrier"
    )
    output.append(
        "Processes p3 and p4 do not use the barrier and can continue independently"
    )

    for process in processes:
        process.start()
        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(result_queue, expected_count=14)
    )

    for process in processes:
        output.append(
            f"Process status: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Barrier-based process synchronization workflow finished"
    )

    return {
        "method": "process",
        "section": 7,
        "scenario": 3,
        "title": "Synchronizing Processes with Barrier",
        "problem": (
            "شرح مسئله:\n"
            "چهار Process اجرا می‌شوند. دو Process باید در یک نقطه مشترک منتظر بمانند "
            "تا هر دو به آن نقطه برسند و سپس همزمان ادامه دهند. دو Process دیگر هیچ Barrier ندارند "
            "و بدون انتظار برای بقیه ادامه می‌دهند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Barrier بخشی از Processها را در یک نقطه همگام کرد "
            "و تفاوت آن‌ها را با Processهای بدون Barrier مشاهده کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Barrier برای phase synchronization بین Processها"
        ),
        "output": output,
        "explanation": (
            "در این سناریو یک multiprocessing.Barrier با مقدار parties=2 ساخته شده است. "
            "این یعنی دو Process باید به barrier.wait برسند تا هر دو آزاد شوند. "
            "Processهای p1 و p2 وارد تابع barrier-managed می‌شوند و بعد از رسیدن به Barrier متوقف می‌مانند. "
            "وقتی هر دو Process به Barrier رسیدند، Barrier آن‌ها را آزاد می‌کند و هر دو وارد مرحله بعدی می‌شوند. "
            "برای اینکه همزمانی آزاد شدن آن‌ها واضح‌تر باشد، زمان آزاد شدن Barrier به صورت یک مقدار مشترک ذخیره می‌شود "
            "و هر دو Process همان timestamp آزادسازی را گزارش می‌کنند. "
            "در مقابل، Processهای p3 و p4 هیچ Barrier ندارند و بعد از delay کوتاه خودشان بلافاصله ادامه می‌دهند. "
            "بنابراین خروجی نشان می‌دهد که Barrier برای تقسیم برنامه به فازهای همگام‌شده استفاده می‌شود، "
            "در حالی که Processهای بدون Barrier مستقل از بقیه ادامه پیدا می‌کنند."
        ),
    }