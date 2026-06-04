import threading
import time


def scenario_1():
    output = []
    rlock = threading.RLock()
    available_seats = ["A1", "A2", "A3"]

    def check_seat(seat_code):
        with rlock:
            output.append(
                f"Checking availability for seat {seat_code}"
            )

            return seat_code in available_seats

    def reserve_seat(seat_code):
        with rlock:
            output.append(
                f"Reservation process started for seat {seat_code}"
            )

            if check_seat(seat_code):
                available_seats.remove(seat_code)

                output.append(
                    f"Seat {seat_code} reserved successfully"
                )
            else:
                output.append(
                    f"Seat {seat_code} is not available"
                )

    thread = threading.Thread(
        target=reserve_seat,
        args=("A1",)
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 1,
        "title": "Cinema Seat Reservation with Nested Lock",
        "output": output,
        "explanation":
            "در این سناریو فرایند رزرو صندلی سینما خودش قفل را می‌گیرد و داخل آن تابع بررسی صندلی دوباره همان قفل را می‌گیرد. چون از RLock استفاده شده، همان thread می‌تواند چند بار قفل را دریافت کند و deadlock رخ نمی‌دهد."
    }


def scenario_2():
    output = []
    rlock = threading.RLock()
    available_seats = ["A1", "A2", "A3", "A4", "A5"]

    def reserve_next_seat(user_number):
        with rlock:
            output.append(
                f"User #{user_number} is trying to reserve a cinema seat"
            )

            time.sleep(0.2)

            if available_seats:
                seat = available_seats.pop(0)

                output.append(
                    f"User #{user_number} reserved seat {seat}"
                )
            else:
                output.append(
                    f"User #{user_number} could not reserve a seat"
                )

    threads = []

    for i in range(1, 9):
        thread = threading.Thread(
            target=reserve_next_seat,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"Remaining seats: {available_seats}"
    )

    return {
        "method": "thread",
        "section": 5,
        "scenario": 2,
        "title": "Concurrent Cinema Seat Reservation",
        "output": output,
        "explanation":
            "در این سناریو چند کاربر همزمان برای رزرو صندلی اقدام می‌کنند. RLock از لیست صندلی‌های باقی‌مانده محافظت می‌کند تا دو کاربر نتوانند یک صندلی یکسان را رزرو کنند."
    }


def scenario_3():
    output = []
    rlock = threading.RLock()
    available_seats = ["B1", "B2", "B3"]

    def print_ticket(user_number, seat_code):
        with rlock:
            output.append(
                f"Ticket printed for User #{user_number}, Seat {seat_code}"
            )

    def confirm_reservation(user_number, seat_code):
        with rlock:
            output.append(
                f"Reservation confirmed for User #{user_number}, Seat {seat_code}"
            )

            print_ticket(user_number, seat_code)

    def reserve_seat(user_number, seat_code):
        with rlock:
            output.append(
                f"User #{user_number} selected Seat {seat_code}"
            )

            if seat_code in available_seats:
                available_seats.remove(seat_code)

                confirm_reservation(user_number, seat_code)
            else:
                output.append(
                    f"Seat {seat_code} is already taken"
                )

    thread = threading.Thread(
        target=reserve_seat,
        args=(1, "B2")
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 3,
        "title": "Cinema Reservation with Multi-step Nested Operations",
        "output": output,
        "explanation":
            "در این سناریو رزرو صندلی شامل چند مرحله تو در تو است: انتخاب صندلی، تأیید رزرو و چاپ بلیت. همه این مراحل از همان RLock استفاده می‌کنند و چون قفل بازگشتی است، همان thread می‌تواند بدون deadlock وارد مراحل داخلی شود."
    }