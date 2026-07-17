import multiprocessing
import os
import time


def _calculate_order_total(order_task):
    order_id, item_prices, delay = order_task

    current_process = multiprocessing.current_process()

    time.sleep(delay)

    total_price = sum(item_prices)

    return {
        "order_id": order_id,
        "total_price": total_price,
        "message":
            f"{order_id} calculated total={total_price} inside process name='{current_process.name}', PID={os.getpid()}, delay={delay}"
    }


def scenario_1():
    output = []

    order_tasks = [
        ("Order-1", [120, 80, 50], 0.30),
        ("Order-2", [40, 25], 0.10),
        ("Order-3", [300, 150, 75], 0.20),
        ("Order-4", [60, 60, 30], 0.15),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created a Pool with 2 worker processes"
    )

    output.append(
        "Parent sends order calculation tasks to Pool.map"
    )

    output.append(
        "Each task has a different delay, but Pool.map returns results in the same order as the input list"
    )

    pool = multiprocessing.Pool(
        processes=2
    )

    try:
        results = pool.map(
            _calculate_order_total,
            order_tasks
        )

        pool.close()

    finally:
        pool.join()

    for result in results:
        output.append(
            result["message"]
        )

    output.append(
        f"Result order returned by Pool.map: {[result['order_id'] for result in results]}"
    )

    output.append(
        "Pool.map workflow finished"
    )

    return {
        "method": "process",
        "section": 8,
        "scenario": 1,
        "title": "Ordered Parallel Processing with Pool.map",
        "problem":
            "شرح مسئله:\n"
            "چند سفارش باید محاسبه شوند. هر سفارش زمان پردازش متفاوتی دارد، اما parent می‌خواهد خروجی‌ها را مطابق ترتیب ورودی دریافت کند، "
            "نه الزاماً مطابق ترتیب تمام شدن واقعی taskها.\n\n"
            "سؤال:\n"
            "چگونه می‌توان چند task را با multiprocessing.Pool به صورت موازی اجرا کرد و نتیجه‌ها را با همان ترتیب ورودی دریافت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Pool.map برای اجرای موازی taskها و حفظ ترتیب نتیجه‌ها",
        "output": output,
        "explanation":
            "در این سناریو parent یک Pool با دو worker process می‌سازد و لیست سفارش‌ها را به Pool.map می‌دهد. "
            "هر سفارش زمان اجرای متفاوتی دارد، اما map نتیجه‌ها را مطابق ترتیب input list برمی‌گرداند. "
            "پس حتی اگر یک سفارش زودتر تمام شود، جایگاه آن در خروجی map بر اساس ترتیب ورودی حفظ می‌شود. "
            "این رفتار برای زمانی مناسب است که ترتیب خروجی‌ها برای برنامه مهم است."
    }


def _process_file_job(file_task):
    file_name, delay, failure_message = file_task

    current_process = multiprocessing.current_process()

    time.sleep(delay)

    if failure_message is not None:
        raise ValueError(
            failure_message
        )

    return {
        "file_name": file_name,
        "message":
            f"File '{file_name}' processed successfully inside process name='{current_process.name}', PID={os.getpid()}, delay={delay}"
    }


def scenario_2():
    output = []

    file_tasks = [
        (
            "report.pdf",
            0.20,
            None
        ),
        (
            "image.png",
            0.15,
            None
        ),
        (
            "data.csv",
            0.10,
            "File 'data.csv' is corrupted"
        ),
        (
            "video.mp4",
            0.25,
            None
        ),
        (
            "backup.zip",
            0.12,
            "File format for 'backup.zip' is not supported"
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created a Pool with 2 worker processes"
    )

    output.append(
        "Parent submits file-processing jobs with Pool.apply_async"
    )

    pool = multiprocessing.Pool(
        processes=2
    )

    async_results = []

    for file_task in file_tasks:
        file_name = file_task[0]

        async_result = pool.apply_async(
            _process_file_job,
            args=(file_task,)
        )

        async_results.append(
            (file_name, async_result)
        )

        output.append(
            f"Parent submitted async job for file='{file_name}'"
        )

    pool.close()

    for file_name, async_result in async_results:
        try:
            result = async_result.get(
                timeout=2
            )

            output.append(
                f"Parent received success result: {result['message']}"
            )

        except Exception as error:
            output.append(
                f"Parent caught failure for file='{file_name}': {type(error).__name__}: {error}"
            )

    pool.join()

    output.append(
        "Parent joined the Pool after collecting async results"
    )

    output.append(
        "Pool.apply_async file-processing workflow finished"
    )

    return {
        "method": "process",
        "section": 8,
        "scenario": 2,
        "title": "Asynchronous File Processing with Per-Task Error Handling",
        "problem":
            "شرح مسئله:\n"
            "کاربر پنج فایل را برای پردازش ارسال کرده است. بعضی فایل‌ها سالم هستند، "
            "اما ممکن است یک فایل خراب باشد یا فرمت آن توسط سیستم پشتیبانی نشود. "
            "خرابی یک فایل نباید باعث متوقف‌شدن پردازش سایر فایل‌ها شود و parent باید "
            "نتیجه موفقیت یا خطای هر فایل را جداگانه بررسی کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با Pool.apply_async فایل‌ها را به‌صورت مستقل در یک "
            "Process Pool پردازش کرد و خطای هر فایل را هنگام دریافت نتیجه مدیریت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از apply_async، دریافت AsyncResult برای هر فایل، فراخوانی get "
            "و مدیریت جداگانه Exceptionهای ایجادشده در worker process",
        "output": output,
        "explanation":
            "در این سناریو parent پنج فایل را به صورت jobهای مستقل با apply_async "
            "به Process Pool ارسال می‌کند. apply_async برای هر فایل یک AsyncResult "
            "جداگانه برمی‌گرداند و parent همه این نتیجه‌های موقت را در یک لیست نگه "
            "می‌دارد. سپس parent روی هر AsyncResult متد get را فراخوانی می‌کند. "
            "اگر پردازش فایل موفق باشد، نتیجه به parent بازگردانده می‌شود. اگر worker "
            "هنگام پردازش فایل Exception ایجاد کرده باشد، همان Exception هنگام get "
            "در parent دوباره raise می‌شود و با try/except مدیریت می‌شود. بنابراین "
            "خراب‌بودن data.csv یا پشتیبانی‌نشدن backup.zip مانع پردازش موفق "
            "report.pdf، image.png و video.mp4 نمی‌شود."
    }


def _create_thumbnail_job(thumbnail_task):
    image_name, delay = thumbnail_task

    current_process = multiprocessing.current_process()

    time.sleep(delay)

    return {
        "image_name": image_name,
        "delay": delay,
        "message":
            f"Thumbnail for '{image_name}' finished inside process name='{current_process.name}', PID={os.getpid()}, delay={delay}"
    }


def scenario_3():
    output = []

    thumbnail_tasks = [
        ("hero-banner.jpg", 0.35),
        ("small-icon.png", 0.05),
        ("product-card.webp", 0.20),
        ("user-avatar.jpg", 0.10),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created a Pool with 3 worker processes"
    )

    output.append(
        "Parent sends thumbnail jobs to Pool.imap_unordered"
    )

    output.append(
        "Results will be yielded when each task finishes, not necessarily in input order"
    )

    pool = multiprocessing.Pool(
        processes=3
    )

    completed_images = []

    try:
        for result in pool.imap_unordered(
                _create_thumbnail_job,
                thumbnail_tasks
        ):
            completed_images.append(
                result["image_name"]
            )

            output.append(
                f"Parent received completed result: {result['message']}"
            )

        pool.close()

    finally:
        pool.join()

    output.append(
        f"Completion order received by parent: {completed_images}"
    )

    output.append(
        "Pool.imap_unordered workflow finished"
    )

    return {
        "method": "process",
        "section": 8,
        "scenario": 3,
        "title": "Completion-Order Results with Pool.imap_unordered",
        "problem":
            "شرح مسئله:\n"
            "چند تصویر باید thumbnail شوند. parent لازم ندارد خروجی‌ها حتماً مطابق ترتیب ورودی باشند؛ "
            "بلکه می‌خواهد هر نتیجه‌ای که زودتر آماده شد همان لحظه دریافت شود.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با Process Pool نتیجه taskها را به ترتیب پایان یافتن دریافت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از Pool.imap_unordered برای دریافت نتیجه‌ها بر اساس completion order",
        "output": output,
        "explanation":
            "در این سناریو parent از imap_unordered استفاده می‌کند. این متد نتیجه‌ها را الزاماً مطابق ترتیب input list برنمی‌گرداند؛ "
            "هر task که زودتر تمام شود، زودتر به parent yield می‌شود. "
            "برای همین تصویر small-icon.png که delay کمتری دارد معمولاً زودتر از تصویرهای سنگین‌تر در خروجی دیده می‌شود. "
            "این سناریو با Pool.map فرق دارد، چون map ترتیب ورودی را حفظ می‌کند، اما imap_unordered ترتیب completion را نشان می‌دهد."
    }