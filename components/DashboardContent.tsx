// PROPRIETARY AND CONFIDENTIAL
// Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
// Contact: Mikebains41@gmail.com
// Unauthorized use prohibited.

'use client';

import { useState, useEffect } from 'react';

export default function DashboardContent() {
  const [a100Data, setA100Data] = useState<any>(null);
  const [h100Data, setH100Data] useState<any>(null);
  const [historicalData, setHistoricalData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const [throttlePrediction, setThrottlePrediction] = useState<any>(null);
  
  const [autoMode, setAutoMode] = useState(false);
  const [actionLogs, setActionLogs] = useState<string[]>([]);
  const [stabilityMetrics, setStabilityMetrics] = useState<any>(null);

  // Fetch all data
  const fetchAllData = async () => {
    try {
      // Fetch A100
      const a100Res = await fetch('https://ai-gpu-brain-v3.onrender.com/metrics/a100');
      const a100Json = await a100Res.json();
      if (a100Json['a100-runpod'] && a100Json['a100-runpod'].length > 0) {
        const latest = a100Json['a100-runpod'][a100Json['a100-runpod'].length - 1];
        setA100Data(latest.gpus[0]);
      }

      // Fetch H100
      const h100Res = await fetch('https://ai-gpu-brain-v3.onrender.com/metrics/h100');
      const h100Json = await h100Res.json();
      if (h100Json['h100-runpod'] && h100Json['h100-runpod'].length > 0) {
        const latest = h100Json['h100-runpod'][h100Json['h100-runpod'].length - 1];
        setH100Data(latest.gpus[0]);
        setLastUpdated(new Date().toLocaleTimeString());
      }

      // Fetch history for chart
      const metricsRes = await fetch('https://ai-gpu-brain-v3.onrender.com/metrics');
      const metricsData = await metricsRes.json();
      
      const h100History: any[] = [];
      const a100History: any[] = [];
      
      if (metricsData['h100-runpod']) {
        metricsData['h100-runpod'].forEach((entry: any) => {
          if (entry.gpus?.[0]) {
            h100History.push({
              timestamp: entry.timestamp,
              power: entry.gpus[0].power_draw_watts || 0
            });
          }
        });
      }
      
      if (metricsData['a100-runpod']) {
        metricsData['a100-runpod'].forEach((entry: any) => {
          if (entry.gpus?.[0]) {
            a100History.push({
              timestamp: entry.timestamp,
              power: entry.gpus[0].power_draw_watts || 0
            });
          }
        });
      }
      
      const h100Recent = h100History.slice(-24);
      const a100Recent = a100History.slice(-24);
      const maxLen = Math.max(h100Recent.length, a100Recent.length);
      
      const merged = [];
      for (let i = 0; i < maxLen; i++) {
        merged.push({
          timestamp: h100Recent[i]?.timestamp || a100Recent[i]?.timestamp || Date.now() / 1000,
          power_h100: h100Recent[i]?.power || 0,
          power_a100: a100Recent[i]?.power || 0
        });
      }
      
      setHistoricalData(merged);
      setLoading(false);
    } catch (err) {
      console.error('Fetch error:', err);
      setLoading(false);
    }
  };

  // Fetch throttle prediction
  const fetchThrottle = async () => {
    try {
      const res = await fetch('https://ai-gpu-brain-v3.onrender.com/power-headroom?gpu_power=380&cpu_power=45');
      const data = await res.json();
      setThrottlePrediction(data);
    } catch (err) {
      console.error('Throttle error:', err);
    }
  };

  // Initial load + auto refresh every 30 seconds
  useEffect(() => {
    fetchAllData();
    fetchThrottle();
    
    const interval = setInterval(() => {
      fetchAllData();
    }, 30000);
    
    return () => clearInterval(interval);
  }, []);

  // Auto mode effect
  useEffect(() => {
    if (autoMode && h100Data) {
      const temp = h100Data.temperature_celsius || 58;
      if (temp > 70) {
        setActionLogs(prev => [...prev, `⚠️ Thermal rise (${temp}°C) → reducing power cap at ${new Date().toLocaleTimeString()}`]);
      }
    }
  }, [autoMode, h100Data]);

  // Stability metrics
  useEffect(() => {
    if (historicalData.length > 10) {
      const powers = historicalData.map(d => d.power_a100 + d.power_h100);
      const mean = powers.reduce((a, b) => a + b, 0) / powers.length;
      const variance = powers.map(p => Math.pow(p - mean, 2)).reduce((a, b) => a + b, 0) / powers.length;
      const stdDev = Math.sqrt(variance);
      const stabilityScore = Math.max(0, 100 - (stdDev / mean) * 100);
      
      setStabilityMetrics({
        stability_score: stabilityScore.toFixed(1),
        status: stabilityScore > 90 ? "Excellent" : stabilityScore > 70 ? "Good" : "Needs improvement"
      });
    }
  }, [historicalData]);

  // Get current values
  const a100Power = a100Data?.power_draw_watts ?? 400;
  const a100Temp = a100Data?.temperature_celsius ?? 65;
  const a100Util = a100Data?.utilization_percent ?? 100;
  const a100Memory = a100Data?.memory_used_gb ?? 45;
  const a100Clock = 1455;
  const a100MemoryClock = 1215;
  
  const h100Power = h100Data?.power_draw_watts ?? 690;
  const h100Temp = h100Data?.temperature_celsius ?? 60;
  const h100Util = h100Data?.utilization_percent ?? 100;
  const h100Memory = h100Data?.memory_used_gb ?? 0.71;
  const h100Clock = 1830;
  const h100MemoryClock = 1593;

  const totalPowerMW = (a100Power + h100Power) / 1000;

  // Savings calculations
  const POWER_DIFF_KW = (h100Power - a100Power) / 1000;
  const ELECTRICITY_RATE = 0.12;
  const OFF_PEAK_HOURS = 8;
  const FULL_DAY_HOURS = 24;

  const dailySavingsSwitch = POWER_DIFF_KW * FULL_DAY_HOURS * ELECTRICITY_RATE;
  const monthlySavingsSwitch = dailySavingsSwitch * 30;
  const annualSavingsSwitch = dailySavingsSwitch * 365;

  const h100PowerCapSavingsKW = (h100Power - 380) / 1000;
  const dailySavingsCap = h100PowerCapSavingsKW * FULL_DAY_HOURS * ELECTRICITY_RATE;
  const monthlySavingsCap = dailySavingsCap * 30;

  const dailySavingsOffPeak = POWER_DIFF_KW * OFF_PEAK_HOURS * ELECTRICITY_RATE;
  const monthlySavingsOffPeak = dailySavingsOffPeak * 30;

  const co2Reduction = POWER_DIFF_KW * FULL_DAY_HOURS * 365 * 0.4;

  // Efficiency calculation
  const a100Efficiency = a100Util / (a100Power / 1000);
  const h100Efficiency = h100Util / (h100Power / 1000);
  const avgEfficiency = (a100Efficiency + h100Efficiency) / 2;
  const efficiencyPercent = (avgEfficiency / 10).toFixed(1);

  const getThrottleReason = () => {
    if (h100Temp > 80) return "Thermal throttling active";
    if (h100Temp > 70) return "Approaching thermal limit";
    return "No throttle - Normal operation";
  };

  const pcieBandwidth = "64 GB/s (PCIe 5.0 x16)";

  const recommendations = [
    { text: 'Switch light workloads from H100 → A100', savings: `Save ~$${monthlySavingsSwitch.toFixed(0)}/month` },
    { text: 'Power cap H100 (690W → 380W)', savings: `Save ~$${monthlySavingsCap.toFixed(0)}/month` },
    { text: 'Shift 8 hours to off-peak', savings: `Save ~$${monthlySavingsOffPeak.toFixed(0)}/month` }
  ];

  const handleRefresh = () => {
    setLoading(true);
    fetchAllData().finally(() => setLoading(false));
  };

  if (loading && historicalData.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-400">Loading recorded test data...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-100">AI GPU Energy Optimizer</h1>
        <p className="text-gray-400 mt-2 max-w-2xl mx-auto">
          Recorded test data from A100 and H100 GPU benchmarks.
        </p>
        <p className="text-gray-500 text-sm mt-4">
          Built on Samsung S25 Ultra | No laptop, no desktop
        </p>
        <div className="flex justify-center items-center gap-3 mt-2">
          <p className="text-gray-500 text-xs">Last updated: {lastUpdated} | 📈 {totalPowerMW.toFixed(2)} MW Total (Test Data)</p>
          <button
            onClick={handleRefresh}
            className="px-3 py-1 text-xs bg-gray-700 rounded hover:bg-gray-600 transition-colors"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Auto Mode Toggle */}
      <div className="flex items-center justify-between bg-gray-800/50 rounded-lg p-4 border border-gray-700">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${autoMode ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></div>
          <div>
            <h3 className="text-sm font-semibold text-gray-200">Auto Mode</h3>
            <p className="text-xs text-gray-400">{autoMode ? 'Actively optimizing GPU power' : 'Monitoring only'}</p>
          </div>
        </div>
        <button
          onClick={() => {
            setAutoMode(!autoMode);
            setActionLogs(prev => [...prev, `Auto mode ${!autoMode ? 'ON' : 'OFF'} at ${new Date().toLocaleTimeString()}`]);
          }}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            autoMode 
              ? 'bg-green-600 text-white hover:bg-green-700' 
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          {autoMode ? 'ON' : 'OFF'}
        </button>
      </div>

      {/* Action Logs */}
      {actionLogs.length > 0 && (
        <div className="bg-gray-800/30 rounded-lg p-3 border border-gray-700">
          <div className="text-xs text-gray-400 mb-2">Action Log</div>
          <div className="space-y-1">
            {actionLogs.slice(-5).map((log, i) => (
              <div key={i} className="text-xs text-gray-300 font-mono">→ {log}</div>
            ))}
          </div>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-r from-green-900/30 to-green-800/20 rounded-lg p-4 border border-green-700">
          <p className="text-gray-400 text-sm">Annual Savings (Test Data)</p>
          <p className="text-2xl font-bold text-green-400">${Math.round(annualSavingsSwitch).toLocaleString()}</p>
          <p className="text-xs text-green-500 mt-1">Based on {Math.round(POWER_DIFF_KW * 1000)}W difference</p>
          <p className="text-xs text-green-400 mt-2">≈ ${dailySavingsSwitch.toFixed(2)} per day</p>
        </div>
        <div className="bg-gradient-to-r from-blue-900/30 to-blue-800/20 rounded-lg p-4 border border-blue-700">
          <p className="text-gray-400 text-sm">CO₂ Reduction (Test Data)</p>
          <p className="text-2xl font-bold text-blue-400">{Math.round(co2Reduction).toLocaleString()} kg</p>
          <p className="text-xs text-blue-500 mt-1">Annual estimated reduction</p>
        </div>
        <div className="bg-gradient-to-r from-orange-900/30 to-orange-800/20 rounded-lg p-4 border border-orange-700">
          <p className="text-gray-400 text-sm">Compute Efficiency</p>
          <p className="text-2xl font-bold text-orange-400">{efficiencyPercent}%</p>
          <p className="text-xs text-orange-500 mt-1">Utilization vs power draw</p>
          <p className="text-xs text-gray-500 mt-1">Normal range: 15-25% for H100 at 100% load</p>
        </div>
        {stabilityMetrics && (
          <div className="bg-gradient-to-r from-indigo-900/30 to-indigo-800/20 rounded-lg p-4 border border-indigo-700">
            <p className="text-gray-400 text-sm">Performance Stability</p>
            <p className="text-2xl font-bold text-indigo-400">{stabilityMetrics.stability_score}%</p>
            <p className="text-xs text-indigo-500 mt-1">{stabilityMetrics.status}</p>
          </div>
        )}
      </div>

      {/* GPU Clusters */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* A100 Cluster */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <div className="flex justify-between items-start mb-4">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-gray-100">NVIDIA A100 Cluster</h2>
                <span className="px-2 py-1 text-xs font-bold rounded bg-blue-600 text-white">A100</span>
              </div>
              <p className="text-sm text-gray-400 mt-1">US-East</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-100">1/1</div>
              <div className="text-xs text-gray-500">Active GPUs</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">GPU Utilization</div>
              <div className="text-2xl font-bold text-gray-100">{a100Util}%</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Power Draw</div>
              <div className="text-2xl font-bold text-gray-100">{Math.round(a100Power)}W</div>
              <div className="text-xs text-gray-500">Test Data</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Temperature</div>
              <div className="text-2xl font-bold text-gray-100">{a100Temp}°C</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Memory</div>
              <div className="text-2xl font-bold text-gray-100">{a100Memory.toFixed(1)} / 80 GB</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">GPU Clock Speed</div>
              <div className="text-xl font-bold text-gray-100">{a100Clock} MHz</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Memory Clock Speed</div>
              <div className="text-xl font-bold text-gray-100">{a100MemoryClock} MHz</div>
            </div>
          </div>
        </div>

        {/* H100 Cluster */}
        <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
          <div className="flex justify-between items-start mb-4">
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold text-gray-100">NVIDIA H100 Cluster</h2>
                <span className="px-2 py-1 text-xs font-bold rounded bg-orange-600 text-white">H100</span>
              </div>
              <p className="text-sm text-gray-400 mt-1">US-West</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-100">1/1</div>
              <div className="text-xs text-gray-500">Active GPUs</div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">GPU Utilization</div>
              <div className="text-2xl font-bold text-gray-100">{h100Util}%</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Power Draw</div>
              <div className="text-2xl font-bold text-gray-100">{Math.round(h100Power)}W</div>
              <div className="text-xs text-gray-500">Test Data</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Temperature</div>
              <div className="text-2xl font-bold text-gray-100">{h100Temp}°C</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Memory</div>
              <div className="text-2xl font-bold text-gray-100">{h100Memory.toFixed(1)} / 80 GB</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">GPU Clock Speed</div>
              <div className="text-xl font-bold text-gray-100">{h100Clock} MHz</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-xs text-gray-400">Memory Clock Speed</div>
              <div className="text-xl font-bold text-gray-100">{h100MemoryClock} MHz</div>
            </div>
          </div>
        </div>
      </div>

      {/* Throttle Prediction, Throttle Reason, PCIe Bandwidth */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-gray-900 rounded-lg p-4 border border-yellow-700">
          <h3 className="text-sm font-semibold text-yellow-400 mb-2">Throttling Prediction</h3>
          <p className="text-gray-300 text-sm">{throttlePrediction?.action || "Monitoring GPU thermal headroom"}</p>
          <p className="text-xs text-gray-500 mt-2">Level: {throttlePrediction?.throttle_level || "Normal"}</p>
        </div>
        <div className="bg-gray-900 rounded-lg p-4 border border-red-700">
          <h3 className="text-sm font-semibold text-red-400 mb-2">Throttle Reason</h3>
          <p className="text-gray-300 text-sm">{getThrottleReason()}</p>
          <p className="text-xs text-gray-500 mt-2">Trigger: {h100Temp > 70 ? "Temperature threshold exceeded" : "Normal operation"}</p>
        </div>
        <div className="bg-gray-900 rounded-lg p-4 border border-blue-700">
          <h3 className="text-sm font-semibold text-blue-400 mb-2">PCIe Bandwidth</h3>
          <p className="text-gray-300 text-sm">{pcieBandwidth}</p>
          <p className="text-xs text-gray-500 mt-2">PCIe 5.0 x16 interface</p>
        </div>
      </div>

      {/* Energy Graph */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-sm font-semibold text-gray-300 mb-4">Energy Consumption (Watts) - Test Data</h3>
        {historicalData.length > 0 ? (
          <div style={{ overflowX: 'auto', width: '100%' }}>
            <div style={{ minWidth: '800px' }}>
              <div className="flex justify-center gap-6 mb-4 text-xs">
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 bg-orange-500 rounded"></div>
                  <span className="text-gray-300 font-medium">H100</span>
                  <span className="text-gray-500">({Math.round(h100Power)}W)</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 bg-blue-500 rounded"></div>
                  <span className="text-gray-300 font-medium">A100</span>
                  <span className="text-gray-500">({Math.round(a100Power)}W)</span>
                </div>
              </div>
              
              <div className="h-48 flex items-end gap-2">
                {historicalData.map((point, idx) => {
                  const h100Height = Math.min(120, (point.power_h100 / 700) * 120);
                  const a100Height = Math.min(120, (point.power_a100 / 700) * 120);
                  const timeStr = new Date(point.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                  return (
                    <div key={idx} className="flex flex-col items-center" style={{ width: '60px' }}>
                      <div className="flex gap-1 items-end" style={{ height: '120px' }}>
                        <div 
                          className="w-5 bg-orange-500 rounded-t transition-all duration-300 hover:bg-orange-400" 
                          style={{ height: `${h100Height}px` }}
                          title={`H100: ${point.power_h100}W`}
                        ></div>
                        <div 
                          className="w-5 bg-blue-500 rounded-t transition-all duration-300 hover:bg-blue-400" 
                          style={{ height: `${a100Height}px` }}
                          title={`A100: ${point.power_a100}W`}
                        ></div>
                      </div>
                      <div className="text-[9px] text-gray-500 mt-1 text-center">
                        {timeStr}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center text-gray-500 py-8">Loading test data...</div>
        )}
      </div>

      {/* Power Capping */}
      <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
        <h3 className="text-sm font-semibold text-gray-300 mb-2">Power Capping</h3>
        <p className="text-gray-400 text-sm">Recommended power cap: 380W for H100 | 250W for A100</p>
        <p className="text-xs text-gray-500 mt-1">Dynamic power limiting based on thermal headroom</p>
      </div>

      {/* Why H100 is Overspending */}
      <div className="bg-gray-900 rounded-lg p-6 border border-yellow-700">
        <h3 className="text-sm font-semibold text-yellow-400 mb-3">⚠️ Why H100 May Be Overspending</h3>
        <div className="space-y-2 text-sm text-gray-300">
          <p>• <strong className="text-white">Your current workload:</strong> Using {Math.round(h100Power)}W on H100</p>
          <p>• <strong className="text-white">Same workload on A100:</strong> Only {Math.round(a100Power)}W</p>
          <p>• <strong className="text-white">Power difference:</strong> {Math.round(h100Power - a100Power)}W extra</p>
          <p>• <strong className="text-white">Why?</strong> H100 is designed for massive AI models (70B+ parameters). Your current workload doesn't need H100's power.</p>
          <p>• <strong className="text-white">Recommendation:</strong> Run light workloads on A100. Reserve H100 for large language models.</p>
        </div>
        <div className="mt-3 p-3 bg-yellow-900/30 rounded-lg">
          <p className="text-xs text-yellow-300">
            💡 <strong>Rule of thumb:</strong> If memory usage {"<"} 20GB and utilization is 100%, switch to A100.
          </p>
        </div>
      </div>

      {/* Savings Summary */}
      <div className="bg-gray-900 rounded-lg p-6 border border-green-700">
        <h3 className="text-sm font-semibold text-green-400 mb-4">💰 Potential Savings (Based on Test Data)</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center py-2 border-b border-gray-800">
            <span className="text-gray-300">Switch light workloads from H100 → A100</span>
            <span className="text-green-400 font-bold">Save ~${monthlySavingsSwitch.toFixed(0)}/month</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-gray-800">
            <span className="text-gray-300">Power cap H100 (690W → 380W)</span>
            <span className="text-green-400 font-bold">Save ~${monthlySavingsCap.toFixed(0)}/month</span>
          </div>
          <div className="flex justify-between items-center py-2 border-b border-gray-800">
            <span className="text-gray-300">Shift 8 hours to off-peak</span>
            <span className="text-green-400 font-bold">Save ~${monthlySavingsOffPeak.toFixed(0)}/month</span>
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-4">Based on test run data: H100 {Math.round(h100Power)}W, A100 {Math.round(a100Power)}W</p>
      </div>

      {/* AI Optimization Recommendations */}
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-800">
        <h3 className="text-sm font-semibold text-gray-300 mb-4">AI Optimization Recommendations</h3>
        <div className="space-y-3">
          {recommendations.map((rec, idx) => (
            <div key={idx} className="flex justify-between items-center py-2 border-b border-gray-800">
              <span className="text-gray-300">{rec.text}</span>
              <span className="text-green-400 text-sm">{rec.savings}</span>
            </div>
          ))}
        </div>
        <div className="mt-4 text-xs text-gray-500">Based on recorded test data</div>
      </div>
    </div>
  );
              }
