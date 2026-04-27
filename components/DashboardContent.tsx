'use client';

import { useState, useEffect } from 'react';

export default function DashboardContent() {
  const [clusters, setClusters] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://ai-gpu-brain-v3.onrender.com/optimize')
      .then(res => res.json())
      .then(data => {
        if (data.clusters) {
          setClusters(data.clusters);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-400">Loading GPU metrics...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-100">AI GPU Energy Optimizer</h1>
        <p className="text-gray-400 mt-2 max-w-2xl mx-auto">
          Real-time power, temperature, and utilization monitoring for A100 and H100 GPUs.
          Predict throttling. Optimize energy use. Deploy in 60 seconds.
        </p>
        <p className="text-gray-500 text-sm mt-4">
          Built on Samsung S25 Ultra | No laptop, no desktop
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {clusters.map((cluster: any) => {
          const isH100 = cluster.location === 'US-West' || cluster.id?.includes('h100');
          return (
            <div key={cluster.id} className="bg-gray-900 rounded-lg p-6 border border-gray-800">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-xl font-semibold text-gray-100">
                      {isH100 ? 'NVIDIA H100 Cluster' : 'NVIDIA A100 Cluster'}
                    </h2>
                    <span className={`px-2 py-1 text-xs font-bold rounded ${
                      isH100 ? 'bg-purple-600 text-white' : 'bg-blue-600 text-white'
                    }`}>
                      {isH100 ? 'H100' : 'A100'}
                    </span>
                  </div>
                  <p className="text-sm text-gray-400 mt-1">{cluster.location || 'Cluster'}</p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-gray-100">{cluster.active_gpus || 256}/{cluster.total_gpus || 256}</div>
                  <div className="text-xs text-gray-500">Active GPUs</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="bg-gray-800 rounded-lg p-3">
                  <div className="text-xs text-gray-400">GPU Utilization</div>
                  <div className="text-2xl font-bold text-gray-100">{cluster.gpu_utilization || 0}%</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3">
                  <div className="text-xs text-gray-400">Power Draw</div>
                  <div className="text-2xl font-bold text-gray-100">{cluster.power_draw || 0} MW</div>
                  <div className="text-xs text-gray-500">Real-time</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3">
                  <div className="text-xs text-gray-400">Temperature</div>
                  <div className="text-2xl font-bold text-gray-100">{cluster.temperature || 0}°C</div>
                </div>
                <div className="bg-gray-800 rounded-lg p-3">
                  <div className="text-xs text-gray-400">Clean Energy</div>
                  <div className="text-2xl font-bold text-gray-100">{cluster.renewable_pct || 0}%</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

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
