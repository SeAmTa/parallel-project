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
            time.sleep(0.1)

            tickets_left -= 1
            sold_to.append(customer_number)

            output.append(
                f"Customer #{customer_number} thinks they bought the last ticket"
            )
        else:
            output.append(
                f"Customer #{customer_number} could not buy a ticket"
            )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=buy_ticket,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Tickets left: {tickets_left}")
    output.append(f"Customers marked as buyers: {sold_to}")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 1,
        "title": "Concert Ticket Sale Without Reservation Lock",
        "problem":
            "شرح مسئله:\n"
            "در یک سامانه فروش بلیت کنسرت فقط یک بلیت باقی مانده است. چند مشتری به صورت همزمان تلاش می‌کنند همان بلیت آخر را خریداری کنند، اما سیستم هیچ Lock یا مکانیزم همگام‌سازی ندارد.\n\n"
            "سؤال:\n"
            "اگر چند Thread همزمان مقدار بلیت باقی‌مانده را بررسی و تغییر دهند، آیا ممکن است چند مشتری تصور کنند خریدشان موفق بوده است؟\n\n"
            "مفهوم مورد بررسی:\n"
            "Race Condition در دسترسی همزمان به داده مشترک",
        "output": output,
        "explanation":
            "در این سناریو فقط یک بلیت باقی مانده است، اما چند مشتری همزمان تلاش می‌کنند آن را بخرند. چون از Lock استفاده نشده، چند thread ممکن است قبل از کم شدن مقدار بلیت، مقدار قبلی را ببینند و فکر کنند خرید موفق بوده است. این حالت Race Condition را نشان می‌دهد."
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
                f"Customer #{customer_number} entered reservation system"
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

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=buy_ticket,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Tickets left: {tickets_left}")
    output.append(f"Final buyer list: {sold_to}")

    return {
        "method": "thread",
        "section": 4,
        "scenario": 2,
        "title": "Concert Ticket Sale With Reservation Lock",
        "problem":
            "شرح مسئله:\n"
            "همان سامانه فروش بلیت اکنون از Lock استفاده می‌کند. چند مشتری همزمان درخواست خرید می‌دهند، اما فقط یک نفر در هر لحظه اجازه دارد وارد بخش بررسی و کم کردن تعداد بلیت شود.\n\n"
            "سؤال:\n"
            "آیا Lock می‌تواند از فروش اشتباه آخرین بلیت به چند مشتری جلوگیری کند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محافظت از Critical Section با Lock",
        "output": output,
        "explanation":
            "این سناریو همان فروش آخرین بلیت را اجرا می‌کند، اما بخش بررسی و کم کردن تعداد بلیت داخل Lock قرار گرفته است. بنابراین فقط یک مشتری می‌تواند وارد بخش بحرانی شود و فقط یک نفر بلیت را می‌خرد."
    }


def scenario_3():
    output = []
    lock = threading.Lock()
    central_log = []

    def atm_transaction(atm_number):
        output.append(
            f"ATM #{atm_number} is preparing a transaction log"
        )

        with lock:
            output.append(
                f"ATM #{atm_number} is writing to the central log"
            )

            central_log.append(
                f"Transaction log written by ATM #{atm_number}"
            )

            time.sleep(0.2)

            output.append(
                f"ATM #{atm_number} finished writing"
            )

    threads = []

    for i in range(1, 8):
        thread = threading.Thread(
            target=atm_transaction,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Final central transaction log:")
    output.extend(central_log)

    return {
        "method": "thread",
        "section": 4,
        "scenario": 3,
        "title": "Central Transaction Log Protected by Lock",
        "problem":
            "شرح مسئله:\n"
            "چند دستگاه ATM همزمان تراکنش انجام می‌دهند و همه باید گزارش خود را در یک لاگ مرکزی ثبت کنند. این لاگ یک منبع مشترک است و نباید چند Thread همزمان داخل آن بنویسند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان نوشتن در یک منبع مشترک را طوری کنترل کرد که در هر لحظه فقط یک Thread وارد بخش نوشتن شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محافظت از منبع مشترک با Lock",
        "output": output,
        "explanation":
            "در این سناریو چند دستگاه ATM همزمان می‌خواهند داخل یک لاگ مرکزی بنویسند. نوشتن در لاگ یک منبع مشترک است، پس با Lock محافظت شده تا در هر لحظه فقط یک thread وارد بخش نوشتن شود."
    }