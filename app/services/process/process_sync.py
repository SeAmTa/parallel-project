import multiprocessing
import os
import queue
import time
from datetime import datetime


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
        "5 render worker processes will compete for only two license slots"
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
        f"{worker_name} completed its production stage after {arrival_delay:.2f} seconds and reached the vehicle assembly barrier"
    )

    synchronizer.wait()

    with serializer_lock:
        if release_timestamp.value == 0.0:
            release_timestamp.value = time.time()

        timestamp = datetime.fromtimestamp(
            release_timestamp.value
        ).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        result_queue.put(
            f"{worker_name} passed the assembly barrier at {timestamp}"
        )

    result_queue.put(
        f"{worker_name} can now enter final vehicle assembly because both the car body and engine are ready"
    )


def _process_without_barrier(
    worker_name,
    arrival_delay,
    result_queue
):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{worker_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    time.sleep(arrival_delay)

    timestamp = datetime.fromtimestamp(
        time.time()
    ).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )

    result_queue.put(
        f"{worker_name} does not depend on vehicle assembly and continued independently at {timestamp}"
    )

    result_queue.put(
        f"{worker_name} finished without waiting for the car body or engine"
    )


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
                "Car Body Production",
                0.25,
                synchronizer,
                serializer_lock,
                release_timestamp,
                result_queue,
            ),
            name="p1 - Car-Body-Production",
        ),
        multiprocessing.Process(
            target=_barrier_managed_worker,
            args=(
                "Engine Production",
                0.60,
                synchronizer,
                serializer_lock,
                release_timestamp,
                result_queue,
            ),
            name="p2 - Engine-Production",
        ),
        multiprocessing.Process(
            target=_process_without_barrier,
            args=(
                "Production Report Generation",
                0.10,
                result_queue
            ),
            name="p3 - Production-Report",
        ),
        multiprocessing.Process(
            target=_process_without_barrier,
            args=(
                "Factory Data Backup",
                0.15,
                result_queue
            ),
            name="p4 - Factory-Data-Backup",
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created multiprocessing.Barrier with parties=2"
    )

    output.append(
        "Car Body Production and Engine Production must both finish before final vehicle assembly can begin"
    )

    output.append(
        "Production Report Generation and Factory Data Backup do not depend on vehicle assembly and can continue independently"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=14
        )
    )

    for process in processes:
        output.append(
            f"Process status: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Vehicle factory barrier synchronization workflow finished"
    )

    return {
        "method": "process",
        "section": 7,
        "scenario": 3,
        "title": "Coordinating Vehicle Assembly Processes with Barrier",
        "problem": (
            "شرح مسئله:\n"
            "در یک کارخانه خودروسازی، یک Process وظیفه تولید بدنه خودرو "
            "و Process دیگر وظیفه تولید موتور را بر عهده دارد. مرحله مونتاژ "
            "نهایی فقط زمانی می‌تواند آغاز شود که هر دو قطعه آماده باشند. "
            "بنابراین، هر کدام که زودتر کارش تمام شود باید در یک نقطه مشترک "
            "منتظر Process دیگر بماند.\n\n"
            "در همین زمان، دو Process دیگر وظیفه تهیه گزارش تولید و "
            "پشتیبان‌گیری از اطلاعات کارخانه را انجام می‌دهند. این فعالیت‌ها "
            "هیچ وابستگی‌ای به آماده‌شدن بدنه و موتور ندارند و باید بدون "
            "انتظار ادامه پیدا کنند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Barrier تولید بدنه و موتور را "
            "پیش از ورود به مرحله مونتاژ هماهنگ کرد، در حالی که Processهای "
            "مستقل بدون Barrier به فعالیت خود ادامه دهند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Barrier برای هماهنگ‌کردن Processهای وابسته در پایان "
            "یک مرحله، بدون متوقف‌کردن Processهای مستقل"
        ),
        "output": output,
        "explanation": (
            "در این سناریو یک multiprocessing.Barrier با parties=2 ساخته "
            "شده است، زیرا فقط دو Process تولید بدنه و تولید موتور باید "
            "با یکدیگر هماهنگ شوند. Process تولید بدنه پس از ۰٫۲۵ ثانیه "
            "آماده می‌شود و به Barrier می‌رسد، اما چون موتور هنوز آماده "
            "نشده است، در همان نقطه منتظر می‌ماند. Process تولید موتور پس "
            "از ۰٫۶۰ ثانیه به Barrier می‌رسد. با رسیدن Process دوم، Barrier "
            "آزاد می‌شود و هر دو Process می‌توانند وارد مرحله مونتاژ نهایی "
            "خودرو شوند. زمان آزادشدن Barrier در release_timestamp مشترک "
            "ذخیره می‌شود، بنابراین هر دو Process یک timestamp یکسان برای "
            "عبور از Barrier گزارش می‌کنند. serializer_lock نیز ثبت این "
            "زمان و پیام‌های مربوط به عبور را کنترل می‌کند. در مقابل، "
            "Process تهیه گزارش تولید و Process پشتیبان‌گیری عضو Barrier "
            "نیستند؛ زیرا فعالیت آن‌ها به آماده‌شدن بدنه و موتور وابسته "
            "نیست. به همین دلیل، پس از پایان delay خود بدون انتظار برای "
            "سایر Processها به فعالیتشان ادامه می‌دهند."
        ),
    }