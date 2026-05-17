# AI GPU Energy Optimizer

## 📊 Benchmark Contribution (Optional)

The GPU Energy Optimizer includes an opt-in telemetry sharing feature to build the CEI benchmark dataset. By enabling contribution, you help map systematic telemetry divergence across cloud providers and improve DESYNC/GHOST detection accuracy. All data is anonymized, aggregated, and used strictly for research and standardization. You retain full ownership of your raw metrics and may disable sharing at any time.

**Enable via Docker Compose:**
\`\`\`
CEI_TELEMETRY=true
\`\`\`

**What we collect:** GPU model, cloud provider, power draw, utilization, workload type, anonymized anomaly flags.

**What we NEVER collect:** Instance IDs, account names, job payloads, IP addresses, or API keys.

For data requests or enterprise DPA: privacy@ai-gpu-optimizer.com

*© 2026 Mike Bains. This notice is for informational purposes and does not constitute legal advice.*
