/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import GPUMetricsCard from '@/components/GPUMetricsCard';
import EnergyChart from '@/components/EnergyChart';
import OptimizationPanel from '@/components/OptimizationPanel';
import CostSavings from '@/components/CostSavings';
import { useOptimizationStream } from '@/hooks/useOptimizationStream';
import { RefreshCw, Zap } from 'lucide-react';

export default function DashboardPage() {
  const { data, connected } = useOptimizationStream();
  const [lastUpdated, setLastUpdated] = useState(new Date());

  useEffect(() => {
    if (data) setLastUpdated(new Date());
  }, [data]);

  if (!data) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-[60vh]">
          <div className="text-center">
            <Zap className="h-12 w-12 text-blue-500 animate-pulse mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-100">Connecting to AI Engine...</h2>
            <p className="text-gray-400 mt-2">Streaming real-time optimization data</p>
            {!connected && (
              <p className="text-sm text-yellow-500 mt-4">
                Make sure AI Engine is running on port 8000
              </p>
            )}
          </div>
        </div>
      </DashboardLayout>
    );
  }

  // Map AI engine output to your existing component props
  const dashboardData = {
    clusters: data.clusters,
    energyMetrics: [], // Will populate from real time-series DB later
    totalCostSavings: data.recommendations.reduce((sum, r) => sum + r.estimated_savings_monthly, 0) * 12,
    carbonReduction: Math.floor(data.grid_carbon_intensity * 10000),
    optimizations: data.recommendations,
  };

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Live Status Header */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-3xl font-bold text-gray-100">AI Optimization Dashboard</h2>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                connected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }`}>
                {connected ? '● Live' : '○ Disconnected'}
              </span>
            </div>
            <p className="text-gray-400 mt-1">Real-time GPU energy optimization & AI recommendations</p>
          </div>
          <div className="flex items-center gap-4">
            <p className="text-sm text-gray-500">Last updated: {lastUpdated.toLocaleTimeString()}</p>
            <div className="flex items-center gap-2 px-4 py-2 bg-blue-600/20 rounded-lg">
              <Zap className="h-4 w-4 text-blue-400" />
              <span className="text-sm text-blue-300">{data.total_power_mw.toFixed(2)} MW Total</span>
            </div>
          </div>
        </div>

        <CostSavings 
          totalSavings={dashboardData.totalCostSavings} 
          carbonReduction={dashboardData.carbonReduction} 
        />

        <div>
          <h3 className="text-xl font-semibold text-gray-100 mb-4">GPU Clusters</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {dashboardData.clusters.map((cluster: any) => (
              <GPUMetricsCard key={cluster.id} cluster={cluster} />
            ))}
          </div>
        </div>

        <EnergyChart data={[]} />
        
        <OptimizationPanel optimizations={dashboardData.optimizations} />
      </div>
    </DashboardLayout>
  );
}
