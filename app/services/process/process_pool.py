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
            f"{order_id} calculated total={total_price} inside process name='{current_process.name}', "
            f"PID={os.getpid()}, delay={delay}"
    }


def _generate_report_job(report_task):
    report_name, delay, should_fail = report_task

    current_process = multiprocessing.current_process()

    time.sleep(delay)

    if should_fail:
        raise ValueError(
            f"Report '{report_name}' contains invalid source data"
        )

    return {
        "report_name": report_name,
        "message":
            f"Report '{report_name}' generated successfully inside process name='{current_process.name}', "
            f"PID={os.getpid()}, delay={delay}"
    }


def _create_thumbnail_job(thumbnail_task):
    image_name, delay = thumbnail_task

    current_process = multiprocessing.current_process()

    time.sleep(delay)

    return {
        "image_name": image_name,
        "delay": delay,
        "message":
            f"Thumbnail for '{image_name}' finished inside process name='{current_process.name}', "
            f"PID={os.getpid()}, delay={delay}"
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


def scenario_2():
    output = []

    report_tasks = [
        ("Daily-Sales", 0.20, False),
        ("Corrupted-Inventory", 0.15, True),
        ("Customer-Summary", 0.10, False),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created a Pool with 2 worker processes"
    )

    output.append(
        "Parent submits report jobs with Pool.apply_async"
    )

    pool = multiprocessing.Pool(
        processes=2
    )

    async_results = []

    for report_task in report_tasks:
        report_name = report_task[0]

        async_result = pool.apply_async(
            _generate_report_job,
            args=(report_task,)
        )

        async_results.append(
            (report_name, async_result)
        )

        output.append(
            f"Parent submitted async job for report='{report_name}'"
        )

    pool.close()

    for report_name, async_result in async_results:
        try:
            result = async_result.get(
                timeout=2
            )

            output.append(
                f"Parent received success result: {result['message']}"
            )

        except Exception as error:
            output.append(
                f"Parent caught failure for report='{report_name}': {type(error).__name__}: {error}"
            )

    pool.join()

    output.append(
        "Parent joined the Pool after collecting async results"
    )

    output.append(
        "Pool.apply_async workflow finished"
    )

    return {
        "method": "process",
        "section": 8,
        "scenario": 2,
        "title": "Asynchronous Pool Jobs with Per-Task Error Handling",
        "problem":
            "شرح مسئله:\n"
            "چند گزارش باید در Process Pool اجرا شوند. بعضی jobها ممکن است موفق شوند و بعضی ممکن است خطا بدهند. "
            "parent باید بتواند نتیجه هر job را جداگانه بررسی کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با Pool.apply_async چند job مستقل را ارسال کرد و success/error هر job را جداگانه مدیریت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از apply_async، AsyncResult.get و مدیریت exceptionهای worker process",
        "output": output,
        "explanation":
            "در این سناریو parent هر job را با apply_async به Pool ارسال می‌کند. برخلاف map که کل لیست را یکجا برمی‌گرداند، "
            "apply_async برای هر job یک AsyncResult جدا می‌دهد. parent بعداً با get نتیجه هر job را می‌گیرد. "
            "اگر worker داخل Pool خطا بدهد، همان خطا هنگام get در parent دوباره raise می‌شود و parent می‌تواند آن را مدیریت کند. "
            "این سناریو با سناریوی اول فرق دارد، چون تمرکز آن روی ارسال async jobها و مدیریت خطای تک‌تک taskهاست."
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