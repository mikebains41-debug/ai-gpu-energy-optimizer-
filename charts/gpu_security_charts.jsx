import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts";

const vramData = [
  { gpu: "A100 SXM", residual: 465 },
  { gpu: "H100 SXM", residual: 527 },
  { gpu: "H200 SXM", residual: 629 },
  { gpu: "B200 SXM", residual: 728 },
];

const ghostData = [
  { gpu: "A100 SXM", ghost: 146, baseline: 65 },
  { gpu: "H100 SXM", ghost: 0, baseline: 70 },
  { gpu: "H200 SXM", ghost: 136, baseline: 79 },
  { gpu: "B200 SXM", ghost: 574, baseline: 144 },
];

export default function GPUSecurityCharts() {
  const [active, setActive] = useState(1);
  const charts = [
    { id: 1, title: "VRAM Residual by Architecture" },
    { id: 2, title: "Cross-GPU Isolation Failure" },
    { id: 3, title: "NVML Blindness" },
    { id: 4, title: "Ghost Power Spike" },
    { id: 5, title: "Spectre Analogy" },
    { id: 6, title: "Financial Exposure" },
    { id: 7, title: "Valuation Model" },
  ];
  return (
    <div style={{ background: "#0a0a0f", minHeight: "100vh", fontFamily: "monospace", color: "#e0e0e0", padding: 24 }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        <div style={{ borderBottom: "1px solid #ff2244", paddingBottom: 16, marginBottom: 24 }}>
          <div style={{ color: "#ff2244", fontSize: 11, letterSpacing: 4 }}>CVE REQUEST 2048350 · MANMOHAN MIKE BAINS · 2026-05-31</div>
          <div style={{ fontSize: 22, fontWeight: "bold", color: "#fff", marginTop: 8 }}>AI GPU ENERGY OPTIMIZER</div>
          <div style={{ fontSize: 13, color: "#888", marginTop: 4 }}>Security Findings — 72+ Tests · 7 Architectures</div>
        </div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24 }}>
          {charts.map(c => (
            <button key={c.id} onClick={() => setActive(c.id)} style={{
              background: active === c.id ? "#ff2244" : "#1a1a2e",
              color: active === c.id ? "#fff" : "#888",
              border: "1px solid",
              borderColor: active === c.id ? "#ff2244" : "#333",
              padding: "6px 12px", fontSize: 11, cursor: "pointer",
            }}>FINDING {c.id}</button>
          ))}
        </div>
        <div style={{ fontSize: 18, fontWeight: "bold", color: "#fff", marginBottom: 8 }}>{charts[active-1].title}</div>
        {active === 1 && (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={vramData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="gpu" tick={{ fill: "#888", fontSize: 11 }} />
              <YAxis tick={{ fill: "#888", fontSize: 11 }} unit=" MB" />
              <Tooltip contentStyle={{ background: "#111", border: "1px solid #333", color: "#fff" }} />
              <Bar dataKey="residual" fill="#ff2244" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
        {active === 2 && (
          <div style={{ background: "#111", padding: 24, border: "1px solid #222" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: 20, alignItems: "center" }}>
              <div style={{ border: "2px solid #ff2244", padding: 20, textAlign: "center" }}>
                <div style={{ color: "#ff2244", fontSize: 11 }}>GPU 0</div>
                <div style={{ color: "#fff", marginTop: 8 }}>FP32 Compute 653W</div>
                <div style={{ color: "#888", fontSize: 11, marginTop: 8 }}>Residual: 1,102 MB</div>
              </div>
              <div style={{ textAlign: "center" }}>
                <div style={{ fontSize: 28, color: "#ff8800" }}>→</div>
                <div style={{ fontSize: 11, color: "#ff8800" }}>528 MB LEAKED</div>
              </div>
              <div style={{ border: "2px solid #ff8800", padding: 20, textAlign: "center" }}>
                <div style={{ color: "#ff8800", fontSize: 11 }}>GPU 1</div>
                <div style={{ color: "#fff", marginTop: 8 }}>ZERO WORKLOAD</div>
                <div style={{ color: "#ff8800", fontSize: 11, marginTop: 8 }}>Residual: 528 MB</div>
              </div>
            </div>
            <div style={{ marginTop: 16, textAlign: "center", color: "#666", fontSize: 12 }}>Total 1,630 MB across both GPUs · Exit code 0 · NVML reports 0%</div>
          </div>
        )}
        {active === 3 && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: "#111", border: "1px solid #222", padding: 16 }}>
              <div style={{ color: "#00ccff", fontSize: 11, marginBottom: 12 }}>NVML REPORTS</div>
              {["Baseline","Loaded 2343MB","After Clear"].map(p => (
                <div key={p} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #1a1a1a" }}>
                  <span style={{ fontSize: 11, color: "#888" }}>{p}</span>
                  <span style={{ fontWeight: "bold", color: "#00ccff" }}>0%</span>
                </div>
              ))}
            </div>
            <div style={{ background: "#111", border: "1px solid #ff2244", padding: 16 }}>
              <div style={{ color: "#ff2244", fontSize: 11, marginBottom: 12 }}>REALITY 100Hz</div>
              {[["Baseline","1 MB · 63W"],["Loaded","2,343 MB · 85W"],["After Clear","423 MB · 85W"]].map(([p,v]) => (
                <div key={p} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #1a1a1a" }}>
                  <span style={{ fontSize: 11, color: "#888" }}>{p}</span>
                  <span style={{ fontWeight: "bold", color: "#ff2244" }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        {active === 4 && (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={ghostData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#222" />
              <XAxis dataKey="gpu" tick={{ fill: "#888", fontSize: 11 }} />
              <YAxis tick={{ fill: "#888", fontSize: 11 }} unit="W" />
              <Tooltip contentStyle={{ background: "#111", border: "1px solid #333", color: "#fff" }} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <Bar dataKey="baseline" name="Baseline" fill="#334" radius={[2,2,0,0]} />
              <Bar dataKey="ghost" name="Ghost Spike" fill="#ff2244" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
        {active === 5 && (
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            {[
              { title: "SPECTRE 2018", color: "#00ccff", rows: [["Security","OS + Hypervisor"],["Vulnerability","CPU Speculative Exec"],["Data Leaked","CPU Cache"],["Blind","All tools"]] },
              { title: "GPU VRAM 2026", color: "#ff2244", rows: [["Security","Container + OS"],["Vulnerability","PyTorch CUDA Allocator"],["Data Leaked","VRAM 457-728 MB"],["Blind","NVML + all built on it"]] },
            ].map(({ title, color, rows }) => (
              <div key={title} style={{ background: "#111", border: `1px solid ${color}40`, padding: 16 }}>
                <div style={{ color, fontSize: 11, marginBottom: 16 }}>{title}</div>
                {rows.map(([k,v]) => (
                  <div key={k} style={{ marginBottom: 12 }}>
                    <div style={{ fontSize: 10, color: "#555" }}>{k}</div>
                    <div style={{ fontSize: 12, color: "#ddd" }}>{v}</div>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
        {active === 6 && (
          <div>
            {[
              ["EU AI Act — AWS $90B revenue","$6.3B maximum fine","#ff2244"],
              ["GDPR — Google $280B revenue","$11.2B maximum fine","#ff8800"],
              ["EU Data Act 2025","$10M+ per violation","#ffcc00"],
              ["California SB 253","$500K per year","#00ccff"],
            ].map(([law,fine,color]) => (
              <div key={law} style={{ display: "flex", justifyContent: "space-between", padding: 16, marginBottom: 8, background: "#111", border: "1px solid #222" }}>
                <span style={{ fontSize: 12, color: "#888" }}>{law}</span>
                <span style={{ fontSize: 14, fontWeight: "bold", color }}>{fine}</span>
              </div>
            ))}
          </div>
        )}
        {active === 7 && (
          <div>
            {[
              ["Bug Bounties Now","$50K–$500K","#888"],
              ["SaaS Launch 6-12mo","$10M–$100M","#00ccff"],
              ["Nelson Partnership","$5M–$50M revenue share","#00ccff"],
              ["Compliance Vertical","$50M–$300M","#ff8800"],
              ["Acquisition","$100M–$1B+","#ff2244"],
            ].map(([path,value,color]) => (
              <div key={path} style={{ display: "flex", justifyContent: "space-between", padding: 16, marginBottom: 8, background: "#111", border: "1px solid #222" }}>
                <span style={{ fontSize: 12, color: "#888" }}>{path}</span>
                <span style={{ fontSize: 14, fontWeight: "bold", color }}>{value}</span>
              </div>
            ))}
            <div style={{ padding: 16, background: "#0a1a0a", border: "1px solid #00ff8830", marginTop: 8 }}>
              <div style={{ fontSize: 11, color: "#888" }}>BASE CASE VALUATION</div>
              <div style={{ fontSize: 32, fontWeight: "bold", color: "#00ff88", marginTop: 4 }}>$180M</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
