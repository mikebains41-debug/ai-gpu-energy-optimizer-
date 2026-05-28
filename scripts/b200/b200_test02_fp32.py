import torch
import time
import subprocess
import datetime

MATRIX=4096
DURATION=900
d0=torch.device("cuda:0")
d1=torch.device("cuda:1")
total_flops=0
start=time.time()

print("="*60)
print("B200 TEST 02 FP32 LOAD TEST")
print("Researcher: Manmohan (Mike) Bains")
print(datetime.datetime.utcnow().isoformat())
print("="*60)
print("GPU0:",torch.cuda.get_device_name(0))
print("GPU1:",torch.cuda.get_device_name(1))
print("Matrix:",MATRIX,"x",MATRIX,"FP32")
print("Duration: 900s")
print("-"*60)

while time.time()-start<DURATION:
    e=time.time()-start
    a=torch.randn(MATRIX,MATRIX,device=d0)
    c=torch.matmul(a,torch.randn(MATRIX,MATRIX,device=d0))
    a=torch.randn(MATRIX,MATRIX,device=d1)
    c=torch.matmul(a,torch.randn(MATRIX,MATRIX,device=d1))
    torch.cuda.synchronize()
    total_flops+=2*(MATRIX**3)*2
    r=subprocess.run(["nvidia-smi","--query-gpu=timestamp,index,power.draw,power.limit,utilization.gpu,temperature.gpu,clocks.current.sm,clocks.current.memory,pstate,memory.used,memory.total","--format=csv,noheader"],capture_output=True,text=True)
    print("["+str(round(e))+"s | FLOPs:"+str(round(total_flops/1e12,3))+"T]")
    print(r.stdout.strip())
    time.sleep(10)

print("="*60)
print("COMPLETE",datetime.datetime.utcnow().isoformat())
print("TotalFLOPs:",round(total_flops/1e12,3),"TFLOPS")
print("CEI:",round(total_flops/2/((time.time()-start)*300)/1e9,3),"GFLOPS/J")
print("A100 reference: 5.68 GFLOPS/J")
print("="*60)
