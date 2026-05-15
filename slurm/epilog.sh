#!/bin/bash
# Slurm Epilog — GPU Energy Observability Platform
# Install: copy to /etc/slurm/epilog.sh on your cluster nodes

GPU_API="${GPU_OBSERVABILITY_API:-https://ai-gpu-brain-v3.onrender.com}"
API_KEY="${GPU_OBS_API_KEY:-test_key_123}"

curl -s -X POST "${GPU_API}/job/end" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d "{\"job_id\":\"${SLURM_JOB_ID}\"}" \
  > /dev/null 2>&1 || true

exit 0
