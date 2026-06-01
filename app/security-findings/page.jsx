"use client";
import { useState } from "react";

const vramData = [
  { gpu: "A100 SXM", min: 457, max: 465, color: "#FF6B6B" },
  { gpu: "H100 SXM", min: 527, max: 527, color: "#4ECDC4" },
  { gpu: "H200 SXM", min: 529, max: 629, color: "#45B7D1" },
  { gpu: "B200 SXM", min: 628, max: 728, color: "#96CEB4" },
];

const ghostData = [
  { gpu: "A100 SXM", baseline: 65, ghost: 146 },
  { gpu: "H100 SXM", baseline: 70, ghost: 0 },
  { gpu: "H200 SXM", baseline: 79, ghost: 136 },
  { gpu: "B200 SXM", baseline: 144, ghost: 574 },
];

export default function SecurityFindings() {
  const [active, setActive] = useState(1);
  const maxVram = 800;
  const maxGhost = 650;

  return (
    <div style={{ background: "#0a0a0f", minHeight: "100vh", fontFamily: "monospace", color: "#e0e0e0", padding: 24 }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <div style={{ borderBottom: "1px solid #ff2244", paddingBottom: 16, marginBottom: 24 }}>
          <div style={{ color: "#ff2244", fontSize: 11, letterSpacing: 4 }}>CVE REQUEST 2048350 · MANMOHAN MIKE BAINS · 2026-05-31</div>
          <div style={{ fontSize: 22, fontWeight: "bold", color: "#fff", marginTop: 8 }}>AI GPU ENERGY OPTIMIZER</div>
          <div style={{ fontSize: 13, color: "#888", marginTop: 4 }}>Security Findings — 72+ Tests · 7 Architectures · 4 Cloud Platforms</div>
          <div style={{ fontSize: 11, color: "#555", marginTop: 4 }}>github.com/mikebains41-debug/ai-gpu-energy-optimizer-</div>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24 }}>
          {[1,2,3,4,5,6,7].map(n => (
            <button key={n} onClick={() => setActive(n)} style={{
              background: active === n ? "#ff2244" : "#1a1a2e",
              color: active === n ? "#fff" : "#888",
              border: `1px solid ${active === n ? "#ff2244" : "#333"}`,
              padding: "6px 14px", fontSize: 11, cursor: "pointer", borderRadius: 2,
            }}>FINDING {n}</button>
          ))}
        </div>

        {active === 1 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>VRAM Residual by Architecture</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>MB of previous tenant data left after graceful PyTorch exit</div>
            {vramData.map(d => (
              <div key={d.gpu} style={{ marginBottom: 16 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 12, color: "#ddd" }}>{d.gpu}</span>
                  <span style={{ fontSize: 12, fontWeight: "bold", color: "#ff2244" }}>{d.min}-{d.max} MB</span>
                </div>
                <div style={{ background: "#1a1a1a", height: 28, borderRadius: 2 }}>
                  <div style={{ background: d.color, height: 28, width: `${(d.max/maxVram)*100}%`, borderRadius: 2, display: "flex", alignItems: "center", paddingLeft: 8 }}>
                    <span style={{ fontSize: 10, color: "#000", fontWeight: "bold" }}>{d.max} MB</span>
                  </div>
                </div>
              </div>
            ))}
            <div style={{ marginTop: 16, padding: 12, background: "#111", border: "1px solid #ff224430", fontSize: 11, color: "#aaa" }}>
              ⚠ SIGKILL clears VRAM to 0 MB. Graceful del + empty_cache() does NOT. Root cause: PyTorch CUDA allocator.
            </div>
          </div>
        )}

        {active === 2 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>Cross-GPU Isolation Failure</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>H200 — GPU0 data leaked into GPU1 despite GPU1 running zero workload</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: 16, alignItems: "center" }}>
              <div style={{ border: "2px solid #ff2244", padding: 20, textAlign: "center", background: "#1a0a0a" }}>
                <div style={{ color: "#ff2244", fontSize: 11, letterSpacing: 2 }}>GPU 0</div>
                <div style={{ color: "#fff", marginTop: 8, fontSize: 13 }}>FP32 Compute @ 653W</div>
                <div style={{ color: "#888", fontSize: 11, marginTop: 8 }}>VRAM: 19,030 MB</div>
                <div style={{ color: "#ff2244", fontSize: 13, fontWeight: "bold", marginTop: 8 }}>Residual: 1,102 MB</div>
              </div>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: 32, color: "#ff8800" }}>→</div>
                <div style={{ fontSize: 10, color: "#ff8800", marginTop: 4 }}>528 MB</div>
                <div style={{ fontSize: 10, color: "#ff8800" }}>LEAKED</div>
              </div>
              <div style={{ border: "2px solid #ff8800", padding: 20, textAlign: "center", background: "#1a0f00" }}>
                <div style={{ color: "#ff8800", fontSize: 11, letterSpacing: 2 }}>GPU 1</div>
                <div style={{ color: "#fff", marginTop: 8, fontSize: 13 }}>ZERO WORKLOAD</div>
                <div style={{ color: "#888", fontSize: 11, marginTop: 8 }}>No compute ran</div>
                <div style={{ color: "#ff8800", fontSize: 13, fontWeight: "bold", marginTop: 8 }}>Residual: 528 MB</div>
              </div>
            </div>
            <div style={{ marginTop: 16, padding: 12, background: "#111", border: "1px solid #ff880030", fontSize: 11, color: "#aaa", textAlign: "center" }}>
              Total 1,630 MB across both GPUs · Process exits code 0 · NVML reports 0% throughout
            </div>
          </div>
        )}

        {active === 3 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>NVML Monitoring Blindness</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>NVML reports 0% while GPU contains active data and compute</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={{ background: "#111", border: "1px solid #00ccff30", padding: 16 }}>
                <div style={{ color: "#00ccff", fontSize: 11, letterSpacing: 2, marginBottom: 12 }}>NVML REPORTS</div>
                {["Baseline", "2,343 MB Loaded", "After Clear"].map(p => (
                  <div key={p} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: "1px solid #1a1a1a" }}>
                    <span style={{ fontSize: 12, color: "#888" }}>{p}</span>
                    <span style={{ fontSize: 14, fontWeight: "bold", color: "#00ccff" }}>0%</span>
                  </div>
                ))}
              </div>
              <div style={{ background: "#111", border: "1px solid #ff2244", padding: 16 }}>
                <div style={{ color: "#ff2244", fontSize: 11, letterSpacing: 2, marginBottom: 12 }}>REALITY AT 100Hz</div>
                {[["Baseline","1 MB · 63W"],["2,343 MB Loaded","2,343 MB · 85W"],["After Clear","423 MB · 85W"]].map(([p,v]) => (
                  <div key={p} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: "1px solid #1a1a1a" }}>
                    <span style={{ fontSize: 12, color: "#888" }}>{p}</span>
                    <span style={{ fontSize: 13, fontWeight: "bold", color: "#ff2244" }}>{v}</span>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ marginTop: 16, padding: 12, background: "#111", border: "1px solid #333" }}>
              <div style={{ fontSize: 11, color: "#888", marginBottom: 8 }}>TOOLS COMPLETELY BLIND</div>
              <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                {["DCGM","Prometheus","Datadog","CloudWatch","Grafana","New Relic"].map(t => (
                  <div key={t} style={{ padding: "4px 10px", background: "#1a1a1a", border: "1px solid #333", fontSize: 11, color: "#555" }}>{t} ✗</div>
                ))}
              </div>
            </div>
          </div>
        )}

        {active === 4 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>Ghost Power Spike</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>Power draw at 0% reported utilization after process exit</div>
            {ghostData.map(d => (
              <div key={d.gpu} style={{ marginBottom: 16 }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 12, color: "#ddd" }}>{d.gpu}</span>
                  <span style={{ fontSize: 12, color: "#888" }}>Base: {d.baseline}W · Ghost: <span style={{ color: d.ghost > 200 ? "#ff2244" : d.ghost > 0 ? "#ff8800" : "#00ff88", fontWeight: "bold" }}>{d.ghost}W</span></span>
                </div>
                <div style={{ background: "#1a1a1a", height: 24, borderRadius: 2, position: "relative" }}>
                  <div style={{ background: "#334", height: 24, width: `${(d.baseline/maxGhost)*100}%`, borderRadius: 2, position: "absolute" }} />
                  {d.ghost > 0 && <div style={{ background: "#ff2244", height: 24, width: `${(d.ghost/maxGhost)*100}%`, borderRadius: 2, position: "absolute", opacity: 0.8 }} />}
                </div>
              </div>
            ))}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 16 }}>
              <div style={{ background: "#111", border: "1px solid #ff224450", padding: 16, textAlign: "center" }}>
                <div style={{ fontSize: 11, color: "#888" }}>B200 GHOST SPIKE</div>
                <div style={{ fontSize: 28, fontWeight: "bold", color: "#ff2244", marginTop: 4 }}>549–574W</div>
                <div style={{ fontSize: 11, color: "#666", marginTop: 4 }}>at 0% NVML utilization</div>
              </div>
              <div style={{ background: "#111", border: "1px solid #33333350", padding: 16, textAlign: "center" }}>
                <div style={{ fontSize: 11, color: "#888" }}>EXCEEDS A100 BY</div>
                <div style={{ fontSize: 28, fontWeight: "bold", color: "#ff8800", marginTop: 4 }}>+217W</div>
                <div style={{ fontSize: 11, color: "#666", marginTop: 4 }}>A100 max was 357W</div>
              </div>
            </div>
          </div>
        )}

        {active === 5 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>Spectre / Meltdown Analogy</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>Same structural pattern — security controls at wrong layer</div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {[
                { title: "SPECTRE 2018", color: "#00ccff", bg: "#001a2a", rows: [["Security Layer","OS + Hypervisor"],["Vulnerability Layer","CPU Speculative Execution"],["Data Leaked","CPU Cache Data"],["Monitoring Blind","All tools"],["Mitigation","Hard process termination"]] },
                { title: "GPU VRAM 2026", color: "#ff2244", bg: "#1a0009", rows: [["Security Layer","Container + OS Isolation"],["Vulnerability Layer","PyTorch CUDA Allocator"],["Data Leaked","VRAM 457–728 MB"],["Monitoring Blind","NVML + everything on it"],["Mitigation","SIGKILL → kernel reclamation"]] },
              ].map(({ title, color, bg, rows }) => (
                <div key={title} style={{ background: bg, border: `1px solid ${color}40`, padding: 16 }}>
                  <div style={{ color, fontSize: 12, letterSpacing: 2, marginBottom: 16, fontWeight: "bold" }}>{title}</div>
                  {rows.map(([k, v]) => (
                    <div key={k} style={{ marginBottom: 12 }}>
                      <div style={{ fontSize: 10, color: "#555" }}>{k}</div>
                      <div style={{ fontSize: 12, color: "#ddd", marginTop: 2 }}>{v}</div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
            <div style={{ marginTop: 16, padding: 16, background: "#111", border: "1px solid #ff880030", fontSize: 12, color: "#aaa", lineHeight: 1.6 }}>
              <span style={{ color: "#ff8800", fontWeight: "bold" }}>Identical pattern:</span> Security controls operate at one layer. Vulnerability exists at a lower layer those controls never reach. Cloud providers believe they are protected. They are not.
            </div>
          </div>
        )}

        {active === 6 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>Regulatory Fine Exposure</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>Maximum fines for cloud providers failing to comply</div>
            {[
              ["EU AI Act — AWS $90B revenue", "$6.3B maximum fine", "#ff2244"],
              ["GDPR Articles 25+32 — Google $280B", "$11.2B maximum fine", "#ff8800"],
              ["EU Data Act 2025", "$10M+ per violation", "#ffcc00"],
              ["California SB 253", "$500K per year", "#00ccff"],
              ["SEC Climate Disclosure", "$10M per violation", "#00ff88"],
              ["Australia PUE 1.4 — July 2025", "$10M AUD per violation", "#aa88ff"],
            ].map(([law, fine, color]) => (
              <div key={law} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 14, marginBottom: 8, background: "#111", border: "1px solid #222" }}>
                <span style={{ fontSize: 12, color: "#888" }}>{law}</span>
                <span style={{ fontSize: 14, fontWeight: "bold", color }}>{fine}</span>
              </div>
            ))}
            <div style={{ marginTop: 12, padding: 12, background: "#111", border: "1px solid #ff224430", fontSize: 12, color: "#ff2244", fontWeight: "bold", textAlign: "center" }}>
              Combined maximum exposure for major cloud provider: $20 BILLION+
            </div>
          </div>
        )}

        {active === 7 && (
          <div>
            <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff", marginBottom: 4 }}>Valuation Model</div>
            <div style={{ fontSize: 12, color: "#888", marginBottom: 20 }}>AI GPU Energy Optimizer — revenue paths and acquisition value</div>
            {[
              ["Bug Bounties Now", "$50K–$500K", "#888"],
              ["SaaS Launch 6-12mo", "$10M–$100M", "#00ccff"],
              ["Nelson Partnership", "$5M–$50M revenue share", "#00ccff"],
              ["Compliance Vertical 12-24mo", "$50M–$300M", "#ff8800"],
              ["Acquisition 18-36mo", "$100M–$1B+", "#ff2244"],
            ].map(([path, value, color]) => (
              <div key={path} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 16, marginBottom: 8, background: "#111", border: "1px solid #222" }}>
                <span style={{ fontSize: 12, color: "#888" }}>{path}</span>
                <span style={{ fontSize: 14, fontWeight: "bold", color }}>{value}</span>
              </div>
            ))}
            <div style={{ padding: 20, background: "#0a1a0a", border: "1px solid #00ff8840", marginTop: 8, textAlign: "center" }}>
              <div style={{ fontSize: 11, color: "#888" }}>BASE CASE VALUATION</div>
              <div style={{ fontSize: 36, fontWeight: "bold", color: "#00ff88", marginTop: 8 }}>$180M</div>
              <div style={{ fontSize: 11, color: "#555", marginTop: 8 }}>Built on Samsung S25 Ultra · Duncan BC Canada</div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
