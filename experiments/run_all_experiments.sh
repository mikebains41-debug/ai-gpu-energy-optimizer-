echo ""
echo "=== RUNNING FINAL PROOF TEST (Synchronized Nsight) ==="
nsys profile --trace=cuda,nvtx --output=final_proof python3 final_proof_test.py
