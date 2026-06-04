import threading
import time


def scenario_1():
    return run_parking_scenario(
        scenario_number=1,
        parking_capacity=1
    )


def scenario_2():
    return run_parking_scenario(
        scenario_number=2,
        parking_capacity=2
    )


def scenario_3():
    return run_parking_scenario(
        scenario_number=3,
        parking_capacity=3
    )


def run_parking_scenario(scenario_number, parking_capacity):
    output = []
    parking_semaphore = threading.Semaphore(parking_capacity)

    def car_enter_parking(car_number):
        output.append(
            f"Car #{car_number} is waiting at the parking entrance"
        )

        with parking_semaphore:
            output.append(
                f"Car #{car_number} entered the parking lot"
            )

            time.sleep(0.5)

            output.append(
                f"Car #{car_number} left the parking lot"
            )

    threads = []

    for i in range(1, 10):
        thread = threading.Thread(
            target=car_enter_parking,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"Parking simulation finished with capacity {parking_capacity}"
    )

    return {
        "method": "thread",
        "section": 6,
        "scenario": scenario_number,
        "title": f"Limited Parking Lot with {parking_capacity} Available Spot(s)",
        "output": output,
        "explanation":
            f"در این سناریو پارکینگ فقط {parking_capacity} جای خالی دارد. Semaphore اجازه می‌دهد حداکثر {parking_capacity} ماشین همزمان وارد پارکینگ شوند و بقیه ماشین‌ها منتظر آزاد شدن ظرفیت می‌مانند."
    }