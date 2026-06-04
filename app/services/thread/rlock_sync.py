import threading
import time


def scenario_1():
    output = []
    rlock = threading.RLock()
    inventory = {
        "laptop": 1
    }

    def check_inventory(product_name):
        with rlock:
            output.append(
                f"Checking inventory for {product_name}"
            )

            return inventory.get(product_name, 0) > 0

    def place_order(product_name):
        with rlock:
            output.append(
                f"Order process started for {product_name}"
            )

            if check_inventory(product_name):
                inventory[product_name] -= 1

                output.append(
                    f"Order placed successfully for {product_name}"
                )
            else:
                output.append(
                    f"Order failed: {product_name} is out of stock"
                )

    thread = threading.Thread(
        target=place_order,
        args=("laptop",)
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 1,
        "title": "Online Store Order Processing with Nested RLock",
        "output": output,
        "explanation":
            "در این سناریو تابع place_order قفل را می‌گیرد و داخل آن تابع check_inventory دوباره همان قفل را دریافت می‌کند. اگر از Lock معمولی استفاده می‌شد، همان thread هنگام ورود به تابع داخلی منتظر خودش می‌ماند و deadlock رخ می‌داد. RLock اجازه می‌دهد همان thread چند بار یک قفل را بگیرد."
    }


def scenario_2():
    output = []
    rlock = threading.RLock()
    loan_requests = {
        "documents_valid": True,
        "credit_score": 720,
        "approved": False
    }

    def approve_loan():
        with rlock:
            output.append(
                "approve_loan: final approval step started"
            )

            loan_requests["approved"] = True

            output.append(
                "approve_loan: loan request approved"
            )

    def calculate_score():
        with rlock:
            output.append(
                "calculate_score: checking customer credit score"
            )

            time.sleep(0.2)

            if loan_requests["credit_score"] >= 650:
                output.append(
                    "calculate_score: credit score is acceptable"
                )

                approve_loan()
            else:
                output.append(
                    "calculate_score: credit score is too low"
                )

    def validate_documents():
        with rlock:
            output.append(
                "validate_documents: validating uploaded documents"
            )

            time.sleep(0.2)

            if loan_requests["documents_valid"]:
                output.append(
                    "validate_documents: documents are valid"
                )

                calculate_score()
            else:
                output.append(
                    "validate_documents: documents are invalid"
                )

    def process_loan():
        with rlock:
            output.append(
                "process_loan: loan workflow started"
            )

            validate_documents()

            output.append(
                "process_loan: workflow finished"
            )

    thread = threading.Thread(
        target=process_loan
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 2,
        "title": "Loan Approval Workflow with Multi-level RLock",
        "output": output,
        "explanation":
            "در این سناریو یک فرایند چندمرحله‌ای داریم: process_loan، validate_documents، calculate_score و approve_loan. همه این توابع روی داده مشترک درخواست وام کار می‌کنند و هرکدام همان RLock را می‌گیرند. این سناریو نشان می‌دهد RLock برای زنجیره فراخوانی‌های تو در تو مناسب است."
    }


def scenario_3():
    output = []
    rlock = threading.RLock()

    folder_tree = {
        "root": {
            "images": {
                "vacation": {}
            },
            "documents": {
                "university": {}
            }
        }
    }

    def scan_folder(folder_name, children, depth=0):
        with rlock:
            indent = "  " * depth

            output.append(
                f"{indent}Scanning folder: {folder_name}"
            )

            time.sleep(0.1)

            for child_name, child_children in children.items():
                scan_folder(
                    child_name,
                    child_children,
                    depth + 1
                )

            output.append(
                f"{indent}Finished folder: {folder_name}"
            )

    thread = threading.Thread(
        target=scan_folder,
        args=("root", folder_tree["root"])
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 3,
        "title": "Recursive Folder Scanner with RLock",
        "output": output,
        "explanation":
            "در این سناریو تابع scan_folder به صورت بازگشتی پوشه‌های تو در تو را پیمایش می‌کند. هر بار که تابع دوباره خودش را صدا می‌زند، همان thread دوباره همان RLock را دریافت می‌کند. این رفتار با RLock مجاز است و برای عملیات بازگشتی که به قفل مشترک نیاز دارند کاربرد دارد."
    }