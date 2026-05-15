#!/bin/bash
# Slurm Prolog — GPU Energy Observability Platform
# Install: copy to /etc/slurm/prolog.sh on your cluster nodes

GPU_API="${GPU_OBSERVABILITY_API:-https://ai-gpu-brain-v3.onrender.com}"
API_KEY="${GPU_OBS_API_KEY:-test_key_123}"
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1 || echo "unknown")

curl -s -X POST "${GPU_API}/job/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{\"job_id\":\"${SLURM_JOB_ID}\",\"user\":\"${SLURM_JOB_USER}\",\"nodes\":${SLURM_NNODES:-1},\"gpu_type\":\"${GPU_NAME}\"}" \
  > /dev/null 2>&1 || true

exit 0
