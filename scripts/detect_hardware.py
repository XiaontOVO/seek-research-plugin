#!/usr/bin/env python3
"""Hardware auto-detection for research projects. Detects CPU, GPU, RAM, and OS info."""

import json
import os
import platform
import sys
from datetime import datetime


def detect_cpu():
    """Detect CPU information."""
    info = {"brand": "unknown", "cores_physical": 1, "cores_logical": 1}
    try:
        if platform.system() == "Windows":
            info["brand"] = platform.processor()
            info["cores_logical"] = os.cpu_count() or 1
            info["cores_physical"] = info["cores_logical"] // 2 or 1
        elif platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        info["brand"] = line.split(":")[1].strip()
                        break
            info["cores_logical"] = os.cpu_count() or 1
            # Count physical cores via /proc/cpuinfo
            try:
                result = os.popen("lscpu | grep 'Core(s) per socket'").read()
                cores_per = int(result.split(":")[1].strip())
                sockets = int(os.popen("lscpu | grep 'Socket(s)'").read().split(":")[1].strip())
                info["cores_physical"] = cores_per * sockets
            except Exception:
                info["cores_physical"] = info["cores_logical"] // 2 or 1
        elif platform.system() == "Darwin":
            info["brand"] = os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
            info["cores_physical"] = int(os.popen("sysctl -n hw.physicalcpu").read().strip())
            info["cores_logical"] = int(os.popen("sysctl -n hw.logicalcpu").read().strip())
    except Exception:
        pass
    return info


def detect_gpu():
    """Detect GPU information."""
    gpus = []
    try:
        result = os.popen("nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null").read()
        if result.strip():
            for line in result.strip().split("\n"):
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 2:
                    gpus.append({"name": parts[0], "memory_mb": _parse_memory(parts[1])})
    except Exception:
        pass

    if not gpus and platform.system() == "Darwin":
        try:
            result = os.popen("system_profiler SPDisplaysDataType 2>/dev/null").read()
            if "Chipset Model" in result:
                for line in result.split("\n"):
                    if "Chipset Model" in line:
                        gpus.append({"name": line.split(":")[1].strip(), "memory_mb": 0})
        except Exception:
            pass

    return gpus


def detect_ram():
    """Detect total RAM in MB."""
    try:
        import psutil
        return psutil.virtual_memory().total // (1024 * 1024)
    except ImportError:
        pass

    try:
        if platform.system() == "Windows":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                ]
            ms = MEMORYSTATUSEX()
            ms.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            return ms.ullTotalPhys // (1024 * 1024)
        elif platform.system() == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        return int(line.split()[1]) // 1024
    except Exception:
        pass
    return 0


def _parse_memory(mem_str):
    """Parse GPU memory string to MB."""
    mem_str = mem_str.strip().lower()
    if "gib" in mem_str or "gb" in mem_str:
        return int(float(mem_str.replace("gib", "").replace("gb", "").strip()) * 1024)
    elif "mib" in mem_str or "mb" in mem_str:
        return int(float(mem_str.replace("mib", "").replace("mb", "").strip()))
    return 0


def detect_disk():
    """Detect available disk space in GB at working directory."""
    try:
        import shutil
        usage = shutil.disk_usage(".")
        return usage.free // (1024 * 1024 * 1024)
    except Exception:
        return 0


def main():
    profile = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version,
        "cpu": detect_cpu(),
        "gpu": detect_gpu(),
        "ram_mb": detect_ram(),
        "disk_free_gb": detect_disk(),
    }
    return profile


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
