import threading
import time


def scenario_1():
    output = []

    class BaggageSortingLine(threading.Thread):

        def __init__(self, line_number, bag_count):
            super().__init__(name=f"Baggage-Line-Thread-{line_number}")
            self.line_number = line_number
            self.bag_count = bag_count

        def run(self):
            output.append(
                f"{self.name}: Sorting Line #{self.line_number} started processing {self.bag_count} baggage item(s)"
            )

            for bag_number in range(1, self.bag_count + 1):
                time.sleep(0.15)

                output.append(
                    f"{self.name}: sorted baggage #{bag_number}"
                )

            output.append(
                f"{self.name}: finished its baggage queue"
            )

    sorting_lines = [
        BaggageSortingLine(1, 3),
        BaggageSortingLine(2, 4),
        BaggageSortingLine(3, 2),
    ]

    for line in sorting_lines:
        line.start()

    for line in sorting_lines:
        line.join()

    output.append("Airport baggage sorting completed")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 1,
        "title": "Airport Baggage Sorting Lines as Thread Subclasses",
        "problem":
            "شرح مسئله:\n"
            "در فرودگاه چند خط تفکیک بار به صورت همزمان کار می‌کنند. "
            "هر خط تفکیک باید تعدادی چمدان را پردازش کند و رفتار مستقلی داشته باشد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان هر خط تفکیک بار را به صورت یک Thread مستقل با رفتار مخصوص خودش پیاده‌سازی کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ارث‌بری از threading.Thread و بازنویسی متد run",
        "output": output,
        "explanation":
            "در این سناریو هر خط تفکیک بار فرودگاه به صورت یک کلاس جدا از threading.Thread پیاده‌سازی شده است. "
            "رفتار هر خط داخل متد run نوشته شده و با start شدن شیء Thread، همان متد اجرا می‌شود. "
            "این سناریو مفهوم پایه‌ای ساخت Thread Subclass و بازنویسی run را نشان می‌دهد."
    }


def scenario_2():
    output = []

    class DeliveryVehicle(threading.Thread):

        def __init__(self, vehicle_id, packages):
            super().__init__(name=f"Delivery-Vehicle-Thread-{vehicle_id}")
            self.vehicle_id = vehicle_id
            self.packages = packages
            self.delivered_packages = 0
            self.failed_deliveries = 0

        def run(self):
            output.append(
                f"{self.name}: Vehicle #{self.vehicle_id} started route with {len(self.packages)} package(s)"
            )

            for package_code, should_deliver in self.packages:
                time.sleep(0.15)

                if should_deliver:
                    self.delivered_packages += 1

                    output.append(
                        f"{self.name}: delivered package {package_code}"
                    )
                else:
                    self.failed_deliveries += 1

                    output.append(
                        f"{self.name}: failed to deliver package {package_code}"
                    )

            output.append(
                f"{self.name}: summary delivered={self.delivered_packages}, failed={self.failed_deliveries}"
            )

    vehicles = [
        DeliveryVehicle(
            1,
            [
                ("A101", True),
                ("A102", False),
                ("A103", True),
            ]
        ),
        DeliveryVehicle(
            2,
            [
                ("B201", True),
                ("B202", True),
            ]
        ),
        DeliveryVehicle(
            3,
            [
                ("C301", False),
                ("C302", True),
                ("C303", True),
                ("C304", False),
            ]
        ),
    ]

    for vehicle in vehicles:
        vehicle.start()

    for vehicle in vehicles:
        vehicle.join()

    total_delivered = sum(
        vehicle.delivered_packages
        for vehicle in vehicles
    )

    total_failed = sum(
        vehicle.failed_deliveries
        for vehicle in vehicles
    )

    output.append(
        f"Final delivery report: delivered={total_delivered}, failed={total_failed}"
    )

    return {
        "method": "thread",
        "section": 3,
        "scenario": 2,
        "title": "Delivery Tracking System with Stateful Thread Objects",
        "problem":
            "شرح مسئله:\n"
            "در یک سامانه ارسال مرسوله، هر خودرو چند بسته متفاوت را تحویل می‌دهد و باید وضعیت مخصوص خودش مثل تعداد تحویل موفق و ناموفق را نگه دارد. "
            "بعد از پایان همه مسیرها، سیستم باید گزارش نهایی بسازد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان برای هر Thread علاوه بر اجرای وظیفه، وضعیت داخلی مستقل نیز نگه داشت و بعد از join از آن وضعیت استفاده کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "نگهداری State داخلی در کلاس‌های مشتق‌شده از Thread",
        "output": output,
        "explanation":
            "در این سناریو هر خودروی ارسال مرسوله یک Thread مستقل است و وضعیت داخلی خودش را نگه می‌دارد؛ مثل تعداد بسته‌های موفق و ناموفق. "
            "بعد از اینکه همه Threadها با join تمام شدند، برنامه اصلی مقدارهای داخلی هر Thread را می‌خواند و گزارش نهایی می‌سازد. "
            "این سناریو نشان می‌دهد Thread Subclass می‌تواند هم رفتار اجرایی و هم داده‌های داخلی مستقل داشته باشد."
    }


def scenario_3():
    output = []

    class ProductionLine(threading.Thread):

        def __init__(self, line_id, product_count):
            super().__init__(name=f"Production-Line-Thread-{line_id}")
            self.line_id = line_id
            self.product_count = product_count
            self.completed_products = 0

        def initialize_line(self):
            output.append(
                f"{self.name}: initialization started"
            )

            time.sleep(0.15)

            output.append(
                f"{self.name}: initialization completed"
            )

        def assemble_product(self, product_number):
            output.append(
                f"{self.name}: assembling product #{product_number}"
            )

            time.sleep(0.2)

            self.completed_products += 1

        def quality_check(self):
            output.append(
                f"{self.name}: quality check passed for {self.completed_products} product(s)"
            )

        def shutdown_line(self):
            output.append(
                f"{self.name}: shutdown completed"
            )

        def run(self):
            self.initialize_line()

            for product_number in range(1, self.product_count + 1):
                self.assemble_product(product_number)

            self.quality_check()
            self.shutdown_line()

    production_lines = [
        ProductionLine(1, 2),
        ProductionLine(2, 3),
        ProductionLine(3, 2),
    ]

    for line in production_lines:
        line.start()

    for line in production_lines:
        line.join()

    total_completed_products = sum(
        line.completed_products
        for line in production_lines
    )

    output.append(
        f"Smart factory production workflow completed with {total_completed_products} product(s)"
    )

    return {
        "method": "thread",
        "section": 3,
        "scenario": 3,
        "title": "Smart Factory Production Line with Helper Methods",
        "problem":
            "شرح مسئله:\n"
            "در یک کارخانه هوشمند، هر خط تولید فقط یک تابع ساده نیست؛ بلکه باید چند مرحله مانند راه‌اندازی، مونتاژ، کنترل کیفیت و خاموش‌سازی را انجام دهد. "
            "هر خط تولید باید این مراحل را مستقل از خط‌های دیگر اجرا کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان یک Thread سفارشی را به صورت شیءگرا طراحی کرد تا چند متد کمکی داخلی داشته باشد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "طراحی شیءگرای Thread با متدهای کمکی در کنار run",
        "output": output,
        "explanation":
            "در این سناریو هر خط تولید کارخانه هوشمند یک Thread سفارشی است. "
            "منطق کلاس فقط در متد run خلاصه نشده و متدهای کمکی initialize_line، assemble_product، quality_check و shutdown_line دارد. "
            "متد run ترتیب اجرای این مراحل را مشخص می‌کند. "
            "این سناریو نشان می‌دهد Thread Subclass برای طراحی شیءگرای وظایف پیچیده مناسب است."
    }