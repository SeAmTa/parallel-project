# پروژه نهایی Parallel Processing

یک web application آموزشی مبتنی بر FastAPI برای نمایش و آموزش **Thread-Based Parallelism** و **Process-Based Parallelism** در Python.

این پروژه به‌عنوان final project درس Parallel Processing توسعه داده شده است. برنامه یک web interface و چند API endpoint ارائه می‌دهد تا چندین سناریوی parallel programming اجرا شوند. هر سناریو شامل problem description، execution output و توضیح آموزشی درباره دلیل تولید خروجی است.

## GitHub Repository

Repository:

```text
https://github.com/SeAmTa/parallel-project
```

Clone URL:

```text
https://github.com/SeAmTa/parallel-project.git
```

## Project Overview

این application دو دسته اصلی از parallel execution در Python را نمایش می‌دهد:

1. **Thread-Based Parallelism**
2. **Process-Based Parallelism**

کاربر می‌تواند موارد زیر را انتخاب کند:

- Parallelism method: `thread` یا `process`
- Section number
- Scenario number

بعد از اجرا، web page موارد زیر را نمایش می‌دهد:

- Scenario title
- Problem statement
- Runtime output
- Educational explanation

این پروژه همچنین REST API endpoints را برای تست مستقیم ارائه می‌دهد.

## Main Features

- FastAPI backend
- Web UI برای انتخاب scenario
- مثال‌های Thread-based با استفاده از Python `threading`
- مثال‌های Process-based با استفاده از Python `multiprocessing`
- Server-Sent Events برای streaming خروجی scenario در browser
- Dockerized application
- Nginx reverse proxy configuration
- آماده برای deployment روی Linux VPS

## Technologies Used

- Python 3.11
- FastAPI
- Uvicorn
- HTML
- CSS
- JavaScript
- Docker
- Docker Compose
- Nginx
- Git
- GitHub

## Project Structure

ساختار پروژه به شکل زیر سازمان‌دهی شده است:

```text
parallel-project/
│
│   .gitignore
│   .dockerignore
│   Dockerfile
│   docker-compose.yml
│   nginx.conf
│   README.md
│   requirements.txt
│
├── app/
│   │   __init__.py
│   │   main.py
│   │
│   ├── routes/
│   │   │   __init__.py
│   │   │   thread.py
│   │   │   process.py
│   │   │   stream.py
│   │
│   ├── services/
│   │   │   __init__.py
│   │   │   dispatcher.py
│   │   │
│   │   ├── thread/
│   │   │   │   defining_thread.py
│   │   │   │   current_thread.py
│   │   │   │   thread_subclass.py
│   │   │   │   lock_sync.py
│   │   │   │   rlock_sync.py
│   │   │   │   semaphore_sync.py
│   │   │   │   barrier_sync.py
│   │   │   │   event_sync.py
│   │   │   │   condition_sync.py
│   │   │   │   queue_sync.py
│   │   │
│   │   ├── process/
│   │   │   │   spawning_process.py
│   │   │   │   naming_process.py
│   │   │   │   background_process.py
│   │   │   │   killing_process.py
│   │   │   │   process_subclass.py
│   │   │   │   queue_exchange.py
│   │   │   │   process_sync.py
│   │   │   │   process_pool.py
│   │
│   ├── templates/
│   │   │   index.html
│
├── static/
│   │   style.css
```

## Application Architecture

این application از یک layered structure استفاده می‌کند:

- `app/main.py` برنامه FastAPI را ایجاد می‌کند، static files را mount می‌کند، routers را include می‌کند و main HTML page را سرو می‌کند.
- `app/routes/thread.py` API endpoints مربوط به thread-based scenarios را ارائه می‌دهد.
- `app/routes/process.py` API endpoints مربوط به process-based scenarios را ارائه می‌دهد.
- `app/routes/stream.py` قابلیت Server-Sent Events را برای streaming خروجی scenarioها به frontend فراهم می‌کند.
- `app/services/dispatcher.py` شماره section و scenario را به scenario function درست map می‌کند.
- `app/services/thread/` شامل همه مثال‌های thread-based است.
- `app/services/process/` شامل همه مثال‌های process-based است.
- `app/templates/index.html` شامل web interface است.
- `static/style.css` شامل UI styling است.
- `Dockerfile`، `docker-compose.yml` و `nginx.conf` برای containerized execution و reverse proxy configuration استفاده می‌شوند.

## API Endpoints

### Thread-Based API

```text
GET /api/thread/{section}/{scenario}
```

Example:

```text
http://127.0.0.1:8000/api/thread/1/1
```

### Process-Based API

```text
GET /api/process/{section}/{scenario}
```

Example:

```text
http://127.0.0.1:8000/api/process/8/3
```

### Streaming Endpoint

```text
GET /stream/{method}/{section}/{scenario}
```

Examples:

```text
/stream/thread/1/1
/stream/process/8/3
```

این streaming endpoint توسط web interface استفاده می‌شود تا خروجی scenario به‌صورت مرحله‌به‌مرحله نمایش داده شود.

## Output Format

هر scenario یک structured response مشابه نمونه زیر برمی‌گرداند:

```json
{
  "method": "thread",
  "section": 1,
  "scenario": 1,
  "title": "Scenario title",
  "problem": "Problem description",
  "output": [
    "Runtime output line 1",
    "Runtime output line 2"
  ],
  "explanation": "Educational explanation"
}
```

## Thread-Based Parallelism Sections

بخش thread-based شامل 10 section است. هر section دارای 3 scenario است. سناریوها طوری طراحی شده‌اند که از نظر فنی متفاوت باشند، نه اینکه فقط داستان آن‌ها فرق کند.

| Section | Topic | Scenario 1 | Scenario 2 | Scenario 3 |
|---:|---|---|---|---|
| 1 | Defining a Thread | چند thread مستقل برای سفارش‌های coffee | ترتیب پایان متفاوت با delayهای مختلف | استفاده فوری از join که رفتار را sequential می‌کند |
| 2 | Determining the Current Thread | ثبت نام current thread در log | رفتار متفاوت بر اساس thread name | تشخیص main/worker thread context |
| 3 | Defining a Thread Subclass | Thread subclass پایه | Subclass با persistent state | Multi-step workflow داخل subclass |
| 4 | Lock Synchronization | Race condition بدون Lock | اصلاح shared update با Lock | Central logging شبیه ATM با محافظت |
| 5 | RLock Synchronization | Nested lock acquisition | Multi-level workflow با nested calls | Recursive scanner با RLock |
| 6 | Semaphore Synchronization | محدودیت ظرفیت parking lot | محدودیت ظرفیت download server | Producer/consumer signaling |
| 7 | Barrier Synchronization | نقطه شروع مشترک | انتخاب coordinator با barrier return value | Multi-phase synchronization |
| 8 | Event Synchronization | One-to-many start signal | Graceful shutdown signal | Timeout و fallback behavior |
| 9 | Condition Synchronization | Single waiter notification | Multiple waiters با predicate | Custom bounded buffer |
| 10 | Queue Communication | FIFO producer/consumer | PriorityQueue processing | task_done و join با multiple workers |

### Thread Section Details

#### 1. Defining a Thread

این section ایجاد و اجرای basic threadها در Python را با استفاده از `threading.Thread` نمایش می‌دهد.

- Scenario 1 برای هر coffee order یک independent thread ایجاد می‌کند.
- Scenario 2 نشان می‌دهد که threadها ممکن است با ترتیبی متفاوت از ترتیب start شدنشان تمام شوند.
- Scenario 3 نشان می‌دهد که استفاده از `join()` بلافاصله بعد از هر `start()` می‌تواند execution را عملاً sequential کند.

#### 2. Determining the Current Thread

این section نشان می‌دهد که چطور می‌توان thread در حال اجرا را شناسایی کرد.

- Scenario 1 نام current thread را log می‌کند.
- Scenario 2 رفتار را بر اساس thread name تغییر می‌دهد.
- Scenario 3 تفاوت بین main application context و worker thread context را نشان می‌دهد.

#### 3. Defining a Thread Subclass

این section طراحی object-oriented thread را از طریق subclass کردن `threading.Thread` نمایش می‌دهد.

- Scenario 1 متد `run()` را override می‌کند.
- Scenario 2 state را داخل thread object ذخیره می‌کند و بعد از `join()` آن را می‌خواند.
- Scenario 3 یک multi-step workflow را با helper methods داخل subclass پیاده‌سازی می‌کند.

#### 4. Thread Synchronization with Lock

این section نشان می‌دهد که `Lock` چطور از دسترسی ناامن به shared data جلوگیری می‌کند.

- Scenario 1 عمداً یک race condition را نمایش می‌دهد.
- Scenario 2 مشکل shared update را با استفاده از `Lock` اصلاح می‌کند.
- Scenario 3 از چند shared resource مثل log numbering و log storage محافظت می‌کند.

#### 5. Thread Synchronization with RLock

این section مفهوم re-entrant locking را نمایش می‌دهد.

- Scenario 1 از nested functions استفاده می‌کند که همان lock را acquire می‌کنند.
- Scenario 2 از RLock در یک multi-level workflow استفاده می‌کند.
- Scenario 3 از RLock داخل یک recursive function استفاده می‌کند.

#### 6. Thread Synchronization with Semaphore

این section محدود کردن concurrent access به یک resource را نمایش می‌دهد.

- Scenario 1 دسترسی به parking را به دو car محدود می‌کند.
- Scenario 2 تعداد downloadهای هم‌زمان را محدود می‌کند.
- Scenario 3 از semaphore به‌عنوان signaling mechanism استفاده می‌کند.

#### 7. Thread Synchronization with Barrier

این section نشان می‌دهد چطور یک گروه از threadها تا رسیدن همه به یک نقطه مشترک منتظر می‌مانند.

- Scenario 1 همه workerها را بعد از آماده شدن همه آن‌ها start می‌کند.
- Scenario 2 از barrier return value برای انتخاب یک coordinator استفاده می‌کند.
- Scenario 3 workerها را در چند phase همگام‌سازی می‌کند.

#### 8. Thread Synchronization with Event

این section event-based signaling را نمایش می‌دهد.

- Scenario 1 از یک event برای start کردن چند worker استفاده می‌کند.
- Scenario 2 از یک event برای graceful shutdown استفاده می‌کند.
- Scenario 3 timeout behavior و fallback logic را نمایش می‌دهد.

#### 9. Thread Synchronization with Condition

این section condition variables را نمایش می‌دهد.

- Scenario 1 از `wait()` و `notify()` استفاده می‌کند.
- Scenario 2 از `wait_for()` و `notify_all()` استفاده می‌کند.
- Scenario 3 یک bounded buffer با full و empty conditions پیاده‌سازی می‌کند.

#### 10. Thread Communication with Queue

این section ارتباط امن بین threadها را نمایش می‌دهد.

- Scenario 1 از FIFO queue استفاده می‌کند.
- Scenario 2 از priority queue استفاده می‌کند.
- Scenario 3 از `task_done()` و `join()` برای track کردن تکمیل taskها استفاده می‌کند.

## Process-Based Parallelism Sections

بخش process-based شامل 8 section است. هر section دارای 3 scenario بر اساس Python `multiprocessing` است.

| Section | Topic | Scenario 1 | Scenario 2 | Scenario 3 |
|---:|---|---|---|---|
| 1 | Spawning a Process | یک child process و join | چند independent process | Memory isolation بین parent و child |
| 2 | Naming a Process | Default و custom process names | رفتار متفاوت بر اساس process name | Monitoring exit codes با process name |
| 3 | Background Process | Daemon background logger | Non-daemon finite process | Daemon process نمی‌تواند child ایجاد کند |
| 4 | Killing a Process | join(timeout) سپس terminate | Graceful stop با Event | Selective termination برای stuck process |
| 5 | Process Subclass | Process subclass پایه | State isolation در subclass | Workflow subclass با custom exit code |
| 6 | Queue Exchange | One-way parent-to-child Queue | Multiple producers و یک consumer | Bidirectional request/response queues |
| 7 | Process Synchronization | Value و Lock | Semaphore capacity limit | Event-based process start |
| 8 | Process Pool | Pool.map ordered results | apply_async با success/error handling | imap_unordered completion order |

### Process Section Details

#### 1. Spawning a Process

این section basic process creation را نمایش می‌دهد.

- Scenario 1 یک child process ایجاد می‌کند و با `join()` منتظر آن می‌ماند.
- Scenario 2 چند independent process را اجرا می‌کند.
- Scenario 3 نشان می‌دهد که parent و child processes حافظه معمولی را به‌صورت shared ندارند.

#### 2. Naming a Process

این section process names و process identity را نمایش می‌دهد.

- Scenario 1 default process names و custom process names را مقایسه می‌کند.
- Scenario 2 رفتار را بر اساس process name تغییر می‌دهد.
- Scenario 3 exit codes را برای named processes بررسی می‌کند.

#### 3. Background Process

این section daemon و non-daemon processes را نمایش می‌دهد.

- Scenario 1 یک daemon logger را در background اجرا می‌کند.
- Scenario 2 یک normal non-daemon process را اجرا می‌کند و منتظر completion می‌ماند.
- Scenario 3 نشان می‌دهد که یک daemon process نمی‌تواند child process ایجاد کند.

#### 4. Killing a Process

این section strategies مربوط به process termination را نمایش می‌دهد.

- Scenario 1 با timeout منتظر می‌ماند و سپس long-running process را terminate می‌کند.
- Scenario 2 از یک Event برای graceful process shutdown استفاده می‌کند.
- Scenario 3 فقط stuck process را از بین چند process terminate می‌کند.

#### 5. Process Subclass

این section subclass کردن `multiprocessing.Process` را نمایش می‌دهد.

- Scenario 1 متد `run()` را override می‌کند.
- Scenario 2 نشان می‌دهد که تغییرات state در child-side باعث update شدن parent object نمی‌شود.
- Scenario 3 از helper methods و یک custom exit code استفاده می‌کند.

#### 6. Queue Exchange Between Processes

این section inter-process communication را با استفاده از queues نمایش می‌دهد.

- Scenario 1 taskها را از parent به child با queue و sentinel value ارسال می‌کند.
- Scenario 2 از multiple producer processes و یک consumer process استفاده می‌کند.
- Scenario 3 از request و response queues برای two-way communication استفاده می‌کند.

#### 7. Process Synchronization

این section synchronization بین processها را نمایش می‌دهد.

- Scenario 1 از `multiprocessing.Value` همراه با `Lock` استفاده می‌کند.
- Scenario 2 از `Semaphore` برای محدود کردن concurrent process access استفاده می‌کند.
- Scenario 3 از `Event` استفاده می‌کند تا child processes بعد از start signal از طرف parent آزاد شوند.

#### 8. Process Pool

این section high-level worker pools را نمایش می‌دهد.

- Scenario 1 از `Pool.map()` استفاده می‌کند و ordered results را نشان می‌دهد.
- Scenario 2 از `Pool.apply_async()` استفاده می‌کند و success/error cases را مدیریت می‌کند.
- Scenario 3 از `Pool.imap_unordered()` استفاده می‌کند و completion-order results را نشان می‌دهد.

## Running the Project Locally Without Docker

ابتدا repository را clone کنید:

```bash
git clone https://github.com/SeAmTa/parallel-project.git
cd parallel-project
```

یک virtual environment ایجاد کنید:

```bash
python -m venv .venv
```

فعال‌سازی virtual environment در Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

dependencies را نصب کنید:

```bash
pip install -r requirements.txt
```

FastAPI application را اجرا کنید:

```bash
uvicorn app.main:app --reload
```

application را در browser باز کنید:

```text
http://127.0.0.1:8000
```

نمونه API endpoints:

```text
http://127.0.0.1:8000/api/thread/1/1
http://127.0.0.1:8000/api/process/8/3
```

## Running the Project with Docker and Nginx

این پروژه به‌صورت کامل Dockerized شده است. پروژه از دو container استفاده می‌کند:

1. FastAPI application container
2. Nginx reverse proxy container

برای build و run کردن پروژه:

```bash
docker compose up --build
```

بعد از اینکه containerها با موفقیت start شدند، آدرس زیر را باز کنید:

```text
http://127.0.0.1
```

برای stop کردن containerهای در حال اجرا، کلیدهای زیر را فشار دهید:

```text
CTRL + C
```

سپس containers و network را remove کنید:

```bash
docker compose down
```

## Docker Configuration

### Dockerfile

فایل `Dockerfile` از `python:3.11-slim` به‌عنوان base image استفاده می‌کند. این فایل project files را copy می‌کند، dependencies را از `requirements.txt` نصب می‌کند، port `8000` را expose می‌کند و FastAPI app را با Uvicorn اجرا می‌کند.

Main command داخل container:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### docker-compose.yml

Docker Compose configuration دو service تعریف می‌کند:

- `app`: FastAPI application را build و run می‌کند.
- `nginx`: یک Nginx container اجرا می‌کند و port `80` را به application forward می‌کند.

FastAPI service به‌صورت internal روی port `8000` expose شده است و Nginx ترافیک HTTP خارجی را روی port `80` دریافت می‌کند.

### nginx.conf

Nginx به‌عنوان reverse proxy پیکربندی شده است:

```text
Client Browser -> Nginx Container -> FastAPI Container
```

Nginx configuration درخواست‌ها را به آدرس زیر forward می‌کند:

```text
http://app:8000
```

گزینه‌های زیر برای streaming support اضافه شده‌اند:

```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 3600;
proxy_send_timeout 3600;
```

این settings مهم هستند، چون frontend از Server-Sent Events برای دریافت مرحله‌به‌مرحله خروجی scenario استفاده می‌کند.

## Testing

پروژه در سه سطح تست شده است:

### 1. Thread API Testing

همه thread-based scenarios تست شدند:

```text
10 sections × 3 scenarios = 30 scenarios
```

Result:

```text
30/30 OK
```

### 2. Process API Testing

همه process-based scenarios تست شدند:

```text
8 sections × 3 scenarios = 24 scenarios
```

Result:

```text
24/24 OK
```

### 3. Docker and Web UI Testing

پروژه با موفقیت با Docker Compose ساخته و اجرا شد.

Tested Docker command:

```bash
docker compose up --build
```

containerهای زیر ایجاد و start شدند:

```text
parallel_fastapi_app
parallel_nginx
```

Successful FastAPI log:

```text
Uvicorn running on http://0.0.0.0:8000
```

Successful Nginx log:

```text
Configuration complete; ready for start up
```

web interface در آدرس زیر تست شد:

```text
http://127.0.0.1
```

scenarioهای زیر با موفقیت از UI تست شدند:

```text
Thread-Based Parallelism -> Section 10 -> Scenario 1
Process-Based Parallelism -> Section 8 -> Scenario 3
```

API endpoints زیر نیز با موفقیت تست شدند:

```text
http://127.0.0.1/api/thread/1/1
http://127.0.0.1/api/process/8/3
```

## Notes About Encoding

هنگام تست JSON responses در Windows PowerShell، متن فارسی ممکن است با encoding نادرست نمایش داده شود. این موضوع مربوط به نحوه نمایش در PowerShell است و application error محسوب نمی‌شود. متن فارسی در browser و web interface به‌درستی نمایش داده می‌شود.
