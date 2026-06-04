import threading
import time
import random


def scenario_1():
    output = []

    class BaggageSortingLine(threading.Thread):

        def __init__(self, line_number, bag_count):
            super().__init__()
            self.line_number = line_number
            self.bag_count = bag_count

        def run(self):
            output.append(
                f"Sorting Line #{self.line_number} started processing {self.bag_count} baggage item(s)"
            )

            for bag_number in range(1, self.bag_count + 1):
                time.sleep(0.15)

                output.append(
                    f"Sorting Line #{self.line_number} sorted baggage #{bag_number}"
                )

            output.append(
                f"Sorting Line #{self.line_number} finished its baggage queue"
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
            "در فرودگاه چند خط تفکیک بار به صورت همزمان کار می‌کنند. هر خط تفکیک باید تعدادی چمدان را پردازش کند و رفتار مستقلی داشته باشد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان هر خط تفکیک بار را به صورت یک Thread مستقل با رفتار مخصوص خودش پیاده‌سازی کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "ارث‌بری از threading.Thread و بازنویسی متد run",
        "output": output,
        "explanation":
            "در این سناریو هر خط تفکیک بار فرودگاه به صورت یک کلاس جدا از threading.Thread پیاده‌سازی شده است. با بازنویسی متد run، هر خط تفکیک هنگام start شدن وظیفه خودش را اجرا می‌کند. این سناریو مفهوم پایه‌ای ساخت Thread Subclass را نشان می‌دهد."
    }


def scenario_2():
    output = []

    class DeliveryVehicle(threading.Thread):

        def __init__(self, vehicle_id, packages):
            super().__init__()
            self.vehicle_id = vehicle_id
            self.packages = packages
            self.delivered_packages = 0
            self.failed_deliveries = 0

        def run(self):
            output.append(
                f"Vehicle #{self.vehicle_id} started route with {len(self.packages)} package(s)"
            )

            for package in self.packages:
                time.sleep(
                    random.uniform(0.1, 0.35)
                )

                delivered = random.choice([True, True, False])

                if delivered:
                    self.delivered_packages += 1

                    output.append(
                        f"Vehicle #{self.vehicle_id} delivered package {package}"
                    )
                else:
                    self.failed_deliveries += 1

                    output.append(
                        f"Vehicle #{self.vehicle_id} failed to deliver package {package}"
                    )

            output.append(
                f"Vehicle #{self.vehicle_id} summary: delivered={self.delivered_packages}, failed={self.failed_deliveries}"
            )

    vehicles = [
        DeliveryVehicle(1, ["A101", "A102", "A103"]),
        DeliveryVehicle(2, ["B201", "B202"]),
        DeliveryVehicle(3, ["C301", "C302", "C303", "C304"]),
    ]

    for vehicle in vehicles:
        vehicle.start()

    for vehicle in vehicles:
        vehicle.join()

    output.append("Delivery tracking finished for all vehicles")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 2,
        "title": "Delivery Tracking System with Stateful Thread Objects",
        "problem":
            "شرح مسئله:\n"
            "در یک سامانه ارسال مرسوله، هر خودرو چند بسته متفاوت را تحویل می‌دهد و باید وضعیت مخصوص خودش مثل تعداد تحویل موفق و ناموفق را نگه دارد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان برای هر Thread علاوه بر اجرای وظیفه، وضعیت داخلی مستقل نیز نگه داشت؟\n\n"
            "مفهوم مورد بررسی:\n"
            "نگهداری State داخلی در کلاس‌های مشتق‌شده از Thread",
        "output": output,
        "explanation":
            "در این سناریو هر خودروی ارسال مرسوله یک Thread مستقل است و وضعیت داخلی خودش را نگه می‌دارد؛ مثل تعداد بسته‌های موفق و ناموفق. این نشان می‌دهد وقتی از Thread Subclass استفاده می‌کنیم، هر Thread می‌تواند علاوه بر اجرای run، داده‌ها و state مخصوص خودش را داشته باشد."
    }


def scenario_3():
    output = []

    class ProductionLine(threading.Thread):

        def __init__(self, line_id, product_count):
            super().__init__()
            self.line_id = line_id
            self.product_count = product_count
            self.completed_products = 0

        def initialize_line(self):
            output.append(
                f"Production Line #{self.line_id}: initialization started"
            )

            time.sleep(0.15)

            output.append(
                f"Production Line #{self.line_id}: initialization completed"
            )

        def assemble_product(self, product_number):
            output.append(
                f"Production Line #{self.line_id}: assembling product #{product_number}"
            )

            time.sleep(0.2)

            self.completed_products += 1

        def quality_check(self):
            output.append(
                f"Production Line #{self.line_id}: quality check passed for {self.completed_products} product(s)"
            )

        def shutdown_line(self):
            output.append(
                f"Production Line #{self.line_id}: shutdown completed"
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

    output.append("Smart factory production workflow completed")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 3,
        "title": "Smart Factory Production Line with Helper Methods",
        "problem":
            "شرح مسئله:\n"
            "در یک کارخانه هوشمند، هر خط تولید فقط یک تابع ساده نیست؛ بلکه باید چند مرحله مانند راه‌اندازی، مونتاژ، کنترل کیفیت و خاموش‌سازی را انجام دهد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان یک Thread سفارشی را به صورت شیءگرا طراحی کرد تا چند متد کمکی داخلی داشته باشد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "طراحی شیءگرای Thread با متدهای کمکی در کنار run",
        "output": output,
        "explanation":
            "در این سناریو هر خط تولید کارخانه هوشمند یک Thread سفارشی است. منطق کلاس فقط در متد run خلاصه نشده و متدهای کمکی initialize_line، assemble_product، quality_check و shutdown_line دارد. این سناریو طراحی شیءگرای Threadها را نشان می‌دهد."
    }