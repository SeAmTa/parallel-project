import threading
import time


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
            args=(i,),
            name=f"Barista-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("All order threads finished")

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
            "ساخت و اجرای Thread با threading.Thread",
        "output": output,
        "explanation":
            "در این سناریو برای هر سفارش یک Thread جداگانه ساخته و اجرا می‌شود. "
            "همه Threadها تقریباً همزمان start می‌شوند و برنامه با join منتظر می‌ماند تا همه آن‌ها تمام شوند. "
            "این سناریو مفهوم پایه‌ای ساخت Thread، اجرای Thread و انتظار برای پایان همه Threadها را نشان می‌دهد."
    }


def scenario_2():
    output = []
    completion_order = []

    order_preparation_times = [
        (1, 0.60),
        (2, 0.20),
        (3, 0.50),
        (4, 0.10),
        (5, 0.40),
        (6, 0.30),
    ]

    def prepare_order(order_number, preparation_time):
        output.append(
            f"Order #{order_number} started and needs {preparation_time:.2f} seconds"
        )

        time.sleep(preparation_time)

        completion_order.append(order_number)

        output.append(
            f"Order #{order_number} completed after {preparation_time:.2f} seconds"
        )

    threads = []

    for order_number, preparation_time in order_preparation_times:
        thread = threading.Thread(
            target=prepare_order,
            args=(order_number, preparation_time),
            name=f"Order-Thread-{order_number}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    started_order = [
        order_number
        for order_number, _ in order_preparation_times
    ]

    output.append(f"Order start sequence: {started_order}")
    output.append(f"Order completion sequence: {completion_order}")

    return {
        "method": "thread",
        "section": 1,
        "scenario": 2,
        "title": "Coffee Shop Orders with Different Preparation Times",
        "problem":
            "شرح مسئله:\n"
            "در کافی‌شاپ، زمان آماده‌سازی سفارش‌ها یکسان نیست. بعضی سفارش‌ها ساده هستند و سریع آماده می‌شوند، "
            "اما بعضی سفارش‌ها زمان بیشتری نیاز دارند. همه سفارش‌ها تقریباً همزمان شروع می‌شوند.\n\n"
            "سؤال:\n"
            "اگر چند Thread به ترتیب مشخصی start شوند، آیا ترتیب پایان آن‌ها هم الزاماً همان ترتیب شروع خواهد بود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "اجرای همزمان Threadها و تفاوت ترتیب شروع با ترتیب پایان",
        "output": output,
        "explanation":
            "در این سناریو Threadها به ترتیب سفارش‌های ۱ تا ۶ start می‌شوند، اما زمان آماده‌سازی هر سفارش متفاوت است. "
            "به همین دلیل سفارش‌هایی که زمان کمتری دارند زودتر تمام می‌شوند. "
            "خروجی نهایی، ترتیب شروع سفارش‌ها و ترتیب پایان آن‌ها را جداگانه نشان می‌دهد تا مشخص شود در اجرای همزمان، ترتیب پایان الزاماً با ترتیب شروع برابر نیست."
    }


def scenario_3():
    output = []

    def prepare_order(order_number):
        output.append(
            f"Thread for Order #{order_number} started"
        )

        time.sleep(0.2)

        output.append(
            f"Thread for Order #{order_number} finished"
        )

    for i in range(1, 7):
        output.append(
            f"MainThread is creating thread for Order #{i}"
        )

        thread = threading.Thread(
            target=prepare_order,
            args=(i,),
            name=f"Sequential-Order-Thread-{i}"
        )

        thread.start()

        output.append(
            f"MainThread is waiting for Order #{i} thread using join"
        )

        thread.join()

        output.append(
            f"MainThread continued after Order #{i} thread finished"
        )

    output.append("All orders were processed sequentially because join was called immediately")

    return {
        "method": "thread",
        "section": 1,
        "scenario": 3,
        "title": "Thread Creation with Immediate Join and Sequential Execution",
        "problem":
            "شرح مسئله:\n"
            "در این حالت برای هر سفارش یک Thread ساخته می‌شود، اما برنامه بلافاصله بعد از start کردن هر Thread، "
            "با join منتظر پایان همان Thread می‌ماند و سپس Thread بعدی را می‌سازد.\n\n"
            "سؤال:\n"
            "آیا صرفاً ساختن Thread باعث اجرای همزمان می‌شود، یا محل استفاده از join هم روی همزمانی اثر دارد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "تأثیر join روی رفتار اجرایی Threadها",
        "output": output,
        "explanation":
            "در این سناریو برای هر سفارش واقعاً یک Thread ساخته می‌شود، اما چون بلافاصله بعد از start همان Thread، join اجرا می‌شود، "
            "MainThread تا پایان آن سفارش منتظر می‌ماند. بنابراین Thread بعدی فقط بعد از پایان Thread قبلی ساخته و اجرا می‌شود. "
            "این سناریو نشان می‌دهد ساخت Thread به‌تنهایی کافی نیست؛ نحوه استفاده از start و join تعیین می‌کند اجرای برنامه واقعاً همزمان باشد یا ترتیبی."
    }