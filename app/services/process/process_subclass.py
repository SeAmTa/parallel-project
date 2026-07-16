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


class InvoiceExportProcess(multiprocessing.Process):
    def __init__(self, result_queue, invoice_count):
        super().__init__(
            name="Invoice-Export-Subclass-Process"
        )

        self.result_queue = result_queue
        self.invoice_count = invoice_count

    def run(self):
        current_process = multiprocessing.current_process()

        self.result_queue.put(
            f"{current_process.name} started with PID={os.getpid()}"
        )

        time.sleep(0.20)

        export_total = self.invoice_count * 125

        self.result_queue.put(
            f"{current_process.name} exported {self.invoice_count} invoices with total={export_total}"
        )

        self.result_queue.put(
            f"{current_process.name} finished run method"
        )


def scenario_1():
    output = []

    result_queue = multiprocessing.Queue()

    process = InvoiceExportProcess(
        result_queue=result_queue,
        invoice_count=4
    )

    output.append(
        f"Parent created custom Process subclass object with name='{process.name}'"
    )

    output.append(
        f"Parent process PID={os.getpid()} is about to start subclass process"
    )

    process.start()

    output.append(
        f"Parent started subclass process with PID={process.pid}"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=3
        )
    )

    output.append(
        f"Parent joined subclass process with exitcode={process.exitcode}"
    )

    return {
        "method": "process",
        "section": 5,
        "scenario": 1,
        "title": "Basic Process Subclass with Run Override",
        "problem":
            "شرح مسئله:\n"
            "یک برنامه باید عملیات export فاکتورها را داخل یک Process جداگانه اجرا کند، اما به جای دادن یک target function ساده، "
            "می‌خواهیم منطق اجرا داخل یک کلاس اختصاصی قرار بگیرد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان با subclass کردن multiprocessing.Process و override کردن متد run یک Process سفارشی ساخت؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ساخت Process subclass و قرار دادن منطق اجرای child process داخل متد run",
        "output": output,
        "explanation":
            "در این سناریو یک کلاس از multiprocessing.Process ارث‌بری می‌کند و متد run را override می‌کند. "
            "وقتی parent متد start را صدا می‌زند، Python یک Process جدید می‌سازد و متد run داخل child process اجرا می‌شود. "
            "این روش زمانی مفید است که بخواهیم منطق اجرای Process را به صورت شیءگرا و قابل توسعه داخل یک کلاس نگه داریم."
    }


class WarehouseCounterProcess(multiprocessing.Process):
    def __init__(self, result_queue, items):
        super().__init__(
            name="Warehouse-Counter-Subclass-Process"
        )

        self.result_queue = result_queue
        self.items = items
        self.accepted_count = 0
        self.rejected_count = 0

    def run(self):
        current_process = multiprocessing.current_process()

        self.result_queue.put(
            f"{current_process.name} started with PID={os.getpid()}"
        )

        self.result_queue.put(
            f"Child initial state: accepted_count={self.accepted_count}, rejected_count={self.rejected_count}"
        )

        for item in self.items:
            time.sleep(0.10)

            if item.startswith("damaged"):
                self.rejected_count += 1

                self.result_queue.put(
                    f"Child rejected item='{item}'. rejected_count={self.rejected_count}"
                )
            else:
                self.accepted_count += 1

                self.result_queue.put(
                    f"Child accepted item='{item}'. accepted_count={self.accepted_count}"
                )

        self.result_queue.put(
            f"Child final state: accepted_count={self.accepted_count}, rejected_count={self.rejected_count}"
        )


def scenario_2():
    output = []

    result_queue = multiprocessing.Queue()

    items = [
        "box-1",
        "damaged-box-2",
        "box-3",
        "damaged-box-4",
    ]

    process = WarehouseCounterProcess(
        result_queue=result_queue,
        items=items
    )

    output.append(
        f"Parent created process object with initial accepted_count={process.accepted_count}, rejected_count={process.rejected_count}"
    )

    process.start()

    output.append(
        f"Parent started process name='{process.name}' with PID={process.pid}"
    )

    process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=7
        )
    )

    output.append(
        f"Parent object after join still has accepted_count={process.accepted_count}, rejected_count={process.rejected_count}"
    )

    output.append(
        "Parent reads the real child result from Queue because normal object state is not shared between processes"
    )

    output.append(
        f"Warehouse counter process exitcode={process.exitcode}"
    )

    return {
        "method": "process",
        "section": 5,
        "scenario": 2,
        "title": "Process Subclass State Is Isolated from Parent",
        "problem":
            "شرح مسئله:\n"
            "یک Process subclass چند آیتم انبار را بررسی می‌کند و شمارنده‌های accepted و rejected را داخل خودش تغییر می‌دهد. "
            "بعد از پایان Process باید بررسی شود آیا این state تغییرکرده مستقیماً داخل object موجود در parent هم دیده می‌شود یا نه.\n\n"
            "سؤال:\n"
            "آیا تغییر attributeهای یک Process subclass داخل child process، object موجود در parent را هم تغییر می‌دهد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "جدایی حافظه در Process subclass و نیاز به Queue برای ارسال نتیجه از child به parent",
        "output": output,
        "explanation":
            "در این سناریو Process subclass دارای attributeهای accepted_count و rejected_count است. داخل child process این مقدارها تغییر می‌کنند، "
            "اما بعد از join، object موجود در parent هنوز مقدارهای اولیه را دارد. دلیلش این است که Processها حافظه جدا دارند و object داخل child یک کپی جداگانه است. "
            "برای همین نتیجه واقعی از طریق Queue به parent گزارش می‌شود. این سناریو با سناریوی اول فرق دارد، چون فقط ساخت subclass را نشان نمی‌دهد؛ "
            "بلکه رفتار state داخلی subclass در مدل multiprocessing را بررسی می‌کند."
    }


class ReportPipelineProcess(multiprocessing.Process):
    def __init__(self, result_queue, batch_name, should_fail):
        super().__init__(
            name=f"Report-Pipeline-{batch_name}"
        )

        self.result_queue = result_queue
        self.batch_name = batch_name
        self.should_fail = should_fail

    def _extract_data(self):
        time.sleep(0.10)

        self.result_queue.put(
            f"{self.name} extracted data for batch='{self.batch_name}'"
        )

    def _validate_data(self):
        time.sleep(0.10)

        if self.should_fail:
            self.result_queue.put(
                f"{self.name} validation failed for batch='{self.batch_name}'"
            )

            raise ValueError(
                f"Invalid records found in batch '{self.batch_name}'"
            )

        self.result_queue.put(
            f"{self.name} validation passed for batch='{self.batch_name}'"
        )

    def _generate_report(self):
        time.sleep(0.10)

        self.result_queue.put(
            f"{self.name} generated final report for batch='{self.batch_name}'"
        )

    def run(self):
        current_process = multiprocessing.current_process()

        self.result_queue.put(
            f"{current_process.name} started with PID={os.getpid()}"
        )

        try:
            self._extract_data()
            self._validate_data()
            self._generate_report()

            self.result_queue.put(
                f"{self.name} pipeline status=SUCCESS"
            )

        except ValueError as error:
            self.result_queue.put(
                f"{self.name} pipeline status=FAILED because {error}"
            )

            time.sleep(0.10)

            raise SystemExit(3)
        
        
def scenario_3():
    output = []

    result_queue = multiprocessing.Queue()

    processes = [
        ReportPipelineProcess(
            result_queue=result_queue,
            batch_name="Daily-Sales",
            should_fail=False
        ),
        ReportPipelineProcess(
            result_queue=result_queue,
            batch_name="Corrupted-Orders",
            should_fail=True
        ),
    ]

    output.append(
        f"Parent process PID={os.getpid()} created two pipeline process subclasses"
    )

    for process in processes:
        process.start()

        output.append(
            f"Parent started {process.name} with PID={process.pid}"
        )

    for process in processes:
        process.join()

    output.extend(
        _collect_queue_messages(
            result_queue,
            expected_count=9
        )
    )

    for process in processes:
        output.append(
            f"Pipeline process result: name='{process.name}', exitcode={process.exitcode}"
        )

    output.append(
        "Pipeline subclass workflow finished"
    )

    return {
        "method": "process",
        "section": 5,
        "scenario": 3,
        "title": "Process Subclass with Internal Workflow and Custom Exit Code",
        "problem":
            "شرح مسئله:\n"
            "دو pipeline پردازش گزارش در دو Process جداگانه اجرا می‌شوند. هر pipeline چند مرحله داخلی دارد: استخراج داده، اعتبارسنجی داده و تولید گزارش. "
            "یکی از pipelineها موفق است و دیگری در مرحله validation خطا می‌دهد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان داخل یک Process subclass، workflow چندمرحله‌ای و exitcode متفاوت برای success/failure پیاده‌سازی کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "طراحی Process subclass با متدهای داخلی، مدیریت خطا داخل run و تولید exitcode سفارشی",
        "output": output,
        "explanation":
            "در این سناریو Process subclass فقط یک run ساده ندارد؛ بلکه run چند helper method را صدا می‌زند. "
            "Pipeline موفق همه مراحل extract، validate و generate را انجام می‌دهد و با exitcode صفر تمام می‌شود. "
            "Pipeline خراب در مرحله validation خطا می‌دهد، خطا داخل run مدیریت می‌شود و سپس با SystemExit(3) خاتمه پیدا می‌کند. "
            "به همین دلیل parent بعد از join می‌تواند از روی exitcode بفهمد کدام pipeline موفق و کدام ناموفق بوده است. "
            "این سناریو با دو سناریوی قبلی فرق دارد، چون Process subclass را برای یک workflow چندمرحله‌ای و قابل مانیتورینگ استفاده می‌کند."
    }