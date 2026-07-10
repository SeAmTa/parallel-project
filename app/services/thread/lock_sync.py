import threading
import time


def scenario_1():
    output = []
    tickets_left = 1
    sold_to = []

    def buy_ticket(customer_number):
        nonlocal tickets_left

        output.append(
            f"Customer #{customer_number} is trying to buy the last ticket"
        )

        if tickets_left > 0:
            output.append(
                f"Customer #{customer_number} saw tickets_left={tickets_left} and entered purchase step"
            )

            time.sleep(0.1)

            tickets_left -= 1
            sold_to.append(customer_number)

            output.append(
                f"Customer #{customer_number} completed purchase without lock"
            )
        else:
            output.append(
                f"Customer #{customer_number} could not buy a ticket"
            )

    threads = []

    for i in range(1, 5):
        thread = threading.Thread(
            target=buy_ticket,
            args=(i,),
            name=f"Customer-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Tickets left after unsafe sale: {tickets_left}")
    output.append(f"Customers marked as buyers: {sold_to}")

    if len(sold_to) > 1 or tickets_left < 0:
        output.append(
            "Race condition detected: more than one customer bought the last ticket"
        )

    return {
        "method": "thread",
        "section": 4,
        "scenario": 1,
        "title": "Race Condition Before Using Lock",
        "problem":
            "شرح مسئله:\n"
            "در یک سامانه فروش بلیت کنسرت فقط یک بلیت باقی مانده است. "
            "چند مشتری تقریباً همزمان تلاش می‌کنند همان بلیت آخر را خریداری کنند، اما سیستم هیچ Lock یا مکانیزم همگام‌سازی ندارد.\n\n"
            "سؤال:\n"
            "اگر چند Thread همزمان مقدار بلیت باقی‌مانده را بررسی و تغییر دهند، آیا ممکن است چند مشتری تصور کنند خریدشان موفق بوده است؟\n\n"
            "مفهوم مورد بررسی:\n"
            "Race Condition قبل از استفاده از Lock",
        "output": output,
        "explanation":
            "این سناریو عمداً بدون Lock نوشته شده است تا مشکل Race Condition دیده شود. "
            "چند مشتری تقریباً همزمان مقدار tickets_left را بررسی می‌کنند. "
            "چون بین بررسی مقدار و کم کردن آن یک تأخیر کوتاه وجود دارد، ممکن است چند Thread قبل از تغییر مقدار، tickets_left را برابر ۱ ببینند. "
            "در نتیجه چند مشتری می‌توانند خودشان را خریدار آخرین بلیت ثبت کنند و مقدار tickets_left حتی منفی شود. "
            "این همان مشکلی است که Lock برای جلوگیری از آن استفاده می‌شود."
    }


def scenario_2():
    output = []
    tickets_left = 1
    sold_to = []
    lock = threading.Lock()

    def buy_ticket(customer_number):
        nonlocal tickets_left

        output.append(
            f"Customer #{customer_number} is waiting for reservation lock"
        )

        with lock:
            output.append(
                f"Customer #{customer_number} entered critical section with tickets_left={tickets_left}"
            )

            if tickets_left > 0:
                time.sleep(0.1)

                tickets_left -= 1
                sold_to.append(customer_number)

                output.append(
                    f"Customer #{customer_number} successfully bought the last ticket"
                )
            else:
                output.append(
                    f"Customer #{customer_number} failed: no ticket left"
                )

            output.append(
                f"Customer #{customer_number} left critical section"
            )

    threads = []

    for i in range(1, 4):
        thread = threading.Thread(
            target=buy_ticket,
            args=(i,),
            name=f"Customer-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Tickets left after safe sale: {tickets_left}")
    output.append(f"Final buyer list: {sold_to}")

    if len(sold_to) == 1 and tickets_left == 0:
        output.append(
            "Lock protected the critical section: only one customer bought the last ticket"
        )

    return {
        "method": "thread",
        "section": 4,
        "scenario": 2,
        "title": "Concert Ticket Sale Protected by Lock",
        "problem":
            "شرح مسئله:\n"
            "همان سامانه فروش بلیت اکنون از Lock استفاده می‌کند. "
            "چند مشتری همزمان درخواست خرید می‌دهند، اما فقط یک نفر در هر لحظه اجازه دارد وارد بخش بررسی و کم کردن تعداد بلیت شود.\n\n"
            "سؤال:\n"
            "آیا Lock می‌تواند از فروش اشتباه آخرین بلیت به چند مشتری جلوگیری کند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محافظت از Critical Section با Lock",
        "output": output,
        "explanation":
            "این سناریو همان مسئله فروش آخرین بلیت را اجرا می‌کند، اما بخش بررسی و کم کردن tickets_left داخل Lock قرار گرفته است. "
            "به این بخش Critical Section گفته می‌شود، چون چند Thread به داده مشترک دسترسی دارند. "
            "Lock تضمین می‌کند در هر لحظه فقط یک Thread وارد این بخش شود. "
            "بنابراین فقط اولین مشتری بلیت را می‌خرد و بقیه بعد از ورود به بخش بحرانی متوجه می‌شوند بلیتی باقی نمانده است."
    }


def scenario_3():
    output = []
    lock = threading.Lock()
    central_log = []
    log_entry_number = 0

    def atm_transaction(atm_number):
        nonlocal log_entry_number

        output.append(
            f"ATM #{atm_number} prepared a transaction log"
        )

        time.sleep(0.05)

        output.append(
            f"ATM #{atm_number} is waiting to write into the central log"
        )

        with lock:
            log_entry_number += 1
            entry_number = log_entry_number

            output.append(
                f"ATM #{atm_number} entered log critical section"
            )

            central_log.append(
                f"Log entry #{entry_number}: transaction written by ATM #{atm_number}"
            )

            time.sleep(0.15)

            output.append(
                f"ATM #{atm_number} finished writing log entry #{entry_number}"
            )

    threads = []

    for i in range(1, 8):
        thread = threading.Thread(
            target=atm_transaction,
            args=(i,),
            name=f"ATM-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Final central transaction log:")

    for log in central_log:
        output.append(log)

    output.append(
        f"Total log entries written safely: {len(central_log)}"
    )

    return {
        "method": "thread",
        "section": 4,
        "scenario": 3,
        "title": "Central Transaction Log Protected by Lock",
        "problem":
            "شرح مسئله:\n"
            "چند دستگاه ATM همزمان تراکنش انجام می‌دهند و همه باید گزارش خود را در یک لاگ مرکزی ثبت کنند. "
            "این لاگ یک منبع مشترک است و نباید چند Thread همزمان داخل آن بنویسند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان نوشتن در یک منبع مشترک را طوری کنترل کرد که در هر لحظه فقط یک Thread وارد بخش نوشتن شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محافظت از منبع مشترک با Lock",
        "output": output,
        "explanation":
            "در این سناریو چند دستگاه ATM همزمان می‌خواهند داخل یک لاگ مرکزی بنویسند. "
            "نوشتن در لاگ مرکزی یک Critical Section است، چون هم central_log و هم شماره entry بین Threadها مشترک هستند. "
            "با Lock تضمین می‌شود در هر لحظه فقط یک Thread شماره لاگ را افزایش دهد و متن لاگ را ثبت کند. "
            "به همین دلیل شماره‌های لاگ بدون تداخل و به صورت منظم ایجاد می‌شوند."
    }