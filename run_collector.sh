#!/bin/bash
while true; do
  python3 gpu_collector.py
  echo "Collector crashed. Restarting..."
  sleep 2
done
