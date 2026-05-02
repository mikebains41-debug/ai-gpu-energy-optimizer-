#!/bin/bash
# Install Nsight Systems on RunPod
apt-get update
apt-get install -y nsight-systems
echo "Nsight installed. Run: nsys profile --trace=cuda python workload.py"
