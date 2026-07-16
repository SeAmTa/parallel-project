import multiprocessing
import os
import queue
import time


def _collect_queue_messages(result_queue, expected_count):
    messages = []

    for _ in range(expected_count):
        try:
            messages.append(
                result_queue.get(timeout=2)
            )
        except queue.Empty:
            messages.append(
                "Warning: expected message was not received from child process"
            )

    return messages


def _single_child_consumer_worker(task_queue, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{current_process.name} started with PID={os.getpid()}"
    )

    processed_tasks = []

    while True:
        task = task_queue.get()

        if task is None:
            result_queue.put(
                f"{current_process.name} received shutdown sentinel"
            )
            break

        time.sleep(0.10)

        processed_tasks.append(task)

        result_queue.put(
            f"{current_process.name} processed task='{task}'"
        )

    result_queue.put(
        f"{current_process.name} processed tasks in FIFO order: {processed_tasks}"
    )


def scenario_1():
    output = []

    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_single_child_consumer_worker,
        args=(task_queue, result_queue),
        name="Single-Queue-Consumer-Process"
    )

    tasks = [
        "resize-menu-image",
        "generate-invoice-pdf",
        "send-customer-email",
    ]

    output.append(
        f"Parent process PID={os.getpid()} created one Queue for parent-to-child task transfer"
    )

    process.start()

    output.append(
        f"Parent started consumer process name='{process.name}' with PID={process.pid}"
    )

    for task in tasks:
        task_queue.put(task)

        output.append(
            f"Parent put task='{task}' into multiprocessing.Queue"
        )

    task_queue.put(None)

    output.append(
        "Parent put shutdown sentinel into multiprocessing.Queue"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=6
        )
    )

    output.append(
        f"Consumer process exitcode={process.exitcode}"
    )

    output.append(
        "One-way Queue exchange workflow finished"
    )

    return {
        "method": "process",
        "section": 6,
        "scenario": 1,
        "title": "One-Way Parent to Child Queue Exchange",
        "problem":
            "شرح مسئله:\n"
            "فرایند اصلی چند task دارد و می‌خواهد آن‌ها را به یک Process فرزند ارسال کند. "
            "Process فرزند باید taskها را از Queue دریافت کند و به ترتیب FIFO پردازش کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با multiprocessing.Queue داده را از parent process به child process منتقل کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ارتباط یک‌طرفه بین Processها با Queue و استفاده از sentinel برای پایان کار",
        "output": output,
        "explanation":
            "در این سناریو parent یک multiprocessing.Queue می‌سازد و taskها را با put داخل آن قرار می‌دهد. "
            "Process فرزند با get taskها را دریافت می‌کند. Queue داده را بین Processهای جداگانه منتقل می‌کند، برخلاف متغیر معمولی که shared نیست. "
            "در پایان parent مقدار None را به عنوان sentinel داخل Queue می‌گذارد تا child بداند دیگر task جدیدی وجود ندارد و باید متوقف شود."
    }


def _producer_worker(producer_name, item_count, work_queue, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"{producer_name} started in process name='{current_process.name}', PID={os.getpid()}"
    )

    for item_number in range(1, item_count + 1):
        item = f"{producer_name}-Item-{item_number}"

        time.sleep(0.08)

        work_queue.put(item)

        result_queue.put(
            f"{producer_name} put {item} into shared process queue"
        )

    result_queue.put(
        f"{producer_name} finished producing {item_count} items"
    )


def _shared_consumer_worker(work_queue, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Shared consumer started in process name='{current_process.name}', PID={os.getpid()}"
    )

    consumed_items = []

    while True:
        item = work_queue.get()

        if item is None:
            result_queue.put(
                "Shared consumer received shutdown sentinel"
            )
            break

        time.sleep(0.12)

        consumed_items.append(item)

        result_queue.put(
            f"Shared consumer processed {item}"
        )

    result_queue.put(
        f"Shared consumer processed total items={len(consumed_items)}"
    )


def scenario_2():
    output = []

    work_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    consumer_process = multiprocessing.Process(
        target=_shared_consumer_worker,
        args=(work_queue, result_queue),
        name="Shared-Queue-Consumer-Process"
    )

    producer_processes = [
        multiprocessing.Process(
            target=_producer_worker,
            args=("Producer-A", 3, work_queue, result_queue),
            name="Producer-A-Process"
        ),
        multiprocessing.Process(
            target=_producer_worker,
            args=("Producer-B", 3, work_queue, result_queue),
            name="Producer-B-Process"
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created shared Queue for multiple producers and one consumer"
    )

    consumer_process.start()

    output.append(
        f"Parent started consumer process with PID={consumer_process.pid}"
    )

    for process in producer_processes:
        process.start()

        output.append(
            f"Parent started producer process name='{process.name}' with PID={process.pid}"
        )

    for process in producer_processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=17
        )
    )

    for process in producer_processes:
        output.append(
            f"Parent joined producer process name='{process.name}' with exitcode={process.exitcode}"
        )

    work_queue.put(None)

    output.append(
        "Parent put shutdown sentinel after all producers finished"
    )

    consumer_process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=2
        )
    )

    output.append(
        f"Consumer process exitcode={consumer_process.exitcode}"
    )

    output.append(
        "Multiple producers single consumer Queue workflow finished"
    )

    return {
        "method": "process",
        "section": 6,
        "scenario": 2,
        "title": "Multiple Producer Processes and One Consumer Process",
        "problem":
            "شرح مسئله:\n"
            "دو Process تولیدکننده همزمان آیتم تولید می‌کنند و یک Process مصرف‌کننده باید همه آیتم‌ها را از یک Queue مشترک دریافت کند. "
            "parent نباید از shared list معمولی استفاده کند، چون Processها حافظه جدا دارند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند producer process و یک consumer process را با یک multiprocessing.Queue مشترک به هم وصل کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "الگوی many-to-one communication با Queue بین چند Process",
        "output": output,
        "explanation":
            "در این سناریو دو producer process آیتم‌ها را داخل یک Queue مشترک قرار می‌دهند و یک consumer process همان Queue را مصرف می‌کند. "
            "parent ابتدا منتظر تمام شدن producerها می‌ماند، سپس sentinel را داخل Queue قرار می‌دهد تا consumer بعد از مصرف همه آیتم‌ها متوقف شود. "
            "این سناریو با سناریوی اول فرق دارد، چون فقط یک parent و یک child نداریم؛ چند Process تولیدکننده همزمان با یک consumer از طریق Queue مشترک ارتباط دارند."
    }


def _generate_bot_reply(message_text):
    normalized_text = message_text.strip().lower()

    if "hello" in normalized_text:
        return "Hello! How can I help you?"

    if "price" in normalized_text:
        return "Please send the product name so I can check its price."

    if "order" in normalized_text:
        return "Your order request has been received."

    return "I received your message. A support agent will respond soon."


def _telegram_bot_worker(request_queue, response_queue, result_queue):
    current_process = multiprocessing.current_process()

    result_queue.put(
        f"Telegram bot worker started in process name='{current_process.name}', PID={os.getpid()}"
    )

    while True:
        request = request_queue.get()

        if request is None:
            result_queue.put(
                "Telegram bot worker received shutdown sentinel"
            )
            break

        message_id = request["message_id"]
        chat_id = request["chat_id"]
        message_text = request["message_text"]

        result_queue.put(
            f"Telegram bot worker received message_id={message_id} from chat_id={chat_id}"
        )

        time.sleep(0.12)

        reply_text = _generate_bot_reply(message_text)

        response_queue.put(
            {
                "message_id": message_id,
                "chat_id": chat_id,
                "reply_text": reply_text,
                "handled_by": current_process.name
            }
        )

    result_queue.put(
        "Telegram bot worker exits after processing all messages"
    )


def scenario_3():
    output = []

    request_queue = multiprocessing.Queue()
    response_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_telegram_bot_worker,
        args=(
            request_queue,
            response_queue,
            result_queue
        ),
        name="Telegram-Bot-Reply-Worker"
    )

    user_messages = [
        {
            "message_id": "MSG-1",
            "chat_id": 1001,
            "message_text": "Hello"
        },
        {
            "message_id": "MSG-2",
            "chat_id": 1002,
            "message_text": "What is the product price?"
        },
        {
            "message_id": "MSG-3",
            "chat_id": 1001,
            "message_text": "I want to place an order"
        },
    ]

    output.append(
        f"Parent process PID={os.getpid()} created request_queue and response_queue for Telegram bot messages"
    )

    process.start()

    output.append(
        f"Parent started Telegram bot worker with PID={process.pid}"
    )

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=1
        )
    )

    for message in user_messages:
        request_queue.put(message)

        output.append(
            f"Parent received Telegram message_id={message['message_id']} and sent it to child process"
        )

        output.extend(
            _collect_queue_messages(
                result_queue,
                expected_count=1
            )
        )

        try:
            response = response_queue.get(timeout=2)

            output.append(
                f"Parent received generated reply for message_id={response['message_id']}: reply='{response['reply_text']}', handled_by='{response['handled_by']}'"
            )

            output.append(
                f"Parent sent reply back to Telegram chat_id={response['chat_id']}"
            )

        except queue.Empty:
            output.append(
                f"Warning: parent did not receive a reply for message_id={message['message_id']}"
            )

    request_queue.put(None)

    output.append(
        "Parent sent shutdown sentinel to Telegram bot worker"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=2
        )
    )

    output.append(
        f"Telegram bot worker exitcode={process.exitcode}"
    )

    output.append(
        "Bidirectional Telegram bot Queue workflow finished"
    )

    return {
        "method": "process",
        "section": 6,
        "scenario": 3,
        "title": "Telegram Bot Request and Response Queues",
        "problem":
            "شرح مسئله:\n"
            "یک ربات تلگرام پیام کاربران را در parent process دریافت می‌کند، "
            "اما تولید پاسخ در یک child process جداگانه انجام می‌شود. "
            "پس از تولید پاسخ، child باید آن را به parent برگرداند تا parent "
            "پاسخ را برای کاربر ارسال کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با دو multiprocessing.Queue جداگانه، پیام کاربر "
            "را از parent به child فرستاد و پاسخ تولیدشده را از child به "
            "parent بازگرداند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "پیاده‌سازی ارتباط دوطرفه request/response میان Processها با "
            "request_queue و response_queue",
        "output": output,
        "explanation":
            "در این سناریو parent نقش بخش دریافت و ارسال پیام ربات تلگرام را دارد. "
            "پیام کاربر از طریق request_queue به child process منتقل می‌شود. "
            "Child پاسخ را تولید می‌کند و آن را از طریق response_queue به parent "
            "برمی‌گرداند. Parent سپس پاسخ را برای chat_id مربوطه ارسال می‌کند. "
            "جدا بودن Queue درخواست و پاسخ باعث می‌شود جهت حرکت داده‌ها مشخص و "
            "ساختار ارتباط خواناتر باشد. همچنین message_id برای ارتباط دادن هر "
            "پاسخ به پیام اصلی استفاده می‌شود. result_queue فقط برای انتقال "
            "لاگ‌های نمایشی سناریو است."
    }