/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { GPUCluster } from '@/types';
import { Cpu, Zap, Thermometer, Activity } from 'lucide-react';
import { cn, formatPower, formatPercentage } from '@/lib/utils';

interface GPUMetricsCardProps { cluster: GPUCluster; }

export default function GPUMetricsCard({ cluster }: GPUMetricsCardProps) {
  const statusColors = { optimal: 'bg-green-500', warning: 'bg-yellow-500', critical: 'bg-red-500' };
  const statusLabels = { optimal: 'Optimal', warning: 'Warning', critical: 'Critical' };

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6 hover:border-gray-700 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div><h3 className="font-semibold text-gray-100">{cluster.name}</h3><p className="text-sm text-gray-400">{cluster.location}</p></div>
        <div className="flex items-center gap-2"><span className={cn('h-2 w-2 rounded-full', statusColors[cluster.status])} /><span className="text-xs text-gray-400">{statusLabels[cluster.status]}</span></div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1"><div className="flex items-center gap-2 text-gray-400"><Cpu className="h-4 w-4" /><span className="text-xs">GPU Utilization</span></div><p className="text-lg font-semibold text-gray-100">{formatPercentage(cluster.utilization)}</p><p className="text-xs text-gray-500">{cluster.activeGPUs}/{cluster.gpuCount} active</p></div>
        <div className="space-y-1"><div className="flex items-center gap-2 text-gray-400"><Zap className="h-4 w-4" /><span className="text-xs">Power Draw</span></div><p className="text-lg font-semibold text-gray-100">{formatPower(cluster.powerConsumption)}</p><p className="text-xs text-gray-500">${cluster.energyCost}/kWh</p></div>
        <div className="space-y-1"><div className="flex items-center gap-2 text-gray-400"><Thermometer className="h-4 w-4" /><span className="text-xs">Temperature</span></div><p className={cn("text-lg font-semibold", cluster.temperature > 75 ? "text-red-400" : "text-gray-100")}>{cluster.temperature}°C</p><p className="text-xs text-gray-500">{cluster.temperature > 75 ? 'High' : 'Normal'}</p></div>
        <div className="space-y-1"><div className="flex items-center gap-2 text-gray-400"><Activity className="h-4 w-4" /><span className="text-xs">Renewable</span></div><p className="text-lg font-semibold text-gray-100">{formatPercentage(cluster.renewablePercentage)}</p><p className="text
