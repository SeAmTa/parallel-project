import threading
import time
import random


def scenario_1():
    output = []
    parking_semaphore = threading.Semaphore(2)

    def car_enter_parking(car_number):
        output.append(
            f"Car #{car_number} is waiting for a parking spot"
        )

        with parking_semaphore:
            output.append(
                f"Car #{car_number} entered the parking lot"
            )

            time.sleep(0.5)

            output.append(
                f"Car #{car_number} left the parking lot"
            )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=car_enter_parking,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Parking simulation finished")

    return {
        "method": "thread",
        "section": 6,
        "scenario": 1,
        "title": "Limited Parking Lot with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "یک پارکینگ فقط دو جای خالی دارد، اما ۱۰ خودرو تقریباً همزمان به ورودی پارکینگ می‌رسند. اگر همه خودروها بدون کنترل وارد شوند، ظرفیت پارکینگ رعایت نمی‌شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان تضمین کرد که در هر لحظه حداکثر دو خودرو داخل پارکینگ باشند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محدود کردن تعداد Threadهای همزمان با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو ۱۰ خودرو می‌خواهند وارد پارکینگ شوند، اما فقط ۲ جای پارک وجود دارد. Semaphore با ظرفیت ۲ باعث می‌شود حداکثر دو خودرو همزمان وارد پارکینگ شوند. این سناریو کاربرد Semaphore به عنوان محدودکننده تعداد اجرای همزمان را نشان می‌دهد."
    }


def scenario_2():
    output = []
    download_slots = threading.Semaphore(3)

    def download_file(user_number):
        output.append(
            f"User #{user_number} is waiting for an available download slot"
        )

        with download_slots:
            download_time = round(
                random.uniform(0.2, 0.8),
                2
            )

            output.append(
                f"User #{user_number} started downloading using one server slot"
            )

            time.sleep(download_time)

            output.append(
                f"User #{user_number} finished download after {download_time} seconds"
            )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=download_file,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("All download requests were processed")

    return {
        "method": "thread",
        "section": 6,
        "scenario": 2,
        "title": "Download Server Resource Pool with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "یک سرور دانلود فقط سه slot همزمان برای دانلود فایل دارد، اما چند کاربر همزمان درخواست دانلود ارسال می‌کنند. هر کاربر باید برای شروع دانلود یکی از slotهای محدود سرور را دریافت کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان منابع محدود سرور را بین چند Thread مدیریت کرد تا بیش از ظرفیت مجاز استفاده نشوند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "مدیریت Resource Pool با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو یک سرور دانلود فقط ۳ slot همزمان دارد. هر کاربر برای شروع دانلود باید یکی از این slotها را بگیرد و پس از پایان دانلود آن را آزاد می‌کند. این سناریو Semaphore را به عنوان ابزار مدیریت Resource Pool نشان می‌دهد."
    }


def scenario_3():
    output = []
    ready_food = threading.Semaphore(0)
    kitchen_counter = []
    counter_lock = threading.Lock()

    def chef():
        for i in range(1, 6):
            time.sleep(0.3)

            with counter_lock:
                meal = f"Meal #{i}"
                kitchen_counter.append(meal)

                output.append(
                    f"Chef prepared {meal}"
                )

            ready_food.release()

    def waiter():
        for _ in range(1, 6):
            output.append(
                "Waiter is waiting for a prepared meal"
            )

            ready_food.acquire()

            with counter_lock:
                meal = kitchen_counter.pop(0)

                output.append(
                    f"Waiter served {meal}"
                )

    chef_thread = threading.Thread(target=chef)
    waiter_thread = threading.Thread(target=waiter)

    waiter_thread.start()
    chef_thread.start()

    chef_thread.join()
    waiter_thread.join()

    output.append("Restaurant kitchen workflow finished")

    return {
        "method": "thread",
        "section": 6,
        "scenario": 3,
        "title": "Restaurant Kitchen Producer Consumer with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "در یک رستوران، آشپز غذا را آماده می‌کند و گارسون غذا را سرو می‌کند. گارسون نباید قبل از آماده شدن غذا چیزی را از پیشخوان بردارد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان بین Thread تولیدکننده غذا و Thread مصرف‌کننده غذا هماهنگی ایجاد کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "هماهنگی Producer و Consumer با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو آشپز نقش Producer و گارسون نقش Consumer را دارد. گارسون نباید غذایی را بردارد که هنوز آماده نشده است، بنابراین با Semaphore مقداردهی اولیه صفر منتظر می‌ماند. هر بار آشپز غذا آماده می‌کند، با release به گارسون اجازه مصرف می‌دهد. این سناریو هماهنگی Producer/Consumer با Semaphore را نشان می‌دهد."
    }