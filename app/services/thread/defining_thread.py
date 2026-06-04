import threading
import time
import random


def scenario_1():
    output = []

    def prepare_order(order_number):
        output.append(
            f"Order #{order_number} assigned to a separate barista thread"
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
        "title": "Coffee Shop Orders with Multiple Barista Threads",
        "problem":
            "شرح مسئله:\n"
            "یک کافی‌شاپ چند سفارش آنلاین را تقریباً همزمان دریافت می‌کند. "
            "برای اینکه سفارش‌ها سریع‌تر آماده شوند، برای هر سفارش یک Thread جداگانه ساخته می‌شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند سفارش مستقل را به صورت همزمان پردازش کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ساخت و اجرای Thread",
        "output": output,
        "explanation":
            "در این سناریو کافی‌شاپ چند سفارش آنلاین دریافت کرده است. برای هر سفارش یک Thread جدا ساخته می‌شود تا سفارش‌ها به صورت همزمان آماده شوند. این سناریو مفهوم ساخت و اجرای Thread را نشان می‌دهد."
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
        "problem":
            "شرح مسئله:\n"
            "در کافی‌شاپ، زمان آماده‌سازی سفارش‌ها یکسان نیست. بعضی سفارش‌ها ساده هستند و سریع آماده می‌شوند، اما بعضی سفارش‌ها زمان بیشتری نیاز دارند.\n\n"
            "سؤال:\n"
            "اگر همه سفارش‌ها همزمان شروع شوند، آیا ترتیب پایان آن‌ها الزاماً با ترتیب ثبت سفارش‌ها یکی خواهد بود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "اجرای همزمان Threadها و غیرقابل پیش‌بینی بودن ترتیب پایان",
        "output": output,
        "explanation":
            "در این سناریو هر سفارش زمان آماده‌سازی متفاوتی دارد. چون همه سفارش‌ها در Threadهای جدا اجرا می‌شوند، سفارش‌های سریع‌تر زودتر تمام می‌شوند و ترتیب پایان کار ممکن است با ترتیب شماره سفارش‌ها یکسان نباشد."
    }


def scenario_3():
    output = []

    def prepare_order(order_number):
        output.append(
            f"Single barista started preparing Order #{order_number}"
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
        "title": "Single-Barista Coffee Shop with Sequential Orders",
        "problem":
            "شرح مسئله:\n"
            "در این حالت کافی‌شاپ فقط یک باریستا دارد. با اینکه برای هر سفارش یک Thread ساخته می‌شود، باریستا باید سفارش فعلی را کامل آماده کند و بعد سراغ سفارش بعدی برود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان اجرای Threadها را طوری کنترل کرد که هر سفارش پس از پایان سفارش قبلی شروع شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از join برای اجرای ترتیبی Threadها",
        "output": output,
        "explanation":
            "در این سناریو کافی‌شاپ فقط یک باریستا دارد. برای هر سفارش همچنان یک Thread ساخته می‌شود، اما بعد از start بلافاصله join اجرا می‌شود. بنابراین سفارش بعدی تا پایان سفارش قبلی شروع نمی‌شود و خروجی به صورت ترتیبی تولید می‌شود."
    }