import threading
import time


def scenario_1():
    output = []

    def function_a():
        output.append("function_A --> starting")
        time.sleep(1)
        output.append("function_A --> exiting")

    def function_b():
        output.append("function_B --> starting")
        time.sleep(1)
        output.append("function_B --> exiting")

    def function_c():
        output.append("function_C --> starting")
        time.sleep(1)
        output.append("function_C --> exiting")

    threads = [
        threading.Thread(target=function_a),
        threading.Thread(target=function_b),
        threading.Thread(target=function_c),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 1,
        "title": "Determining the Current Thread",
        "output": output,
        "explanation":
            "در این سناریو سه تابع در سه thread جداگانه اجرا می‌شوند. ابتدا هر تابع پیام starting را چاپ می‌کند، سپس بعد از sleep پیام exiting را تولید می‌کند."
    }


def scenario_2():
    output = []

    def worker(function_name):
        current_thread = threading.current_thread()

        output.append(
            f"{function_name} is running in {current_thread.name}"
        )

        time.sleep(0.5)

        output.append(
            f"{function_name} finished in {current_thread.name}"
        )

    threads = [
        threading.Thread(
            target=worker,
            name="Thread-A",
            args=("function_A",)
        ),
        threading.Thread(
            target=worker,
            name="Thread-B",
            args=("function_B",)
        ),
        threading.Thread(
            target=worker,
            name="Thread-C",
            args=("function_C",)
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 2,
        "title": "Determining the Current Thread",
        "output": output,
        "explanation":
            "در این سناریو برای هر thread یک نام مشخص تعیین شده است. با threading.current_thread نام thread جاری دریافت و در خروجی نمایش داده می‌شود."
    }


def scenario_3():
    output = []

    def worker(function_name, delay):
        current_thread = threading.current_thread()

        output.append(
            f"{function_name} started in {current_thread.name}"
        )

        time.sleep(delay)

        output.append(
            f"{function_name} exited after {delay} seconds"
        )

    threads = [
        threading.Thread(
            target=worker,
            name="Fast-Thread",
            args=("function_A", 0.2)
        ),
        threading.Thread(
            target=worker,
            name="Medium-Thread",
            args=("function_B", 0.6)
        ),
        threading.Thread(
            target=worker,
            name="Slow-Thread",
            args=("function_C", 1)
        ),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 2,
        "scenario": 3,
        "title": "Determining the Current Thread",
        "output": output,
        "explanation":
            "در این سناریو thread ها زمان اجرای متفاوت دارند. به همین دلیل ترتیب پیام‌های خروج بر اساس delay هر thread تغییر می‌کند."
    }