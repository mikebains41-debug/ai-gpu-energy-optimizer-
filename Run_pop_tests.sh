# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2026 Mike Bains. All Rights Reserved.
# Contact: Mikebains41@gmail.com
# Unauthorized use prohibited.

#!/bin/bash

echo "=========================================="
echo "H100 vs A100 Proof of Product Test Suite"
echo "=========================================="

# Run benchmark
python3 H100_benchmark.py

# Check if results were saved
if [ -f "pop_results.json" ]; then
    echo ""
    echo "Results saved to pop_results.json"
    cat pop_results.json
else
    echo "ERROR: Results file not created"
fi

echo ""
echo "Test complete"
