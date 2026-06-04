import threading
import time
import os
import random


def scenario_1():
    output = []
    lock = threading.Lock()

    def worker(thread_number):
        with lock:
            output.append(
                f"---> Thread#{thread_number} running, belonging to process ID {os.getpid()}"
            )

            time.sleep(0.5)

            output.append(
                f"---> Thread#{thread_number} over"
            )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=worker,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("End")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 1,
        "title": "Thread Synchronization with Lock",
        "output": output,
        "explanation":
            "در این سناریو از Lock استفاده شده است. بنابراین در هر لحظه فقط یک thread می‌تواند وارد بخش بحرانی شود و پیام running و over را پشت سر هم تولید کند."
    }


def scenario_2():
    output = []
    lock = threading.Lock()

    def worker(thread_number):
        output.append(
            f"Thread#{thread_number} is waiting for lock"
        )

        with lock:
            output.append(
                f"Thread#{thread_number} entered critical section"
            )

            time.sleep(
                random.uniform(0.2, 0.8)
            )

            output.append(
                f"Thread#{thread_number} left critical section"
            )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=worker,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 4,
        "scenario": 2,
        "title": "Thread Synchronization with Lock",
        "output": output,
        "explanation":
            "در این سناریو قبل از گرفتن Lock پیام waiting چاپ می‌شود. سپس هر thread به ترتیب وارد بخش بحرانی می‌شود. زمان اجرای بخش بحرانی تصادفی است، اما همزمانی داخل آن رخ نمی‌دهد."
    }


def scenario_3():
    output = []

    def worker(thread_number):
        output.append(
            f"Thread#{thread_number} running without lock"
        )

        time.sleep(
            random.uniform(0.2, 0.8)
        )

        output.append(
            f"Thread#{thread_number} over without lock"
        )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=worker,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 4,
        "scenario": 3,
        "title": "Thread Synchronization with Lock",
        "output": output,
        "explanation":
            "در این سناریو عمداً از Lock استفاده نشده است. بنابراین چند thread می‌توانند همزمان اجرا شوند و ترتیب خروجی‌ها قابل پیش‌بینی نیست."
    }