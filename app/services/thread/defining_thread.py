import threading
import time
import random


def scenario_1():
    output = []

    def prepare_order(order_number):
        output.append(
            f"Order #{order_number} assigned to a barista thread"
        )

        time.sleep(0.2)

        output.append(
            f"Order #{order_number} is ready"
        )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=prepare_order,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 1,
        "title": "Coffee Shop Online Orders - Parallel Preparation",
        "output": output,
        "explanation":
            "در این سناریو ۱۰ سفارش آنلاین وارد کافی‌شاپ شده‌اند. برای هر سفارش یک thread جدا ساخته می‌شود تا سفارش‌ها به صورت همزمان آماده شوند. این حالت مفهوم ساختن thread را نشان می‌دهد."
    }


def scenario_2():
    output = []

    def prepare_order(order_number):
        preparation_time = round(
            random.uniform(0.1, 1.0),
            2
        )

        output.append(
            f"Order #{order_number} started and needs {preparation_time} seconds"
        )

        time.sleep(preparation_time)

        output.append(
            f"Order #{order_number} completed in {preparation_time} seconds"
        )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=prepare_order,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 2,
        "title": "Coffee Shop Orders with Different Preparation Times",
        "output": output,
        "explanation":
            "در این سناریو سفارش‌ها زمان آماده‌سازی متفاوتی دارند. چون همه سفارش‌ها با threadهای جدا اجرا می‌شوند، سفارش‌های سبک‌تر زودتر تمام می‌شوند و ترتیب خروجی ممکن است با شماره سفارش‌ها یکی نباشد."
    }


def scenario_3():
    output = []

    def prepare_order(order_number):
        output.append(
            f"Single barista started Order #{order_number}"
        )

        time.sleep(0.2)

        output.append(
            f"Single barista finished Order #{order_number}"
        )

    for i in range(1, 11):
        thread = threading.Thread(
            target=prepare_order,
            args=(i,)
        )

        thread.start()
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 3,
        "title": "Coffee Shop with One Barista - Sequential Preparation",
        "output": output,
        "explanation":
            "در این سناریو برای هر سفارش هنوز یک thread ساخته می‌شود، اما چون فقط یک باریستا داریم، بعد از start هر thread بلافاصله join اجرا می‌شود. بنابراین سفارش بعدی تا پایان سفارش قبلی شروع نمی‌شود و اجرا ترتیبی است."
    }