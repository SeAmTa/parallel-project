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


def _single_invoice_worker(result_queue):
    process_id = os.getpid()

    result_queue.put(
        f"Child process started with PID={process_id}"
    )

    time.sleep(0.30)

    invoice_total = 120 + 80 + 50

    result_queue.put(
        f"Invoice calculated inside child process. Total={invoice_total}"
    )

    result_queue.put(
        f"Child process PID={process_id} finished invoice calculation"
    )


def _image_resize_worker(image_name, resize_time, result_queue):
    process_id = os.getpid()

    result_queue.put(
        f"{image_name} resize started in process PID={process_id}"
    )

    time.sleep(resize_time)

    result_queue.put(
        f"{image_name} resize finished in process PID={process_id}"
    )


def _memory_isolation_worker(shared_number, result_queue):
    process_id = os.getpid()

    result_queue.put(
        f"Child process PID={process_id} received shared_number={shared_number}"
    )

    shared_number += 100

    result_queue.put(
        f"Child process changed its own copy to shared_number={shared_number}"
    )

    time.sleep(0.20)

    result_queue.put(
        "Child process finished, but this change does not affect the parent process memory"
    )


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_single_invoice_worker,
        args=(result_queue,),
        name="Invoice-Calculation-Process"
    )

    output.append(
        f"Parent process PID={os.getpid()} is creating one child process"
    )

    process.start()

    output.append(
        f"Parent started child process with PID={process.pid}"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=3
        )
    )

    output.append(
        f"Child process exit code: {process.exitcode}"
    )

    output.append(
        "Parent process continued after join because the child process finished"
    )

    return {
        "method": "process",
        "section": 1,
        "scenario": 1,
        "title": "Spawning One Child Process and Waiting with Join",
        "problem":
            "شرح مسئله:\n"
            "یک برنامه باید محاسبه یک فاکتور را در یک Process جداگانه انجام دهد تا کار از Process اصلی جدا شود. "
            "Process اصلی باید Process فرزند را ایجاد کند، آن را اجرا کند و تا پایان کار آن منتظر بماند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان یک Process جدید ساخت، آن را اجرا کرد و با join منتظر پایان اجرای آن ماند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ساخت یک Process ساده با multiprocessing.Process، اجرای start و انتظار با join",
        "output": output,
        "explanation":
            "در این سناریو Process اصلی یک Process فرزند ایجاد می‌کند. تابع محاسبه فاکتور داخل Process فرزند اجرا می‌شود، نه داخل Process اصلی. "
            "بعد از start، سیستم‌عامل یک Process جداگانه با PID مستقل می‌سازد. سپس parent با join منتظر می‌ماند تا child تمام شود. "
            "در پایان exitcode برابر ۰ نشان می‌دهد Process فرزند بدون خطا تمام شده است."
    }


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()

    images = [
        ("menu-banner.jpg", 0.45),
        ("product-photo.png", 0.20),
        ("landing-hero.webp", 0.35),
    ]

    processes = []

    output.append(
        f"Parent process PID={os.getpid()} is spawning multiple image resize processes"
    )

    for image_name, resize_time in images:
        process = multiprocessing.Process(
            target=_image_resize_worker,
            args=(image_name, resize_time, result_queue),
            name=f"Resize-Process-{image_name}"
        )

        processes.append(process)
        process.start()

        output.append(
            f"Started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=len(images) * 2
        )
    )

    for process in processes:
        output.append(
            f"{process.name} joined with exit code {process.exitcode}"
        )
        
    output.append(
        "All image resize processes finished"
    )

    return {
        "method": "process",
        "section": 1,
        "scenario": 2,
        "title": "Spawning Multiple Independent Processes",
        "problem":
            "شرح مسئله:\n"
            "یک سیستم باید چند تصویر را resize کند. هر تصویر مستقل از بقیه است، بنابراین می‌توان برای هر تصویر یک Process جداگانه ساخت "
            "تا کارها به صورت جداگانه و همزمان اجرا شوند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند Process مستقل ایجاد کرد، همه را start کرد و بعد منتظر پایان همه آن‌ها ماند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ساخت چند Process مستقل و مدیریت start/join برای همه آن‌ها",
        "output": output,
        "explanation":
            "در این سناریو parent برای هر تصویر یک Process جداگانه می‌سازد. همه Processها ابتدا start می‌شوند و سپس parent با join منتظر پایان همه آن‌ها می‌ماند. "
            "برخلاف سناریوی اول که فقط یک Process ساخته می‌شد، اینجا چند Process مستقل اجرا می‌شوند. "
            "ترتیب تمام شدن کارها می‌تواند با ترتیب start شدن متفاوت باشد، چون هر Process زمان اجرای متفاوتی دارد."
    }


def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()

    shared_number = 10

    output.append(
        f"Parent process PID={os.getpid()} initial shared_number={shared_number}"
    )

    process = multiprocessing.Process(
        target=_memory_isolation_worker,
        args=(shared_number, result_queue),
        name="Memory-Isolation-Process"
    )

    process.start()

    output.append(
        f"Parent started child process with PID={process.pid}"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=3
        )
    )

    output.append(
        f"Parent process still has shared_number={shared_number}"
    )

    output.append(
        "Parent value did not change because processes do not share normal memory"
    )

    output.append(
        f"Child process exit code: {process.exitcode}"
    )

    return {
        "method": "process",
        "section": 1,
        "scenario": 3,
        "title": "Process Memory Isolation After Spawning",
        "problem":
            "شرح مسئله:\n"
            "یک مقدار عددی از Process اصلی به Process فرزند ارسال می‌شود. Process فرزند مقدار را تغییر می‌دهد، "
            "اما باید بررسی شود آیا این تغییر روی مقدار داخل Process اصلی هم اثر می‌گذارد یا نه.\n\n"
            "سؤال:\n"
            "آیا Process فرزند بعد از spawn شدن می‌تواند متغیر معمولی Process اصلی را مستقیماً تغییر دهد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "جدایی حافظه در Processها و تفاوت آن با Threadها",
        "output": output,
        "explanation":
            "در این سناریو یک عدد از parent به child ارسال می‌شود. Process فرزند مقدار خودش را تغییر می‌دهد، اما این تغییر روی مقدار parent اثر نمی‌گذارد. "
            "دلیلش این است که Processها حافظه مستقل دارند و مثل Threadها حافظه معمولی را به صورت مستقیم share نمی‌کنند. "
            "برای انتقال داده بین Processها باید از ابزارهایی مثل Queue، Pipe، Value، Array یا Manager استفاده شود."
    }