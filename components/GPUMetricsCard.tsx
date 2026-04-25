/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

interface ClusterData {
  id: string;
  name: string;
  location?: string;
  gpu_utilization: number;
  memory_usage?: number;
  temperature: number;
  power_draw?: number;
  power_draw_kw?: number;
  renewable_pct?: number;
  efficiency_score?: number;
  status?: string;
  total_gpus?: number;
  active_gpus?: number;
}

interface GPUMetricsCardProps {
  cluster: ClusterData;
}

export default function GPUMetricsCard({ cluster }: GPUMetricsCardProps) {
  const getStatusColor = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'optimal':
        return 'bg-green-500/20 text-green-400';
      case 'warning':
        return 'bg-yellow-500/20 text-yellow-400';
      case 'critical':
        return 'bg-red-500/20 text-red-400';
      default:
        return 'bg-blue-500/20 text-blue-400';
    }
  };

  const getStatusLabel = (status?: string) => {
    switch (status?.toLowerCase()) {
      case 'optimal':
        return 'Optimal';
      case 'warning':
        return 'Warning';
      case 'critical':
        return 'Critical';
      default:
        return 'Normal';
    }
  };

  const getUtilizationColor = (utilization: number) => {
    if (utilization >= 90) return 'bg-red-500';
    if (utilization >= 75) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const formatPowerDraw = () => {
    // Use power_draw_kw if available, otherwise power_draw (which is in kW)
    let powerKw = cluster.power_draw_kw ?? cluster.power_draw ?? 0;
    if (powerKw < 0.1) {
      // Values less than 0.1 kW (100 W) – show in watts
      const watts = Math.round(powerKw * 1000);
      return `${watts} W`;
    } else {
      // Show in kilowatts with two decimals
      return `${powerKw.toFixed(2)} kW`;
    }
  };

  const formatRenewable = () => {
    if (cluster.renewable_pct !== undefined && cluster.renewable_pct !== null) {
      return `${cluster.renewable_pct.toFixed(1)}%`;
    }
    return 'N/A';
  };

  return (
    <div className="bg-gray-900/50 border border-gray-800 rounded-xl p-6 hover:border-blue-500/50 transition-colors">
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500/20 rounded-lg">
            <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
          </div>
          <div>
            <h3 className="text-xl font-semibold text-gray-100">{cluster.name}</h3>
            <p className="text-sm text-gray-400">{cluster.location || 'Location N/A'}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(cluster.status)}`}>
          {getStatusLabel(cluster.status)}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* GPU Utilization */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="text-sm">GPU Utilization</span>
          </div>
          <div className="text-2xl font-bold text-gray-100">
            {cluster.gpu_utilization.toFixed(1)}%
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${getUtilizationColor(cluster.gpu_utilization)}`}
              style={{ width: `${cluster.gpu_utilization}%` }}
            />
          </div>
        </div>

        {/* Power Draw */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span className="text-sm">Power Draw</span>
          </div>
          <div className="text-2xl font-bold text-gray-100">
            {formatPowerDraw()}
          </div>
          <p className="text-xs text-gray-500">Real-time</p>
        </div>

        {/* Temperature */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span className="text-sm">Temperature</span>
          </div>
          <div className="text-2xl font-bold text-gray-100">
            {cluster.temperature.toFixed(1)}°C
          </div>
          <p className="text-xs text-green-400">
            {cluster.temperature > 80 ? '⚠️ High' : 'Normal'}
          </p>
        </div>

        {/* Renewable */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span className="text-sm">Renewable</span>
          </div>
          <div className="text-2xl font-bold text-gray-100">
            {formatRenewable()}
          </div>
          <p className="text-xs text-gray-500">
            {cluster.renewable_pct && cluster.renewable_pct > 50 ? 'Clean Energy' : 'Mixed Grid'}
          </p>
        </div>
      </div>

      {/* Capacity */}
      <div className="pt-4 border-t border-gray-800">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-gray-400">Capacity</span>
          <span className="text-gray-300">
            {cluster.active_gpus || 0}/{cluster.total_gpus || 0} active
          </span>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-1.5">
          <div
            className="bg-blue-500 h-1.5 rounded-full transition-all"
            style={{
              width: `${cluster.total_gpus ? ((cluster.active_gpus || 0) / cluster.total_gpus) * 100 : 0}%`
            }}
          />
        </div>
      </div>
    </div>
  );
}
