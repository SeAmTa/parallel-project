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
            
            parking_time = 0.25 if car_number % 2 == 1 else 0.7
            time.sleep(parking_time)

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
    output_lock = threading.Lock()

    payment_gateway = threading.Semaphore(2)

    def log(message):
        with output_lock:
            output.append(message)

    def payment_request(customer_name, processing_time):
        log(f"{customer_name} is trying to access the payment gateway")

        acquired = payment_gateway.acquire(timeout=0.08)

        if not acquired:
            log(
                f"{customer_name} could not access the gateway in time "
                f"and was redirected to the fallback queue"
            )
            return

        try:
            log(f"{customer_name} entered the payment gateway")
            time.sleep(processing_time)
            log(f"{customer_name} payment completed successfully")
        finally:
            payment_gateway.release()
            log(f"{customer_name} released the payment gateway slot")

    customers = [
        ("Customer-1", 0.18),
        ("Customer-2", 0.18),
        ("Customer-3", 0.05),
        ("Customer-4", 0.05),
        ("Customer-5", 0.05),
    ]

    threads = [
        threading.Thread(
            target=payment_request,
            args=(customer_name, processing_time),
            name=customer_name
        )
        for customer_name, processing_time in customers
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 6,
        "scenario": 2,
        "title": "Using Semaphore with Timeout and Fallback Path",
        "problem": (
            "یک درگاه پرداخت فقط می‌تواند همزمان به دو مشتری سرویس بدهد. مشتری‌ها نباید "
            "برای همیشه منتظر بمانند. اگر یک مشتری در مدت زمان مشخص نتواند وارد درگاه شود، "
            "باید به صف جایگزین منتقل شود."
        ),
        "output": output,
        "explanation": (
            "در این سناریو از Semaphore همراه با acquire(timeout=...) استفاده شده است. "
            "برخلاف یک مثال ساده که همه Threadها تا آزاد شدن ظرفیت منتظر می‌مانند، اینجا "
            "هر Thread فقط مدت محدودی منتظر می‌ماند. اگر در آن زمان ظرفیت آزاد نشود، Thread "
            "به جای مسدود ماندن، مسیر جایگزین را اجرا می‌کند. بنابراین این سناریو از نظر "
            "عملکردی با مثال ساده محدودسازی ظرفیت متفاوت است."
        )
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