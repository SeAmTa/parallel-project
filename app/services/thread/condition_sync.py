import threading
import time


def scenario_1():
    output = []
    output_lock = threading.Lock()

    payment_condition = threading.Condition()

    order_state = {
        "payment_confirmed": False,
        "order_prepared": False
    }

    def log(message):
        with output_lock:
            output.append(message)

    def kitchen_worker():
        log(
            "Kitchen-Thread received an order but cannot prepare it before payment confirmation"
        )

        with payment_condition:
            while not order_state["payment_confirmed"]:
                log(
                    "Kitchen-Thread is waiting on payment_condition"
                )

                payment_condition.wait()

            log(
                "Kitchen-Thread detected payment_confirmed=True"
            )

            order_state["order_prepared"] = True

            log(
                "Kitchen-Thread prepared the order after payment was confirmed"
            )

    def cashier_worker():
        log(
            "Cashier-Thread is processing customer payment"
        )

        time.sleep(0.35)

        with payment_condition:
            order_state["payment_confirmed"] = True

            log(
                "Cashier-Thread confirmed payment and calls notify()"
            )

            payment_condition.notify()

    kitchen_thread = threading.Thread(
        target=kitchen_worker,
        name="Kitchen-Thread"
    )

    cashier_thread = threading.Thread(
        target=cashier_worker,
        name="Cashier-Thread"
    )

    kitchen_thread.start()
    cashier_thread.start()

    kitchen_thread.join()
    cashier_thread.join()

    log(
        f"Final order state: {order_state}"
    )

    return {
        "method": "thread",
        "section": 9,
        "scenario": 1,
        "title": "Single Waiter Notification with Condition",
        "problem":
            "شرح مسئله:\n"
            "آشپزخانه یک سفارش دریافت کرده، اما تا زمانی که پرداخت مشتری تأیید نشده نباید سفارش را آماده کند. "
            "Cashier بعد از تأیید پرداخت باید به Kitchen اطلاع دهد که می‌تواند ادامه دهد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان یک Thread را تا تغییر یک وضعیت مشترک منتظر نگه داشت و بعد با notify آن را بیدار کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از threading.Condition برای wait و notify بین دو Thread",
        "output": output,
        "explanation":
            "در این سناریو Kitchen-Thread داخل Condition منتظر می‌ماند تا payment_confirmed برابر True شود. "
            "Cashier-Thread بعد از پردازش پرداخت، همان shared state را تغییر می‌دهد و با notify فقط یک Thread منتظر را بیدار می‌کند. "
            "استفاده از while قبل از wait مهم است، چون Thread بعد از بیدار شدن دوباره شرط واقعی را بررسی می‌کند. "
            "این سناریو ساده‌ترین کاربرد Condition برای هماهنگی یک waiter و یک notifier را نشان می‌دهد."
    }


def scenario_2():
    output = []
    output_lock = threading.Lock()

    startup_condition = threading.Condition()

    startup_state = {
        "config_loaded": False,
        "database_connected": False
    }

    ready_services = []

    def log(message):
        with output_lock:
            output.append(message)

    def service_worker(service_name):
        log(
            f"{service_name} started and is waiting until config and database are both ready"
        )

        with startup_condition:
            startup_condition.wait_for(
                lambda: startup_state["config_loaded"] and startup_state["database_connected"]
            )

            ready_services.append(service_name)

            log(
                f"{service_name} passed wait_for predicate and entered running state"
            )

    def config_loader():
        time.sleep(0.25)

        with startup_condition:
            startup_state["config_loaded"] = True

            log(
                "Config-Loader-Thread loaded configuration and calls notify_all()"
            )

            startup_condition.notify_all()

    def database_connector():
        time.sleep(0.50)

        with startup_condition:
            startup_state["database_connected"] = True

            log(
                "Database-Connector-Thread connected to database and calls notify_all()"
            )

            startup_condition.notify_all()

    service_names = [
        "API-Service-Thread",
        "Worker-Service-Thread",
        "Scheduler-Service-Thread",
    ]

    service_threads = []

    for service_name in service_names:
        thread = threading.Thread(
            target=service_worker,
            args=(service_name,),
            name=service_name
        )

        service_threads.append(thread)
        thread.start()

    config_thread = threading.Thread(
        target=config_loader,
        name="Config-Loader-Thread"
    )

    database_thread = threading.Thread(
        target=database_connector,
        name="Database-Connector-Thread"
    )

    config_thread.start()
    database_thread.start()

    for thread in service_threads:
        thread.join()

    config_thread.join()
    database_thread.join()

    log(
        f"Final startup state: {startup_state}"
    )

    log(
        f"Services that entered running state: {ready_services}"
    )

    return {
        "method": "thread",
        "section": 9,
        "scenario": 2,
        "title": "Multiple Waiters with wait_for and notify_all",
        "problem":
            "شرح مسئله:\n"
            "چند سرویس برنامه فقط زمانی اجازه شروع دارند که هم فایل تنظیمات load شده باشد و هم اتصال دیتابیس برقرار شده باشد. "
            "این دو شرط در زمان‌های متفاوت آماده می‌شوند و چند Thread باید منتظر ترکیب این دو شرط بمانند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند Thread را تا برقرار شدن یک predicate مشترک منتظر نگه داشت و بعد همه آن‌ها را بیدار کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Condition.wait_for برای شرط ترکیبی و notify_all برای چند Thread منتظر",
        "output": output,
        "explanation":
            "در این سناریو چند Service Thread منتظر یک شرط ترکیبی هستند: هم config_loaded باید True باشد و هم database_connected. "
            "به جای wait ساده، از wait_for استفاده شده است تا خود Condition predicate را بعد از هر بیدار شدن دوباره بررسی کند. "
            "وقتی فقط config آماده می‌شود، notify_all صدا زده می‌شود اما predicate هنوز کامل نیست، بنابراین سرویس‌ها ادامه نمی‌دهند. "
            "وقتی database هم آماده شد، predicate کامل می‌شود و همه سرویس‌های منتظر از wait_for عبور می‌کنند. "
            "این سناریو تفاوت Condition برای چند waiter و شرط ترکیبی را نشان می‌دهد."
    }


def scenario_3():
    output = []
    output_lock = threading.Lock()

    buffer_condition = threading.Condition()

    buffer = []
    buffer_capacity = 2

    produced_items = []
    consumed_items = []

    def log(message):
        with output_lock:
            output.append(message)

    def producer():
        items = [
            "Order-1",
            "Order-2",
            "Order-3",
            "Order-4",
            "Order-5",
        ]

        for item in items:
            time.sleep(0.10)

            with buffer_condition:
                while len(buffer) == buffer_capacity:
                    log(
                        f"Producer-Thread found buffer full {buffer} and waits"
                    )

                    buffer_condition.wait()

                buffer.append(item)
                produced_items.append(item)

                log(
                    f"Producer-Thread added {item} to buffer. Buffer={buffer}"
                )

                buffer_condition.notify_all()

        with buffer_condition:
            while len(buffer) == buffer_capacity:
                log(
                    f"Producer-Thread wants to add shutdown sentinel but buffer is full {buffer} and waits"
                )

                buffer_condition.wait()

            buffer.append(None)

            log(
                f"Producer-Thread added shutdown sentinel to buffer. Buffer={buffer}"
            )

            buffer_condition.notify_all()

    def consumer():
        while True:
            with buffer_condition:
                while len(buffer) == 0:
                    log(
                        "Consumer-Thread found buffer empty and waits"
                    )

                    buffer_condition.wait()

                item = buffer.pop(0)

                if item is None:
                    log(
                        "Consumer-Thread received shutdown sentinel"
                    )

                    buffer_condition.notify_all()
                    break

                consumed_items.append(item)

                log(
                    f"Consumer-Thread consumed {item}. Buffer={buffer}"
                )

                buffer_condition.notify_all()

            time.sleep(0.25)

    producer_thread = threading.Thread(
        target=producer,
        name="Producer-Thread"
    )

    consumer_thread = threading.Thread(
        target=consumer,
        name="Consumer-Thread"
    )

    consumer_thread.start()
    producer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    log(
        f"Produced items: {produced_items}"
    )

    log(
        f"Consumed items: {consumed_items}"
    )

    log(
        "Bounded buffer workflow finished"
    )

    return {
        "method": "thread",
        "section": 9,
        "scenario": 3,
        "title": "Custom Bounded Buffer with Condition",
        "problem":
            "شرح مسئله:\n"
            "یک Producer سفارش‌ها را داخل یک buffer کوچک قرار می‌دهد و یک Consumer آن‌ها را پردازش می‌کند. "
            "اگر buffer پر باشد Producer باید منتظر خالی شدن فضا بماند. اگر buffer خالی باشد Consumer باید منتظر رسیدن item جدید بماند. "
            "حتی پیام پایان کار یا sentinel هم نباید ظرفیت buffer را نقض کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با Condition یک buffer محدود ساخت که Producer و Consumer بر اساس وضعیت buffer منتظر بمانند یا ادامه دهند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "پیاده‌سازی producer/consumer با shared buffer، wait، notify_all و بررسی شرط‌های full/empty",
        "output": output,
        "explanation":
            "در این سناریو Condition برای مدیریت یک buffer محدود استفاده شده است. "
            "Producer وقتی buffer پر است داخل while منتظر می‌ماند و Consumer وقتی buffer خالی است منتظر می‌ماند. "
            "بعد از هر تولید یا مصرف، notify_all صدا زده می‌شود تا Thread مقابل دوباره شرط خودش را بررسی کند. "
            "حتی shutdown sentinel هم فقط زمانی وارد buffer می‌شود که ظرفیت آزاد وجود داشته باشد، بنابراین محدودیت buffer_capacity نقض نمی‌شود. "
            "این سناریو با دو سناریوی قبلی فرق دارد، چون Condition اینجا فقط برای یک notification ساده نیست؛ بلکه برای مدیریت state پیوسته یک buffer مشترک استفاده می‌شود."
    }