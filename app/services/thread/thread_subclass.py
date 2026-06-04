import threading
import time
import os
import random


class WarehouseRobot(threading.Thread):

    def __init__(self, robot_number, task_name, delay, output):
        super().__init__()
        self.robot_number = robot_number
        self.task_name = task_name
        self.delay = delay
        self.output = output

    def run(self):
        self.output.append(
            f"Robot #{self.robot_number} started {self.task_name} in process ID {os.getpid()}"
        )

        time.sleep(self.delay)

        self.output.append(
            f"Robot #{self.robot_number} completed {self.task_name}"
        )


def scenario_1():
    output = []
    robots = []

    for i in range(1, 10):
        robot = WarehouseRobot(
            robot_number=i,
            task_name="moving a package",
            delay=0.4,
            output=output
        )

        robots.append(robot)
        robot.start()

    for robot in robots:
        robot.join()

    output.append("All warehouse robots finished their tasks")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 1,
        "title": "Warehouse Robots as Thread Subclasses",
        "output": output,
        "explanation":
            "در این سناریو هر ربات انبار به صورت یک کلاس مستقل از threading.Thread ساخته شده است. هر ربات متد run مخصوص خودش را اجرا می‌کند و همه ربات‌ها داخل یک process مشترک کار می‌کنند."
    }


def scenario_2():
    output = []
    robots = []

    tasks = [
        "moving a package",
        "scanning a barcode",
        "checking shelf inventory",
        "delivering a box",
        "sorting products",
        "charging station check",
        "loading a cart",
        "placing an item on shelf",
        "packing an order",
    ]

    for i in range(1, 10):
        delay = round(random.uniform(0.2, 1.0), 2)

        robot = WarehouseRobot(
            robot_number=i,
            task_name=tasks[i - 1],
            delay=delay,
            output=output
        )

        robots.append(robot)
        robot.start()

    for robot in robots:
        robot.join()

    output.append("Warehouse task queue completed")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 2,
        "title": "Warehouse Robots with Different Task Durations",
        "output": output,
        "explanation":
            "در این سناریو هر ربات وظیفه متفاوتی دارد و زمان انجام کارها یکسان نیست. چون ربات‌ها همزمان اجرا می‌شوند، ترتیب پایان کار آن‌ها به مدت زمان هر وظیفه بستگی دارد."
    }


def scenario_3():
    output = []

    for i in range(1, 10):
        robot = WarehouseRobot(
            robot_number=i,
            task_name="single-lane package handling",
            delay=0.2,
            output=output
        )

        robot.start()
        robot.join()

    output.append("Single-lane warehouse processing completed")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 3,
        "title": "Warehouse Robots in Single-lane Mode",
        "output": output,
        "explanation":
            "در این سناریو ربات‌ها هنوز با subclass از Thread ساخته شده‌اند، اما بعد از start هر ربات بلافاصله join اجرا می‌شود. بنابراین ربات بعدی تا پایان کار ربات قبلی شروع نمی‌شود و عملیات ترتیبی انجام می‌شود."
    }