import queue
import threading
import time


def scenario_1():
    output = []
    output_lock = threading.Lock()

    order_queue = queue.Queue()

    produced_orders = []
    consumed_orders = []

    def log(message):
        with output_lock:
            output.append(message)

    def producer():
        orders = [
            "Order-1",
            "Order-2",
            "Order-3",
            "Order-4",
        ]

        for order in orders:
            time.sleep(0.10)

            order_queue.put(order)
            produced_orders.append(order)

            log(
                f"Producer-Thread put {order} into FIFO queue"
            )

        order_queue.put(None)

        log(
            "Producer-Thread put shutdown sentinel into FIFO queue"
        )

    def consumer():
        while True:
            item = order_queue.get()

            if item is None:
                log(
                    "Consumer-Thread received shutdown sentinel and stops"
                )

                break

            consumed_orders.append(item)

            log(
                f"Consumer-Thread got {item} from FIFO queue"
            )

            time.sleep(0.18)

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
        f"Produced orders: {produced_orders}"
    )

    log(
        f"Consumed orders: {consumed_orders}"
    )

    log(
        "FIFO producer/consumer workflow finished"
    )

    return {
        "method": "thread",
        "section": 10,
        "scenario": 1,
        "title": "FIFO Producer Consumer with Queue",
        "problem":
            "شرح مسئله:\n"
            "یک Producer سفارش‌ها را تولید می‌کند و یک Consumer باید آن‌ها را به همان ترتیبی که وارد سیستم شده‌اند پردازش کند. "
            "بین Producer و Consumer نباید shared list دستی و Lock جداگانه استفاده شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان داده را بین دو Thread به صورت امن و FIFO منتقل کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از queue.Queue برای ارتباط امن بین Threadها با ترتیب FIFO",
        "output": output,
        "explanation":
            "در این سناریو Producer داده‌ها را با put داخل Queue قرار می‌دهد و Consumer آن‌ها را با get دریافت می‌کند. "
            "queue.Queue به صورت داخلی thread-safe است، بنابراین برای عملیات put و get نیازی به Lock جداگانه نداریم. "
            "ترتیب مصرف با ترتیب تولید یکسان است، چون Queue معمولی در Python رفتار FIFO دارد. "
            "در پایان هم از sentinel یعنی None برای اعلام پایان کار Consumer استفاده شده است."
    }


def scenario_2():
    output = []
    output_lock = threading.Lock()

    priority_queue = queue.PriorityQueue()

    processed_tasks = []

    def log(message):
        with output_lock:
            output.append(message)

    def dispatcher():
        tasks = [
            (3, "Generate monthly analytics"),
            (1, "Fix payment outage"),
            (4, "Clean temporary files"),
            (2, "Send delayed invoices"),
        ]

        for priority, task_name in tasks:
            priority_queue.put((priority, task_name))

            log(
                f"Dispatcher-Thread queued task '{task_name}' with priority={priority}"
            )

            time.sleep(0.05)

        priority_queue.put((999, None))

        log(
            "Dispatcher-Thread queued shutdown sentinel with lowest priority"
        )

    def worker():
        while True:
            priority, task_name = priority_queue.get()

            if task_name is None:
                log(
                    "Priority-Worker-Thread received shutdown sentinel and stops"
                )

                break

            processed_tasks.append(
                (priority, task_name)
            )

            log(
                f"Priority-Worker-Thread processed priority={priority} task '{task_name}'"
            )

            time.sleep(0.10)

    dispatcher_thread = threading.Thread(
        target=dispatcher,
        name="Dispatcher-Thread"
    )

    worker_thread = threading.Thread(
        target=worker,
        name="Priority-Worker-Thread"
    )

    dispatcher_thread.start()

    dispatcher_thread.join()

    log(
        "All priority tasks are queued before worker starts consuming"
    )

    worker_thread.start()

    worker_thread.join()

    log(
        f"Processed tasks in priority order: {processed_tasks}"
    )

    log(
        "Priority queue workflow finished"
    )

    return {
        "method": "thread",
        "section": 10,
        "scenario": 2,
        "title": "Priority-Based Task Processing with PriorityQueue",
        "problem":
            "شرح مسئله:\n"
            "چند task وارد سیستم می‌شوند، اما ترتیب پردازش نباید صرفاً بر اساس زمان ورود باشد. "
            "Taskهای بحرانی‌تر باید زودتر پردازش شوند، حتی اگر دیرتر وارد صف شده باشند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان صفی ساخت که Thread مصرف‌کننده taskها را بر اساس priority دریافت کند، نه FIFO ساده؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از queue.PriorityQueue برای پردازش داده‌ها بر اساس اولویت",
        "output": output,
        "explanation":
            "در این سناریو از PriorityQueue استفاده شده است. هر item به شکل یک tuple شامل priority و task_name داخل صف قرار می‌گیرد. "
            "PriorityQueue کوچک‌ترین مقدار priority را زودتر برمی‌گرداند، بنابراین task با priority=1 قبل از priority=2 و priority=3 پردازش می‌شود. "
            "این سناریو با Queue ساده فرق دارد، چون ترتیب خروجی بر اساس اولویت است نه صرفاً ترتیب ورود. "
            "برای اینکه رفتار priority واضح و قابل دفاع باشد، همه taskها قبل از شروع Worker وارد صف شده‌اند."
    }


def scenario_3():
    output = []
    output_lock = threading.Lock()

    task_queue = queue.Queue()

    completed_tasks = []

    def log(message):
        with output_lock:
            output.append(message)

    def worker(worker_name):
        while True:
            task = task_queue.get()

            if task is None:
                log(
                    f"{worker_name} received shutdown sentinel"
                )

                task_queue.task_done()
                break

            log(
                f"{worker_name} started {task}"
            )

            time.sleep(0.20)

            completed_tasks.append(
                f"{worker_name}:{task}"
            )

            log(
                f"{worker_name} completed {task} and calls task_done()"
            )

            task_queue.task_done()

    tasks = [
        "Resize image",
        "Send email",
        "Build report",
        "Update cache",
        "Write audit log",
    ]

    workers = [
        "Queue-Worker-1",
        "Queue-Worker-2",
    ]

    worker_threads = []

    for worker_name in workers:
        thread = threading.Thread(
            target=worker,
            args=(worker_name,),
            name=worker_name
        )

        worker_threads.append(thread)
        thread.start()

    for task in tasks:
        task_queue.put(task)

        log(
            f"Main thread queued task: {task}"
        )

    log(
        "Main thread calls queue.join() and waits until all queued tasks call task_done()"
    )

    task_queue.join()

    log(
        "queue.join() returned because all real tasks were completed"
    )

    for _ in workers:
        task_queue.put(None)

    log(
        "Main thread queued shutdown sentinels for workers"
    )

    task_queue.join()

    for thread in worker_threads:
        thread.join()

    log(
        f"Completed task records: {completed_tasks}"
    )

    log(
        "Queue task tracking workflow finished"
    )

    return {
        "method": "thread",
        "section": 10,
        "scenario": 3,
        "title": "Queue Task Tracking with task_done and join",
        "problem":
            "شرح مسئله:\n"
            "چند Worker از یک Queue مشترک task دریافت می‌کنند. Main thread نباید فقط بعد از put کردن taskها ادامه دهد؛ "
            "بلکه باید مطمئن شود همه taskها واقعاً پردازش شده‌اند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با Queue منتظر ماند تا همه itemهای صف توسط Workerها کامل پردازش شوند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از task_done و queue.join برای tracking پایان پردازش taskها",
        "output": output,
        "explanation":
            "در این سناریو Queue فقط برای انتقال داده نیست، بلکه برای tracking وضعیت taskها هم استفاده می‌شود. "
            "هر بار که main thread با put یک task وارد صف می‌کند، شمارنده داخلی unfinished tasks افزایش پیدا می‌کند. "
            "هر Worker بعد از پایان پردازش هر task باید task_done را صدا بزند. "
            "متد queue.join تا زمانی block می‌شود که برای همه taskهای واردشده task_done صدا زده شده باشد. "
            "این سناریو با دو سناریوی قبلی فرق دارد، چون تمرکزش روی اطمینان از completion همه taskهاست، نه فقط انتقال یا اولویت‌بندی داده."
    }