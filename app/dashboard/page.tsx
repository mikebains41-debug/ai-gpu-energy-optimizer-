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
import { mockData } from '@/lib/mockData';
import { DashboardData } from '@/types';
import { RefreshCw } from 'lucide-react';

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>(mockData);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const refreshData = () => {
    setIsLoading(true);
    setTimeout(() => {
      setData(mockData);
      setLastUpdated(new Date());
      setIsLoading(false);
    }, 1000);
  };

  useEffect(() => {
    const interval = setInterval(refreshData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-gray-100">Dashboard</h2>
            <p className="text-gray-400 mt-1">Real-time GPU energy optimization and monitoring</p>
          </div>
          <div className="flex items-center gap-4">
            <p className="text-sm text-gray-500">Last updated: {lastUpdated.toLocaleTimeString()}</p>
            <button onClick={refreshData} disabled={isLoading} className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-lg transition-colors">
              <RefreshCw className={isLoading ? "animate-spin h-4 w-4" : "h-4 w-4"} />
              Refresh
            </button>
          </div>
        </div>
        <CostSavings totalSavings={data.totalCostSavings} carbonReduction={data.carbonReduction} />
        <div>
          <h3 className="text-xl font-semibold text-gray-100 mb-4">GPU Clusters</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {data.clusters.map((cluster) => <GPUMetricsCard key={cluster.id} cluster={cluster} />)}
          </div>
        </div>
        <EnergyChart data={data.energyMetrics} />
        <OptimizationPanel optimizations={data.optimizations} />
      </div>
    </DashboardLayout>
  );
}
