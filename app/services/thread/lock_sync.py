import threading
import time
import os
import random


def scenario_1():
    output = []
    lock = threading.Lock()

    def technician_access(technician_number):
        with lock:
            output.append(
                f"Technician #{technician_number} entered the server room"
            )

            time.sleep(0.5)

            output.append(
                f"Technician #{technician_number} left the server room"
            )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=technician_access,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Server room access log completed")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 1,
        "title": "Server Room Access Control with Lock",
        "output": output,
        "explanation":
            "در این سناریو چند تکنسین می‌خواهند وارد اتاق سرور شوند. چون اتاق سرور حساس است، با Lock فقط یک تکنسین در هر لحظه اجازه ورود دارد."
    }


def scenario_2():
    output = []
    lock = threading.Lock()

    def technician_access(technician_number):
        output.append(
            f"Technician #{technician_number} requested access to the server room"
        )

        with lock:
            output.append(
                f"Technician #{technician_number} access approved"
            )

            time.sleep(
                random.uniform(0.2, 0.8)
            )

            output.append(
                f"Technician #{technician_number} completed maintenance and exited"
            )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=technician_access,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("All access requests were processed safely")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 2,
        "title": "Server Room Access Queue with Lock",
        "output": output,
        "explanation":
            "در این سناریو همه تکنسین‌ها ابتدا درخواست ورود ثبت می‌کنند. سپس Lock باعث می‌شود درخواست‌ها یکی‌یکی وارد بخش حساس شوند و دسترسی همزمان اتفاق نیفتد."
    }


def scenario_3():
    output = []

    def technician_access(technician_number):
        output.append(
            f"WARNING: Technician #{technician_number} entered without access lock"
        )

        time.sleep(
            random.uniform(0.2, 0.8)
        )

        output.append(
            f"Technician #{technician_number} left without controlled access"
        )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=technician_access,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Unsafe access simulation completed")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 3,
        "title": "Server Room Access Without Lock",
        "output": output,
        "explanation":
            "در این سناریو عمداً Lock حذف شده است. بنابراین چند تکنسین می‌توانند همزمان وارد اتاق سرور شوند و ترتیب خروجی‌ها قابل پیش‌بینی نیست. این حالت نشان می‌دهد چرا برای منابع حساس به Lock نیاز داریم."
    }