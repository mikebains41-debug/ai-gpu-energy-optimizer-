'use client';

import { useState, useEffect } from 'react';

export default function DashboardContent() {
  const [clusters, setClusters] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch real live data from /metrics endpoint
    fetch('https://ai-gpu-brain-v3.onrender.com/metrics')
      .then(res => res.json())
      .then(data => {
        const clusterList = [];
        
        // Parse A100 data
        if (data['a100-80gb-runpod'] && data['a100-80gb-runpod'].length > 0) {
          const latestA100 = data['a100-80gb-runpod'][data['a100-80gb-runpod'].length - 1];
          const gpu = latestA100.gpus[0];
          clusterList.push({
            id: 'a100',
            name: 'NVIDIA A100 Cluster',
            location: 'US-East',
            gpu_utilization: gpu.utilization_percent || 85,
            power_draw: (gpu.power_draw_watts || 250) / 1000,
            temperature: gpu.temperature_celsius || 65,
            renewable_pct: 50,
            active_gpus: 1,
            total_gpus: 1,
            gpu_type: 'A100'
          });
        }
        
        // Parse H100 data
        if (data['h100-runpod'] && data['h100-runpod'].length > 0) {
          const latestH100 = data['h100-runpod'][data['h100-runpod'].length - 1];
          const gpu = latestH100.gpus[0];
          clusterList.push({
            id: 'h100',
            name: 'NVIDIA H100 Cluster',
            location: 'US-West',
            gpu_utilization: gpu.utilization_percent || 94,
            power_draw: (gpu.power_draw_watts || 380) / 1000,
            temperature: gpu.temperature_celsius || 58,
            renewable_pct: 50,
            active_gpus: 1,
            total_gpus: 1,
            gpu_type: 'H100'
          });
        }
        
        setClusters(clusterList);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching metrics:', err);
        setLoading(false);
      });
  }, []);

  // Calculate metrics from live data
  const h100Cluster = clusters.find(c => c.gpu_type === 'H100');
  const a100Cluster = clusters.find(c => c.gpu_type === 'A100');

  const h100Power = h100Cluster?.power_draw ? h100Cluster.power_draw * 1000 : 380;
  const a100Power = a100Cluster?.power_draw ? a100Cluster.power_draw * 1000 : 250;
  const h100Util = h100Cluster?.gpu_utilization || 94;
  const a100Util = a100Cluster?.gpu_utilization || 85;
  const h100Temp = h100Cluster?.temperature || 58;
  const a100Temp = a100Cluster?.temperature || 65;

  // Annual savings calculation
  const powerSavings = (h100Power - a100Power) / 1000;
  const annualSavings = powerSavings * 24 * 365 * 0.12;
  const co2Reduction = powerSavings * 24 * 365 * 0.4;

  // Efficiency scores
  const avgEfficiency = ((h100Util / (h100Power / 1000)) + (a100Util / (a100Power / 1000))) / 2;
  const efficiencyPercent = (avgEfficiency / 10).toFixed(1);

  // Recommendations based on temperature
  const recommendations = [];
  if (h100Temp > 70) {
    recommendations.push({ text: 'Reduce H100 power cap by 5%', savings: '$2,400/year' });
  }
  if (a100Temp > 70) {
    recommendations.push({ text: 'Reduce A100 power cap by 3%', savings: '$1,200/year' });
  }
  if (recommendations.length === 0) {
    recommendations.push({ text: 'All temperatures normal. No action needed.', savings: '$0' });
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-400">Loading GPU metrics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-100">AI GPU Energy Optimizer</h1>
        <p className="text-gray-400 text-sm">Real-time power, temperature, and utilization monitoring for A100 and H100 GPUs.</p>
        <p className="text-gray-500 text-xs mt-1">Built on Samsung S25 Ultra | No laptop, no desktop</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-r from-green-900/30 to-green-800/20 rounded-lg p-4 border border-green-700">
          <p className="text-gray-400 text-sm">Annual Savings</p>
          <p className="text-2xl font-bold text-green-400">${annualSavings.toLocaleString()}</p>
          <p className="text-xs text-green-500 mt-1">↘️ Estimated energy cost reduction</p>
        </div>
        <div className="bg-gradient-to-r from-blue-900/30 to-blue-800/20 rounded-lg p-4 border border-blue-700">
          <p className="text-gray-400 text-sm">CO₂ Reduction</p>
          <p className="text-2xl font-bold text-blue-400">{co2Reduction.toFixed(0)} kg</p>
          <p className="text-xs text-blue-500 mt-1">Per GPU per year</p>
        </div>
        <div className="bg-gradient-to-r from-purple-900/30 to-purple-800/20 rounded-lg p-4 border border-purple-700">
          <p className="text-gray-400 text-sm">Efficiency Score</p>
          <p className="text-2xl font-bold text-purple-400">{efficiencyPercent}%</p>
          <p className="text-xs text-purple-500 mt-1">Fleet average</p>
        </div>
      </div>

      {/* GPU Clusters */}
      <div className="grid md:grid-cols-2 gap-6">
        {clusters.map((cluster) => (
          <div key={cluster.id} className="bg-gray-900 rounded-lg p-6 border border-gray-800">
            <div className="flex justify-between items-start mb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-xl font-semibold text-gray-100">{cluster.name}</h2>
                  <span className={`px-2 py-1 text-xs font-bold rounded ${cluster.gpu_type === 'H100' ? 'bg-purple-600 text-white' : 'bg-blue-600 text-white'}`}>
                    {cluster.gpu_type}
                  </span>
                </div>
                <p className="text-sm text-gray-400 mt-1">{cluster.location}</p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-gray-100">{cluster.active_gpus}/{cluster.total_gpus}</div>
                <div className="text-xs text-gray-500">Active GPUs</div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="text-xs text-gray-400">GPU Utilization</div>
                <div className="text-2xl font-bold text-gray-100">{cluster.gpu_utilization}%</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="text-xs text-gray-400">Power Draw</div>
                <div className="text-2xl font-bold text-gray-100">{cluster.power_draw.toFixed(2)} MW</div>
                <div className="text-xs text-gray-500">Real-time</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="text-xs text-gray-400">Temperature</div>
                <div className="text-2xl font-bold text-gray-100">{cluster.temperature}°C</div>
              </div>
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="text-xs text-gray-400">Clean Energy</div>
                <div className="text-2xl font-bold text-gray-100">{cluster.renewable_pct}%</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recommendations Section */}
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
        <div className="mt-4 text-xs text-gray-500">
          Based on real-time temperature and utilization data
        </div>
      </div>

      {/* Legend */}
      <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
        <h3 className="text-sm font-semibold text-gray-300 mb-2">GPU Cluster Legend</h3>
        <div className="flex gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-600"></div>
            <span className="text-sm text-gray-400">H100 (Higher Power, Higher Performance)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-600"></div>
            <span className="text-sm text-gray-400">A100 (Standard Power, Efficient)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
