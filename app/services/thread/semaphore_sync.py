import threading
import time


def scenario_1():
    output = []
    parking_semaphore = threading.Semaphore(2)
    counter_lock = threading.Lock()

    cars_inside = 0
    max_cars_inside = 0

    def car_enter_parking(car_number):
        nonlocal cars_inside
        nonlocal max_cars_inside

        output.append(
            f"Car #{car_number} is waiting for a parking spot"
        )

        with parking_semaphore:
            with counter_lock:
                cars_inside += 1
                max_cars_inside = max(max_cars_inside, cars_inside)

                output.append(
                    f"Car #{car_number} entered the parking lot | cars_inside={cars_inside}"
                )

            time.sleep(0.4)

            with counter_lock:
                cars_inside -= 1

                output.append(
                    f"Car #{car_number} left the parking lot | cars_inside={cars_inside}"
                )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=car_enter_parking,
            args=(i,),
            name=f"Parking-Car-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"Maximum cars inside at the same time: {max_cars_inside}"
    )
    output.append("Parking simulation finished")

    return {
        "method": "thread",
        "section": 6,
        "scenario": 1,
        "title": "Limited Parking Lot with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "یک پارکینگ فقط دو جای خالی دارد، اما ۱۰ خودرو تقریباً همزمان به ورودی پارکینگ می‌رسند. "
            "اگر همه خودروها بدون کنترل وارد شوند، ظرفیت پارکینگ رعایت نمی‌شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان تضمین کرد که در هر لحظه حداکثر دو خودرو داخل پارکینگ باشند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "محدود کردن تعداد Threadهای همزمان با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو Semaphore با ظرفیت ۲ ساخته شده است. "
            "یعنی در هر لحظه فقط دو Thread اجازه دارند وارد بخش پارکینگ شوند. "
            "برای اینکه این محدودیت در خروجی قابل مشاهده باشد، تعداد خودروهای داخل پارکینگ با cars_inside ثبت می‌شود و بیشترین مقدار همزمان با max_cars_inside گزارش می‌شود. "
            "اگر Semaphore درست عمل کند، مقدار max_cars_inside نباید از ۲ بیشتر شود."
    }


def scenario_2():
    output = []
    download_slots = threading.Semaphore(3)
    counter_lock = threading.Lock()

    active_downloads = 0
    max_active_downloads = 0

    download_times = {
        1: 0.45,
        2: 0.30,
        3: 0.55,
        4: 0.25,
        5: 0.40,
        6: 0.35,
        7: 0.50,
        8: 0.20,
        9: 0.30,
        10: 0.45,
    }

    def download_file(user_number):
        nonlocal active_downloads
        nonlocal max_active_downloads

        output.append(
            f"User #{user_number} is waiting for an available download slot"
        )

        with download_slots:
            with counter_lock:
                active_downloads += 1
                max_active_downloads = max(
                    max_active_downloads,
                    active_downloads
                )

                output.append(
                    f"User #{user_number} started downloading | active_downloads={active_downloads}"
                )

            time.sleep(download_times[user_number])

            with counter_lock:
                active_downloads -= 1

                output.append(
                    f"User #{user_number} finished download after {download_times[user_number]:.2f} seconds | active_downloads={active_downloads}"
                )

    threads = []

    for i in range(1, 11):
        thread = threading.Thread(
            target=download_file,
            args=(i,),
            name=f"Download-User-Thread-{i}"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"Maximum active downloads at the same time: {max_active_downloads}"
    )
    output.append("All download requests were processed")

    return {
        "method": "thread",
        "section": 6,
        "scenario": 2,
        "title": "Download Server Resource Pool with Semaphore",
        "problem":
            "شرح مسئله:\n"
            "یک سرور دانلود فقط سه slot همزمان برای دانلود فایل دارد، اما چند کاربر همزمان درخواست دانلود ارسال می‌کنند. "
            "هر کاربر باید برای شروع دانلود یکی از slotهای محدود سرور را دریافت کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان منابع محدود سرور را بین چند Thread مدیریت کرد تا بیش از ظرفیت مجاز استفاده نشوند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "مدیریت Resource Pool با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو سرور دانلود فقط سه slot همزمان دارد. "
            "Semaphore با ظرفیت ۳ باعث می‌شود حداکثر سه کاربر همزمان وارد بخش دانلود شوند. "
            "برای نمایش دقیق این رفتار، تعداد دانلودهای فعال با active_downloads ثبت می‌شود و بیشترین مقدار همزمان با max_active_downloads گزارش می‌شود. "
            "اگر Semaphore درست عمل کند، مقدار max_active_downloads نباید از ۳ بیشتر شود."
    }


def scenario_3():
    output = []
    ready_food = threading.Semaphore(0)
    counter_lock = threading.Lock()
    kitchen_counter = []

    def chef():
        for i in range(1, 6):
            time.sleep(0.25)

            with counter_lock:
                meal = f"Meal #{i}"
                kitchen_counter.append(meal)

                output.append(
                    f"Chef prepared {meal} and placed it on the counter"
                )

            ready_food.release()

            output.append(
                f"Chef released semaphore for {meal}"
            )

    def waiter():
        for _ in range(1, 6):
            output.append(
                "Waiter is blocked until a prepared meal is available"
            )

            ready_food.acquire()

            output.append(
                "Waiter acquired semaphore and can take one meal"
            )

            with counter_lock:
                meal = kitchen_counter.pop(0)

                output.append(
                    f"Waiter served {meal}"
                )

    chef_thread = threading.Thread(
        target=chef,
        name="Chef-Producer-Thread"
    )

    waiter_thread = threading.Thread(
        target=waiter,
        name="Waiter-Consumer-Thread"
    )

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
            "در یک رستوران، آشپز غذا را آماده می‌کند و گارسون غذا را سرو می‌کند. "
            "گارسون نباید قبل از آماده شدن غذا چیزی را از پیشخوان بردارد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان بین Thread تولیدکننده غذا و Thread مصرف‌کننده غذا هماهنگی ایجاد کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "هماهنگی Producer و Consumer با Semaphore",
        "output": output,
        "explanation":
            "در این سناریو آشپز نقش Producer و گارسون نقش Consumer را دارد. "
            "Semaphore با مقدار اولیه صفر ساخته شده است، بنابراین گارسون در ابتدا اجازه مصرف ندارد و روی acquire منتظر می‌ماند. "
            "هر بار که آشپز یک غذا آماده می‌کند، آن را روی پیشخوان می‌گذارد و با release یک مجوز به Semaphore اضافه می‌کند. "
            "سپس گارسون با acquire آن مجوز را دریافت می‌کند و غذا را سرو می‌کند. "
            "برای محافظت از kitchen_counter نیز از Lock جداگانه استفاده شده است."
    }