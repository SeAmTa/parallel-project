# Parallel Processing Final Project

A FastAPI-based educational web application for demonstrating **Thread-Based Parallelism** and **Process-Based Parallelism** in Python.

This project was developed as a final project for the Parallel Processing course. It provides a web interface and API endpoints for running multiple parallel programming scenarios. Each scenario returns a problem description, execution output, and an explanation of why the output is produced.

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

The application demonstrates two major categories of parallel execution in Python:

1. **Thread-Based Parallelism**
2. **Process-Based Parallelism**

The user can select:

- Parallelism method: `thread` or `process`
- Section number
- Scenario number

After execution, the web page displays:

- Scenario title
- Problem statement
- Runtime output
- Educational explanation

The project also exposes REST API endpoints for direct testing.

## Main Features

- FastAPI backend
- Web UI for scenario selection
- Thread-based examples using Python `threading`
- Process-based examples using Python `multiprocessing`
- Server-Sent Events for streaming scenario output to the browser
- Dockerized application
- Nginx reverse proxy configuration
- Ready for deployment on a Linux VPS

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

The project is organized as follows:

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

The application uses a layered structure:

- `app/main.py` creates the FastAPI application, mounts static files, includes routers, and serves the main HTML page.
- `app/routes/thread.py` exposes API endpoints for thread-based scenarios.
- `app/routes/process.py` exposes API endpoints for process-based scenarios.
- `app/routes/stream.py` provides Server-Sent Events for streaming scenario outputs to the frontend.
- `app/services/dispatcher.py` maps section and scenario numbers to the correct scenario functions.
- `app/services/thread/` contains all thread-based examples.
- `app/services/process/` contains all process-based examples.
- `app/templates/index.html` contains the web interface.
- `static/style.css` contains the UI styling.
- `Dockerfile`, `docker-compose.yml`, and `nginx.conf` are used for containerized execution and reverse proxy configuration.

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

The streaming endpoint is used by the web interface to display the scenario output step by step.

## Output Format

Each scenario returns a structured response similar to this:

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

The thread-based part contains 10 sections. Each section has 3 scenarios. The scenarios are designed to be technically different, not only different in story.

| Section | Topic | Scenario 1 | Scenario 2 | Scenario 3 |
|---:|---|---|---|---|
| 1 | Defining a Thread | Multiple independent coffee order threads | Different completion order with different delays | Immediate join causing sequential behavior |
| 2 | Determining the Current Thread | Logging current thread name | Role-based behavior by thread name | Detecting main/worker thread context |
| 3 | Defining a Thread Subclass | Basic Thread subclass | Subclass with persistent state | Multi-step workflow inside subclass |
| 4 | Lock Synchronization | Race condition without Lock | Correct shared update with Lock | Protected ATM-style central logging |
| 5 | RLock Synchronization | Nested lock acquisition | Multi-level workflow with nested calls | Recursive scanner using RLock |
| 6 | Semaphore Synchronization | Parking lot capacity limit | Download server capacity limit | Producer/consumer signaling |
| 7 | Barrier Synchronization | Common start point | Coordinator selection by barrier return value | Multi-phase synchronization |
| 8 | Event Synchronization | One-to-many start signal | Graceful shutdown signal | Timeout and fallback behavior |
| 9 | Condition Synchronization | Single waiter notification | Multiple waiters with predicate | Custom bounded buffer |
| 10 | Queue Communication | FIFO producer/consumer | PriorityQueue processing | task_done and join with multiple workers |

### Thread Section Details

#### 1. Defining a Thread

This section demonstrates the basic creation and execution of Python threads using `threading.Thread`.

- Scenario 1 creates one independent thread for each coffee order.
- Scenario 2 shows that threads may finish in a different order from the order in which they were started.
- Scenario 3 shows that using `join()` immediately after each `start()` can make the execution effectively sequential.

#### 2. Determining the Current Thread

This section demonstrates how to identify the currently running thread.

- Scenario 1 logs the name of the current thread.
- Scenario 2 changes behavior based on the thread name.
- Scenario 3 shows the difference between the main application context and worker thread context.

#### 3. Defining a Thread Subclass

This section demonstrates object-oriented thread design by subclassing `threading.Thread`.

- Scenario 1 overrides the `run()` method.
- Scenario 2 stores state inside the thread object and reads it after `join()`.
- Scenario 3 implements a multi-step workflow using helper methods inside the subclass.

#### 4. Thread Synchronization with Lock

This section demonstrates how `Lock` prevents unsafe access to shared data.

- Scenario 1 intentionally shows a race condition.
- Scenario 2 fixes the shared update problem using `Lock`.
- Scenario 3 protects multiple shared resources such as log numbering and log storage.

#### 5. Thread Synchronization with RLock

This section demonstrates re-entrant locking.

- Scenario 1 uses nested functions that acquire the same lock.
- Scenario 2 applies RLock in a multi-level workflow.
- Scenario 3 uses RLock in a recursive function.

#### 6. Thread Synchronization with Semaphore

This section demonstrates limiting concurrent access to a resource.

- Scenario 1 limits parking access to two cars.
- Scenario 2 limits concurrent downloads.
- Scenario 3 uses a semaphore as a signaling mechanism.

#### 7. Thread Synchronization with Barrier

This section demonstrates waiting until a group of threads reaches the same point.

- Scenario 1 starts all workers after all of them are ready.
- Scenario 2 uses the barrier return value to select one coordinator.
- Scenario 3 synchronizes workers across multiple phases.

#### 8. Thread Synchronization with Event

This section demonstrates event-based signaling.

- Scenario 1 uses one event to start multiple workers.
- Scenario 2 uses an event for graceful shutdown.
- Scenario 3 uses timeout behavior and fallback logic.

#### 9. Thread Synchronization with Condition

This section demonstrates condition variables.

- Scenario 1 uses `wait()` and `notify()`.
- Scenario 2 uses `wait_for()` and `notify_all()`.
- Scenario 3 implements a bounded buffer with full and empty conditions.

#### 10. Thread Communication with Queue

This section demonstrates safe communication between threads.

- Scenario 1 uses a FIFO queue.
- Scenario 2 uses a priority queue.
- Scenario 3 uses `task_done()` and `join()` to track task completion.

## Process-Based Parallelism Sections

The process-based part contains 8 sections. Each section has 3 scenarios based on Python `multiprocessing`.

| Section | Topic | Scenario 1 | Scenario 2 | Scenario 3 |
|---:|---|---|---|---|
| 1 | Spawning a Process | One child process and join | Multiple independent processes | Memory isolation between parent and child |
| 2 | Naming a Process | Default and custom process names | Role-based behavior by process name | Monitoring exit codes by process name |
| 3 | Background Process | Daemon background logger | Non-daemon finite process | Daemon process cannot create child |
| 4 | Killing a Process | join(timeout) then terminate | Graceful stop with Event | Selective termination of stuck process |
| 5 | Process Subclass | Basic Process subclass | State isolation in subclass | Workflow subclass with custom exit code |
| 6 | Queue Exchange | One-way parent-to-child Queue | Multiple producers and one consumer | Bidirectional request/response queues |
| 7 | Process Synchronization | Value and Lock | Semaphore capacity limit | Barrier synchronization |
| 8 | Process Pool | Pool.map ordered results | apply_async with success/error handling | imap_unordered completion order |

### Process Section Details

#### 1. Spawning a Process

This section demonstrates basic process creation.

- Scenario 1 creates one child process and waits for it using `join()`.
- Scenario 2 runs multiple independent processes.
- Scenario 3 shows that parent and child processes do not share normal memory.

#### 2. Naming a Process

This section demonstrates process names and process identity.

- Scenario 1 compares default and custom process names.
- Scenario 2 changes behavior based on the process name.
- Scenario 3 monitors exit codes for named processes.

#### 3. Background Process

This section demonstrates daemon and non-daemon processes.

- Scenario 1 runs a daemon logger in the background.
- Scenario 2 runs a normal non-daemon process and waits for completion.
- Scenario 3 shows that a daemon process cannot create a child process.

#### 4. Killing a Process

This section demonstrates process termination strategies.

- Scenario 1 waits with timeout and then terminates a long-running process.
- Scenario 2 uses an Event for graceful process shutdown.
- Scenario 3 terminates only the stuck process among several processes.

#### 5. Process Subclass

This section demonstrates subclassing `multiprocessing.Process`.

- Scenario 1 overrides the `run()` method.
- Scenario 2 shows that child-side state changes do not update the parent object.
- Scenario 3 uses helper methods and a custom exit code.

#### 6. Queue Exchange Between Processes

This section demonstrates inter-process communication using queues.

- Scenario 1 sends tasks from parent to child using a queue and a sentinel value.
- Scenario 2 uses multiple producer processes and one consumer process.
- Scenario 3 uses request and response queues for two-way communication.

#### 7. Process Synchronization

This section demonstrates synchronization between processes.

- Scenario 1 uses `multiprocessing.Value` with `Lock`.
- Scenario 2 uses `Semaphore` to limit concurrent process access.
- Scenario 3 uses `multiprocessing.Barrier` to compare processes that wait at a synchronization point with processes that continue without a barrier.

#### 8. Process Pool

This section demonstrates high-level worker pools.

- Scenario 1 uses `Pool.map()` and shows ordered results.
- Scenario 2 uses `Pool.apply_async()` and handles success/error cases.
- Scenario 3 uses `Pool.imap_unordered()` and shows completion-order results.

## Running the Project Locally Without Docker

First, clone the repository:

```bash
git clone https://github.com/SeAmTa/parallel-project.git
cd parallel-project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Open the application in the browser:

```text
http://127.0.0.1:8000
```

Example API endpoints:

```text
http://127.0.0.1:8000/api/thread/1/1
http://127.0.0.1:8000/api/process/8/3
```

## Running the Project with Docker and Nginx

The project is fully Dockerized. It uses two containers:

1. FastAPI application container
2. Nginx reverse proxy container

Build and run the project:

```bash
docker compose up --build
```

After the containers start successfully, open:

```text
http://127.0.0.1
```

To stop the running containers, press:

```text
CTRL + C
```

Then remove the containers and network:

```bash
docker compose down
```

## Docker Configuration

### Dockerfile

The `Dockerfile` uses `python:3.11-slim` as the base image. It copies the project files, installs dependencies from `requirements.txt`, exposes port `8000`, and starts the FastAPI app with Uvicorn.

Main command inside the container:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### docker-compose.yml

The Docker Compose configuration defines two services:

- `app`: builds and runs the FastAPI application.
- `nginx`: runs an Nginx container and forwards port `80` to the application.

The FastAPI service is exposed internally on port `8000`, and Nginx receives external HTTP traffic on port `80`.

### nginx.conf

Nginx is configured as a reverse proxy:

```text
Client Browser -> Nginx Container -> FastAPI Container
```

The Nginx configuration forwards requests to:

```text
http://app:8000
```

The following options are included for streaming support:

```nginx
proxy_buffering off;
proxy_cache off;
proxy_read_timeout 3600;
proxy_send_timeout 3600;
```

These settings are important because the frontend uses Server-Sent Events to receive scenario output step by step.

## Testing

The project was tested in three levels:

### 1. Thread API Testing

All thread-based scenarios were tested:

```text
10 sections × 3 scenarios = 30 scenarios
```

Result:

```text
30/30 OK
```

### 2. Process API Testing

All process-based scenarios were tested:

```text
8 sections × 3 scenarios = 24 scenarios
```

Result:

```text
24/24 OK
```

### 3. Docker and Web UI Testing

The project was successfully built and executed using Docker Compose.

Tested Docker command:

```bash
docker compose up --build
```

The following containers were created and started:

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

The web interface was tested at:

```text
http://127.0.0.1
```

The following scenarios were tested successfully from the UI:

```text
Thread-Based Parallelism -> Section 10 -> Scenario 1
Process-Based Parallelism -> Section 8 -> Scenario 3
```

The following API endpoints were also tested successfully:

```text
http://127.0.0.1/api/thread/1/1
http://127.0.0.1/api/process/8/3
```

## Notes About Encoding

When testing JSON responses in Windows PowerShell, Persian text may appear incorrectly encoded. This is a PowerShell display issue and not an application error. The Persian text is displayed correctly in the browser and web interface.

