import threading
import time


def scenario_1():
    output = []
    rlock = threading.RLock()
    inventory = {
        "laptop": 1
    }

    def check_inventory(product_name):
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: check_inventory acquired the same RLock again"
            )

            available = inventory.get(product_name, 0) > 0

            output.append(
                f"{current_thread.name}: inventory for {product_name} is {inventory.get(product_name, 0)}"
            )

            return available

    def place_order(product_name):
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: place_order acquired RLock"
            )

            output.append(
                f"{current_thread.name}: calling check_inventory while still holding RLock"
            )

            if check_inventory(product_name):
                inventory[product_name] -= 1

                output.append(
                    f"{current_thread.name}: order placed successfully for {product_name}"
                )
            else:
                output.append(
                    f"{current_thread.name}: order failed because {product_name} is out of stock"
                )

            output.append(
                f"{current_thread.name}: place_order finished and will release RLock"
            )

    thread = threading.Thread(
        target=place_order,
        args=("laptop",),
        name="Order-Processing-Thread"
    )

    thread.start()
    thread.join()

    output.append(f"Final inventory: {inventory}")

    return {
        "method": "thread",
        "section": 5,
        "scenario": 1,
        "title": "Online Store Order Processing with Nested RLock",
        "problem":
            "شرح مسئله:\n"
            "در یک فروشگاه اینترنتی، تابع ثبت سفارش باید موجودی کالا را بررسی کند. "
            "خود تابع ثبت سفارش به قفل نیاز دارد و تابع بررسی موجودی نیز برای دسترسی به همان داده مشترک دوباره همان قفل را دریافت می‌کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان اجازه داد همان Thread در یک زنجیره فراخوانی تو در تو، چند بار همان قفل را دریافت کند بدون اینکه بن‌بست ایجاد شود؟\n\n"
            "مفهوم مورد بررسی:\n"
            "Nested Lock Acquisition با RLock",
        "output": output,
        "explanation":
            "در این سناریو تابع place_order ابتدا RLock را می‌گیرد. سپس در حالی که هنوز همان قفل را نگه داشته، تابع check_inventory را صدا می‌زند. "
            "تابع check_inventory هم دوباره همان RLock را می‌گیرد. اگر از Lock معمولی استفاده می‌شد، همان Thread هنگام ورود به تابع داخلی منتظر خودش می‌ماند و deadlock رخ می‌داد. "
            "اما RLock اجازه می‌دهد همان Thread چند بار یک قفل را به صورت تو در تو دریافت کند."
    }


def scenario_2():
    output = []
    rlock = threading.RLock()
    loan_request = {
        "documents_valid": True,
        "credit_score": 720,
        "approved": False
    }

    def approve_loan():
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: approve_loan acquired RLock at level 4"
            )

            loan_request["approved"] = True

            output.append(
                f"{current_thread.name}: loan request approved"
            )

    def calculate_score():
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: calculate_score acquired RLock at level 3"
            )

            time.sleep(0.15)

            if loan_request["credit_score"] >= 650:
                output.append(
                    f"{current_thread.name}: credit score {loan_request['credit_score']} is acceptable"
                )

                approve_loan()
            else:
                output.append(
                    f"{current_thread.name}: credit score is too low"
                )

    def validate_documents():
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: validate_documents acquired RLock at level 2"
            )

            time.sleep(0.15)

            if loan_request["documents_valid"]:
                output.append(
                    f"{current_thread.name}: documents are valid"
                )

                calculate_score()
            else:
                output.append(
                    f"{current_thread.name}: documents are invalid"
                )

    def process_loan():
        current_thread = threading.current_thread()

        with rlock:
            output.append(
                f"{current_thread.name}: process_loan acquired RLock at level 1"
            )

            validate_documents()

            output.append(
                f"{current_thread.name}: workflow finished with approved={loan_request['approved']}"
            )

    thread = threading.Thread(
        target=process_loan,
        name="Loan-Workflow-Thread"
    )

    thread.start()
    thread.join()

    output.append(f"Final loan request state: {loan_request}")

    return {
        "method": "thread",
        "section": 5,
        "scenario": 2,
        "title": "Loan Approval Workflow with Multi-level RLock",
        "problem":
            "شرح مسئله:\n"
            "در یک سامانه بررسی وام، پردازش درخواست شامل چند مرحله تو در تو است: بررسی مدارک، محاسبه امتیاز اعتباری و تأیید نهایی. "
            "همه این مراحل به داده مشترک درخواست وام دسترسی دارند و هر مرحله ممکن است همان قفل مشترک را دریافت کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان در یک workflow چندمرحله‌ای که توابع آن یکدیگر را صدا می‌زنند، از یک قفل مشترک بدون ایجاد بن‌بست استفاده کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "Multi-level Nested Locking با RLock",
        "output": output,
        "explanation":
            "در این سناریو یک workflow چندمرحله‌ای داریم. تابع process_loan قفل را می‌گیرد، سپس validate_documents را صدا می‌زند. "
            "داخل آن calculate_score و سپس approve_loan اجرا می‌شود. همه این توابع همان RLock را دریافت می‌کنند. "
            "چون همه فراخوانی‌ها در همان Thread انجام می‌شوند، RLock اجازه می‌دهد قفل در چند سطح مختلف دوباره گرفته شود. "
            "این رفتار برای workflowهای تو در تو مناسب است."
    }


def scenario_3():
    output = []
    rlock = threading.RLock()

    folder_tree = {
        "root": {
            "images": {
                "vacation": {},
                "profile": {}
            },
            "documents": {
                "university": {
                    "projects": {}
                }
            }
        }
    }

    def scan_folder(folder_name, children, depth=0):
        current_thread = threading.current_thread()
        indent = "  " * depth

        with rlock:
            output.append(
                f"{indent}{current_thread.name}: acquired RLock while scanning folder '{folder_name}' at depth {depth}"
            )

            time.sleep(0.1)

            for child_name, child_children in children.items():
                scan_folder(
                    child_name,
                    child_children,
                    depth + 1
                )

            output.append(
                f"{indent}{current_thread.name}: finished folder '{folder_name}' at depth {depth}"
            )

    thread = threading.Thread(
        target=scan_folder,
        args=("root", folder_tree["root"]),
        name="Recursive-Scanner-Thread"
    )

    thread.start()
    thread.join()

    output.append("Recursive folder scanning completed without deadlock")

    return {
        "method": "thread",
        "section": 5,
        "scenario": 3,
        "title": "Recursive Folder Scanner with RLock",
        "problem":
            "شرح مسئله:\n"
            "یک برنامه اسکن فایل باید پوشه‌های تو در تو را پیمایش کند. "
            "تابع اسکن پوشه به صورت بازگشتی خودش را برای پوشه‌های داخلی صدا می‌زند و در هر مرحله نیاز به قفل مشترک دارد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان در یک تابع بازگشتی، همان قفل را در چند سطح فراخوانی توسط همان Thread دوباره دریافت کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "Recursive Reentrant Locking با RLock",
        "output": output,
        "explanation":
            "در این سناریو تابع scan_folder به صورت بازگشتی پوشه‌های تو در تو را پیمایش می‌کند. "
            "هر بار که تابع برای یک پوشه داخلی دوباره صدا زده می‌شود، همان Thread دوباره همان RLock را دریافت می‌کند. "
            "اگر از Lock معمولی استفاده می‌شد، فراخوانی بازگشتی می‌توانست باعث deadlock شود، چون Thread برای گرفتن قفلی منتظر می‌ماند که خودش قبلاً گرفته است. "
            "RLock این مشکل را حل می‌کند و برای عملیات بازگشتی مناسب است."
    }