import threading
import time


def scenario_1():
    output = []

    def start_race():
        output.append(
            "Barrier action: all runners reached the start line. Race can begin!"
        )

    start_line_barrier = threading.Barrier(
        parties=3,
        action=start_race
    )

    runners = [
        ("Runner-Ali", 0.20),
        ("Runner-Reza", 0.45),
        ("Runner-Sara", 0.30),
    ]

    def runner_task(runner_name, warmup_time):
        output.append(
            f"{runner_name} is warming up for {warmup_time:.2f} seconds"
        )

        time.sleep(warmup_time)

        output.append(
            f"{runner_name} reached the start line and is waiting at the barrier"
        )

        start_line_barrier.wait()

        output.append(
            f"{runner_name} started running after the barrier was released"
        )

    threads = []

    for runner_name, warmup_time in runners:
        thread = threading.Thread(
            target=runner_task,
            args=(runner_name, warmup_time),
            name=f"{runner_name}-Thread"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("Race simulation finished")

    return {
        "method": "thread",
        "section": 7,
        "scenario": 1,
        "title": "Running Race Start Line with Barrier",
        "problem":
            "شرح مسئله:\n"
            "در یک مسابقه دو، چند دونده با زمان آماده‌سازی متفاوت به خط شروع می‌رسند. "
            "هیچ دونده‌ای نباید قبل از رسیدن همه شرکت‌کننده‌ها مسابقه را شروع کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان کاری کرد که همه Threadها در یک نقطه مشخص منتظر بمانند و فقط بعد از رسیدن همه، ادامه دهند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "هماهنگ‌سازی چند Thread با threading.Barrier",
        "output": output,
        "explanation":
            "در این سناریو هر دونده یک Thread جداگانه است. هر Thread بعد از warmup به خط شروع می‌رسد و روی Barrier منتظر می‌ماند. "
            "Barrier با parties=3 ساخته شده، یعنی تا زمانی که هر سه دونده به barrier نرسند، هیچ‌کدام اجازه ادامه ندارند. "
            "وقتی سومین Thread هم به Barrier برسد، action مربوط به Barrier اجرا می‌شود و سپس همه Threadها از نقطه انتظار عبور می‌کنند."
    }


def scenario_2():
    output = []

    startup_barrier = threading.Barrier(
        parties=3
    )

    services = [
        ("Database-Service", 0.50),
        ("Cache-Service", 0.25),
        ("Message-Broker-Service", 0.40),
    ]

    coordinator_result = {
        "service": None
    }

    coordinator_lock = threading.Lock()

    def initialize_service(service_name, startup_time):
        output.append(
            f"{service_name} initialization started"
        )

        time.sleep(startup_time)

        output.append(
            f"{service_name} is ready and waiting for other services at the barrier"
        )

        barrier_index = startup_barrier.wait()

        output.append(
            f"{service_name} passed startup barrier with barrier_index={barrier_index}"
        )

        if barrier_index == 0:
            with coordinator_lock:
                coordinator_result["service"] = service_name

                output.append(
                    f"{service_name} became startup coordinator after the barrier was released"
                )

                output.append(
                    f"{service_name} started the application because all dependencies are ready"
                )
        else:
            output.append(
                f"{service_name} continues as a normal service after startup synchronization"
            )

    threads = []

    for service_name, startup_time in services:
        thread = threading.Thread(
            target=initialize_service,
            args=(service_name, startup_time),
            name=f"{service_name}-Thread"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(
        f"Startup coordinator selected by barrier: {coordinator_result['service']}"
    )

    output.append("Application startup workflow finished")

    return {
        "method": "thread",
        "section": 7,
        "scenario": 2,
        "title": "Application Startup Coordinator Selected by Barrier",
        "problem":
            "شرح مسئله:\n"
            "یک برنامه برای شروع کامل به چند سرویس وابسته است: Database، Cache و Message Broker. "
            "هر سرویس زمان راه‌اندازی متفاوتی دارد و همه باید قبل از شروع برنامه آماده شوند. "
            "بعد از آماده شدن همه سرویس‌ها، فقط یکی از Threadها باید نقش coordinator را بگیرد و شروع برنامه را اعلام کند.\n\n"
            "سؤال:\n"
            "چگونه می‌توان بعد از رسیدن همه Threadها به Barrier، فقط یکی از آن‌ها را برای انجام یک کار یک‌باره انتخاب کرد؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از مقدار برگشتی barrier.wait برای انتخاب یک coordinator بعد از آزاد شدن Barrier",
        "output": output,
        "explanation":
            "در این سناریو هر سرویس در یک Thread جداگانه راه‌اندازی می‌شود و بعد از آماده شدن روی Barrier منتظر می‌ماند. "
            "وقتی هر سه سرویس به Barrier رسیدند، Barrier آزاد می‌شود. "
            "متد barrier.wait برای هر Thread یک عدد متفاوت برمی‌گرداند. "
            "در این سناریو Threadی که barrier_index برابر ۰ دریافت کند، نقش startup coordinator را می‌گیرد و فقط همان Thread شروع برنامه را اعلام می‌کند. "
            "بنابراین این سناریو علاوه بر هماهنگ‌سازی همه Threadها، انتخاب یک Thread خاص برای انجام کار یک‌باره بعد از Barrier را هم نشان می‌دهد."
    }


def scenario_3():
    output = []

    completed_phase_1 = []
    completed_phase_2 = []
    phase_lock = threading.Lock()

    def phase_1_completed():
        output.append(
            "Barrier action: all workers completed phase 1. Phase 2 can start."
        )

    def phase_2_completed():
        output.append(
            "Barrier action: all workers completed phase 2. Final merge can start."
        )

    phase_1_barrier = threading.Barrier(
        parties=4,
        action=phase_1_completed
    )

    phase_2_barrier = threading.Barrier(
        parties=4,
        action=phase_2_completed
    )

    workers = [
        ("Worker-1", 0.20, 0.35),
        ("Worker-2", 0.45, 0.20),
        ("Worker-3", 0.30, 0.40),
        ("Worker-4", 0.25, 0.25),
    ]

    def worker_task(worker_name, phase_1_time, phase_2_time):
        output.append(
            f"{worker_name} started phase 1"
        )

        time.sleep(phase_1_time)

        with phase_lock:
            completed_phase_1.append(worker_name)

        output.append(
            f"{worker_name} completed phase 1 and is waiting at phase 1 barrier"
        )

        phase_1_barrier.wait()

        output.append(
            f"{worker_name} started phase 2 after all workers completed phase 1"
        )

        time.sleep(phase_2_time)

        with phase_lock:
            completed_phase_2.append(worker_name)

        output.append(
            f"{worker_name} completed phase 2 and is waiting at phase 2 barrier"
        )

        phase_2_barrier.wait()

        output.append(
            f"{worker_name} entered final merge step"
        )

    threads = []

    for worker_name, phase_1_time, phase_2_time in workers:
        thread = threading.Thread(
            target=worker_task,
            args=(worker_name, phase_1_time, phase_2_time),
            name=f"{worker_name}-Thread"
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append(f"Workers completed phase 1: {completed_phase_1}")
    output.append(f"Workers completed phase 2: {completed_phase_2}")
    output.append("Multi-phase processing workflow finished")

    return {
        "method": "thread",
        "section": 7,
        "scenario": 3,
        "title": "Multi-phase Worker Processing with Barriers",
        "problem":
            "شرح مسئله:\n"
            "چند Worker باید یک کار چندمرحله‌ای را انجام دهند. همه Workerها باید مرحله اول را کامل کنند، "
            "بعد هیچ Workerی اجازه ندارد زودتر از بقیه وارد مرحله دوم شود. همین قانون برای ورود به مرحله نهایی هم وجود دارد.\n\n"
            "سؤال:\n"
            "چگونه می‌توان بین چند مرحله پردازش، نقطه‌های توقف مشترک ایجاد کرد تا همه Threadها مرحله قبل را کامل کرده باشند؟\n\n"
            "مفهوم مورد بررسی:\n"
            "استفاده از چند Barrier برای پردازش مرحله‌ای",
        "output": output,
        "explanation":
            "در این سناریو چهار Worker داریم و هر Worker دو مرحله پردازش انجام می‌دهد. "
            "بعد از پایان phase 1، همه Workerها روی phase_1_barrier منتظر می‌مانند. فقط وقتی هر چهار Worker مرحله اول را کامل کردند، مرحله دوم شروع می‌شود. "
            "بعد از phase 2 نیز همین کار با phase_2_barrier انجام می‌شود. "
            "این سناریو نشان می‌دهد Barrier فقط برای یک نقطه انتظار ساده نیست و می‌توان از آن برای هماهنگی چند مرحله پردازشی استفاده کرد."
    }