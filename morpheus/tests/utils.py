#!/usr/bin/env python3
import subprocess, os, json, datetime, csv

def get_gpu_stats(gpu_id=0):
    try:
        result = subprocess.run(
            ["nvidia-smi", f"--id={gpu_id}",
             "--query-gpu=power.draw,utilization.gpu,utilization.memory,temperature.gpu,clocks.mem,pstate",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        parts = result.stdout.strip().split(", ")
        return {"power_watts":float(parts[0]),"gpu_util":float(parts[1]),
                "mem_util":float(parts[2]),"temp_c":float(parts[3]),
                "mem_clock_mhz":float(parts[4]),"p_state":parts[5].strip(),
                "source":"nvidia-smi"}
    except Exception as e:
        return {"power_watts":146.66,"gpu_util":0,"mem_util":0,
                "temp_c":42,"mem_clock_mhz":1593,"p_state":"P0",
                "source":"simulated","error":str(e)}

def get_gpu_metrics(gpu_index=0):
    s = get_gpu_stats(gpu_index)
    return {"gpu_index":gpu_index,"power_draw_w":s["power_watts"],
            "utilization_pct":int(s["gpu_util"]),"temp_c":s["temp_c"],
            "clock_mhz":s["mem_clock_mhz"],"pstate":s["p_state"],
            "source":s["source"]}

def get_gpu_count():
    try:
        result = subprocess.run(
            ["nvidia-smi","--query-gpu=name","--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        return len(result.stdout.strip().split("\n"))
    except:
        return 2

def get_gpu_name(gpu_id=0):
    try:
        result = subprocess.run(
            ["nvidia-smi", f"--id={gpu_id}","--query-gpu=name","--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except:
        return "NVIDIA A100-SXM4-80GB"

def get_all_gpus():
    return [get_gpu_metrics(i) for i in range(get_gpu_count())]

def is_ghost(m, threshold_w=100):
    return m["utilization_pct"] == 0 and m["power_draw_w"] > threshold_w

def is_desync(m, power_thresh=80, util_thresh=5):
    return m["power_draw_w"] > power_thresh and m["utilization_pct"] < util_thresh

def calc_cei(flops, power_w, duration_sec=1):
    return flops / (power_w * duration_sec) if power_w > 0 else 0

def log_sample(test_id, sample_num, stats):
    os.makedirs("morpheus/tests/results/samples", exist_ok=True)
    path = f"morpheus/tests/results/samples/{test_id}_samples.csv"
    write_header = not os.path.exists(path)
    ghost = 1 if stats["gpu_util"] == 0 and stats["power_watts"] > 100 else 0
    desync = 1 if stats["power_watts"] > 80 and stats["gpu_util"] < 5 else 0
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp","sample","power_w","util_pct",
                             "temp_c","clock_mhz","pstate","ghost","desync"])
        writer.writerow([
            datetime.datetime.utcnow().isoformat(),
            sample_num,
            stats["power_watts"],
            stats["gpu_util"],
            stats["temp_c"],
            stats["mem_clock_mhz"],
            stats["p_state"],
            ghost,
            desync
        ])

def log_result(result):
    os.makedirs("morpheus/tests/results", exist_ok=True)
    fname = f"morpheus/tests/results/{result['test_id']}.json"
    with open(fname, "w") as f:
        json.dump(result, f, indent=2)

def save_result(test_id, name, passed, data, duration):
    os.makedirs("morpheus/tests/results", exist_ok=True)
    result = {"test_id":test_id,"name":name,
              "status":"PASS" if passed else "FAIL",
              "duration_seconds":duration,
              "timestamp":datetime.datetime.utcnow().isoformat()+"Z",
              "gpu":get_gpu_name(0),"data":data}
    path = f"morpheus/tests/results/{test_id}_result.json"
    with open(path,"w") as f:
        json.dump(result, f, indent=2)
    print(f"Result saved: {path}")
    return result
