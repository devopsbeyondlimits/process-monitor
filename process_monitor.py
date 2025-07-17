# Import FastAPI framework and dependencies
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import psutil

# Initialize FastAPI app with metadata
app = FastAPI(title="Process Monitor", description="Monitor and filter running processes on your Ubuntu instance.")

# Define the /processes endpoint for process monitoring and filtering
@app.get("/processes")
def get_processes(
    min_memory: Optional[float] = Query(None, description="Minimum memory usage in MB"),
    min_cpu: Optional[float] = Query(None, description="Minimum CPU percent usage (since process start)"),
    proc_name: Optional[str] = Query(None, description="Substring to match in process name")
):
    # List to hold filtered process info
    processes = []
    # Iterate over all running processes and collect info
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent', 'cmdline']):
        try:
            # Gather memory and CPU usage, process name
            mem_mb = proc.info['memory_info'].rss / 1024 / 1024 if proc.info['memory_info'] else 0
            cpu_percent = proc.cpu_percent(interval=0.1)  # short interval for up-to-date CPU
            name = proc.info['name'] or ''
            # Apply memory, CPU, and name filters if provided
            if min_memory is not None and mem_mb < min_memory:
                continue
            if min_cpu is not None and cpu_percent < min_cpu:
                continue
            if proc_name and proc_name.lower() not in name.lower():
                continue
            # Append process info to results if all filters pass
            processes.append({
                'pid': proc.info['pid'],
                'name': name,
                'username': proc.info['username'],
                'memory_mb': round(mem_mb, 2),
                'cpu_percent': cpu_percent,
                'cmdline': ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            })
        except Exception as e:
            # Return a 400 error for any kind of error during process iteration
            raise HTTPException(status_code=400, detail=f"Error retrieving process info: {str(e)}")
    # Return filtered process list and count
    return {"processes": processes, "count": len(processes)}

# To run: uvicorn process_monitor:app --host 0.0.0.0 --port 8000 