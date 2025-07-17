# Process Monitor

**Process Monitor** is a lightweight, production-ready FastAPI application designed for real-time process monitoring on Linux servers (e.g., AWS EC2). It provides a secure, filterable REST API to inspect and analyze running processes, similar to a process explorer tool, enabling DevOps, SRE, and engineering leaders to automate system health checks and resource audits at scale.

## Features
- List all running processes with key attributes (PID, name, user, memory, CPU, command line)
- Filter processes by minimum memory usage, CPU consumption, or process name
- Simple, stateless REST API for integration with dashboards, automation, or monitoring tools

## Deployment (Ubuntu 24.04)

1. **Install prerequisites:**
   ```sh
   sudo apt update
   sudo apt install -y git python3 python3-pip python3.12-venv
   ```

2. **Clone the repository:**
   ```sh
   git clone https://github.com/devopsbeyondlimits/process-monitor.git
   cd process-monitor
   ```

3. **(Optional) Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Start the API server:**
   ```sh
   uvicorn process_monitor:app --host 0.0.0.0 --port 8080
   ```

## API Usage

### List All Processes
```
GET /processes
```
**Example:**
```
curl http://52.59.236.99:8080/processes
```

### Filter by Memory, CPU, or Name
```
GET /processes?min_memory=100&min_cpu=1&proc_name=python
```
- `min_memory`: Minimum memory usage in MB
- `min_cpu`: Minimum CPU percent usage
- `proc_name`: Substring to match in process name

**Example:**
```
curl "http://localhost:8080/processes?min_memory=200&min_cpu=0.5"
```

### Sample Response
```json
{
  "processes": [
      {
         "pid": 1234,
         "name": "python3",
         "username": "ubuntu",
         "memory_mb": 120.5,
         "cpu_percent": 2.3,
         "cmdline": "python3 myscript.py"
      },        
      {
         "pid": 656,
         "name": "networkd-dispat",
         "username": "root",
         "memory_mb": 20.12,
         "cpu_percent": 1.3,
         "cmdline": "/usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers"
      },
      {
         "pid": 663,
         "name": "snapd",
         "username": "root",
         "memory_mb": 35.73,
         "cpu_percent": 0.7,
         "cmdline": "/usr/lib/snapd/snapd"
      }
  ],
  "count": 1
}
```
