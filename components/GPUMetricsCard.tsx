/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { GPUMetrics } from '@/types';
import { AlertTriangle, Thermometer, Zap, Cpu, Droplet } from 'lucide-react';

interface GPUMetricsCardProps {
  cluster: GPUMetrics;
}

const getTempStatus = (temp: number) => {
  if (temp > 85) return { 
    color: 'text-red-500', 
    bg: 'bg-red-500/20',
    border: 'border-red-500',
    label: 'Critical',
    icon: AlertTriangle 
  };
  if (temp > 75) return { 
    color: 'text-yellow-500', 
    bg: 'bg-yellow-500/20',
    border: 'border-yellow-500',
    label: 'Warning',
    icon: AlertTriangle 
  };
  return { 
    color: 'text-green-500', 
    bg: 'bg-green-500/20',
    border: 'border-green-500',
    label: 'Normal',
    icon: Thermometer 
  };
};

const getStatusColor = (status: string) => {
  switch (status) {
    case 'Optimal': return 'bg-green-500';
    case 'Warning': return 'bg-yellow-500';
    case 'Critical': return 'bg-red-500';
    default: return 'bg-gray-500';
  }
};

export default function GPUMetricsCard({ cluster }: GPUMetricsCardProps) {
  const tempStatus = getTempStatus(cluster.temperature);
  const TempIcon = tempStatus.icon;
  return (
    <div className={`rounded-xl border-2 ${tempStatus.border} bg-gray-900/50 p-6 transition-all hover:scale-[1.02]`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-semibold text-gray-100">{cluster.name}</h3>
          <p className="text-gray-400 text-sm">{cluster.location}</p>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${tempStatus.bg}`}>
          <div className={`w-2 h-2 rounded-full ${getStatusColor(cluster.status)}`} />
          <span className={`text-sm font-medium ${tempStatus.color}`}>{cluster.status}</span>
        </div>
      </div>

      {/* Temperature Alert Banner */}
      {cluster.temperature > 75 && (
        <div className={`mb-4 p-3 rounded-lg border ${tempStatus.border} ${tempStatus.bg} flex items-center gap-3`}>
          <TempIcon className={`h-5 w-5 ${tempStatus.color}`} />
          <div>
            <p className={`text-sm font-semibold ${tempStatus.color}`}>
              {tempStatus.label} Temperature Alert
            </p>
            <p className="text-xs text-gray-400">
              {cluster.temperature > 85 
                ? 'Immediate action required! GPU overheating.' 
                : 'Monitor closely. Consider improving cooling.'}
            </p>
          </div>
        </div>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-4">
        {/* GPU Utilization */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <Cpu className="h-4 w-4" />
            <span className="text-sm">GPU Utilization</span>
          </div>
          <p className="text-2xl font-bold text-gray-100">{cluster.gpuUtilization}%</p>
          <p className="text-xs text-gray-500">{cluster.activeGPUs}/{cluster.totalGPUs} active</p>
        </div>

        {/* Power Draw */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <Zap className="h-4 w-4" />
            <span className="text-sm">Power Draw</span>
          </div>          <p className="text-2xl font-bold text-gray-100">{cluster.powerDraw}</p>
          <p className="text-xs text-gray-500">{cluster.costPerKWh}/kWh</p>
        </div>

        {/* Temperature */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <Thermometer className="h-4 w-4" />
            <span className="text-sm">Temperature</span>
          </div>
          <p className={`text-2xl font-bold ${tempStatus.color}`}>{cluster.temperature}°C</p>
          <p className={`text-xs ${tempStatus.color}`}>{tempStatus.label}</p>
        </div>

        {/* Renewable Energy */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-gray-400">
            <Droplet className="h-4 w-4" />
            <span className="text-sm">Renewable</span>
          </div>
          <p className="text-2xl font-bold text-gray-100">{cluster.renewablePercentage}%</p>
          <p className="text-xs text-gray-500">
            {cluster.renewablePercentage >= 60 ? 'Good' : 'Needs improvement'}
          </p>
        </div>
      </div>

      {/* Capacity Bar */}
      <div className="mt-6">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-gray-400">Capacity</span>
          <span className="text-gray-100 font-medium">{cluster.gpuUtilization}%</span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <div 
            className={`h-full transition-all duration-500 ${
              cluster.gpuUtilization > 90 ? 'bg-red-500' :
              cluster.gpuUtilization > 75 ? 'bg-yellow-500' :
              'bg-green-500'
            }`}
            style={{ width: `${cluster.gpuUtilization}%` }}
          />
        </div>
      </div>
    </div>
  );
}
