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
    output_lock = threading.Lock()

    order_lock = threading.RLock()

    inventory = {
        "laptop": 5
    }

    revenue = {
        "total": 0
    }

    approved_orders = []
    rejected_orders = []

    def log(message):
        with output_lock:
            output.append(message)

    def check_inventory(order_id, product, quantity):
        with order_lock:
            log(f"{order_id}: checking inventory for {quantity} {product}")

            available = inventory.get(product, 0)

            if available >= quantity:
                log(f"{order_id}: inventory is available")
                return True

            log(f"{order_id}: inventory is not enough")
            return False

    def reserve_inventory(order_id, product, quantity):
        with order_lock:
            log(f"{order_id}: reserving {quantity} {product}")

            inventory[product] -= quantity

            log(
                f"{order_id}: inventory after reservation = "
                f"{inventory[product]}"
            )

    def charge_customer(order_id, quantity):
        with order_lock:
            amount = quantity * 1000

            log(f"{order_id}: charging customer ${amount}")

            revenue["total"] += amount

            log(f"{order_id}: total revenue = ${revenue['total']}")

    def approve_order(order_id, product, quantity):
        with order_lock:
            log(f"{order_id}: order approval workflow started")

            if not check_inventory(order_id, product, quantity):
                rejected_orders.append(order_id)
                log(f"{order_id}: order rejected")
                return

            reserve_inventory(order_id, product, quantity)
            charge_customer(order_id, quantity)

            approved_orders.append(order_id)

            log(f"{order_id}: order approved")

    orders = [
        ("Order-1", "laptop", 2),
        ("Order-2", "laptop", 2),
        ("Order-3", "laptop", 2),
    ]

    threads = [
        threading.Thread(
            target=approve_order,
            args=(order_id, product, quantity),
            name=order_id
        )
        for order_id, product, quantity in orders
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Approved orders: {approved_orders}")
    output.append(f"Rejected orders: {rejected_orders}")
    output.append(f"Final inventory: {inventory}")
    output.append(f"Final revenue: ${revenue['total']}")

    return {
        "method": "thread",
        "section": 5,
        "scenario": 2,
        "title": "استفاده از RLock در یک تراکنش چندمرحله‌ای سفارش",
        "problem": (
            "یک فروشگاه آنلاین باید سفارش‌ها را به شکل امن تایید کند. تایید سفارش شامل "
            "چند مرحله است: بررسی موجودی، رزرو موجودی، و دریافت مبلغ از مشتری. همه این "
            "مراحل به داده‌های مشترک دسترسی دارند و باید به صورت هماهنگ اجرا شوند."
        ),
        "output": output,
        "explanation": (
            "در این سناریو از RLock برای اجرای یک تراکنش چندمرحله‌ای استفاده شده است. "
            "تابع approve_order() ابتدا RLock را می‌گیرد و سپس تابع‌های کمکی دیگری را صدا "
            "می‌زند که آن‌ها هم همان RLock را می‌گیرند. اگر به جای RLock از Lock معمولی "
            "استفاده شود، همان Thread هنگام گرفتن دوباره قفل ممکن است دچار بن‌بست شود. "
            "اما RLock اجازه می‌دهد همان Thread چند بار وارد ناحیه محافظت‌شده شود. تفاوت "
            "این سناریو با مثال ساده nested lock این است که چند Thread همزمان روی موجودی، "
            "درآمد و وضعیت سفارش‌ها کار می‌کنند."
        )
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
        indent = "│   " * depth

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