/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import DashboardLayout from '@/components/DashboardLayout';
import { useOptimizationStream } from '@/hooks/useOptimizationStream';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { Globe, Zap } from 'lucide-react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

export default function AnalyticsPage() {
  const { data, connected } = useOptimizationStream();

  if (!data) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-[60vh]">
          <div className="text-center">
            <Zap className="h-12 w-12 text-blue-500 animate-pulse mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-100">Loading analytics data...</h2>
            <p className="text-gray-400 mt-2">Waiting for real-time GPU metrics</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  // Transform real data for charts
  const clusterData = data.clusters?.map((c: any) => ({
    name: c.name?.split(' ')[0] || c.id,
    power: c.power_draw || 0,
    utilization: c.gpu_utilization || 0,
    renewable: c.renewable_pct || 0,
    temperature: c.temperature || 0,
    location: c.location || 'Unknown',
    id: c.id
  })) || [];

  // Heat data from temperature (approximate)
  const heatData = data.clusters?.map((c: any, index: number) => ({
    name: c.name?.split(' ')[0] || c.id,
    captured: Math.round(100 - (c.temperature / 100) * 100),
    wasted: Math.round((c.temperature / 100) * 100),
  })) || [];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-100">Analytics</h2>
            <p className="text-gray-400 mt-1">Deep insights into energy usage and optimization</p>
          </div>
          <div className={`px-3 py-1 rounded-full text-xs font-medium ${
            connected ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
          }`}>
            {connected ? '● Live Data' : '○ Demo Mode'}
          </div>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
          <h3 className="text-lg font-semibold text-gray-100 mb-6">Power Usage by Cluster</h3>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={clusterData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} />
                <Legend />
                <Bar dataKey="power" name="Power (MW)" fill="#3b82f6" />
                <Bar dataKey="utilization" name="Utilization %" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
          <h3 className="text-lg font-semibold text-gray-100 mb-6">Heat & Cooling Efficiency</h3>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie 
                  data={heatData} 
                  cx="50%" 
                  cy="50%" 
                  labelLine={false} 
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`} 
                  outerRadius={150} 
                  fill="#8884d8" 
                  dataKey="captured"
                >
                  {heatData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="text-center text-sm text-gray-500 mt-4">Heat capture efficiency by cluster</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {clusterData.map((cluster: any) => (
            <div key={cluster.id} className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
              <div className="flex items-center gap-3 mb-4">
                <Globe className="h-5 w-5 text-blue-400" />
                <h4 className="font-semibold text-gray-100">{cluster.location}</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-400">Renewable Energy</span>
                  <span className="text-sm font-medium text-green-400">{cluster.renewable}%</span>
                </div>
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 rounded-full" style={{ width: `${cluster.renewable}%` }} />
                </div>
                <div className="flex justify-between items-center pt-2">
                  <span className="text-sm text-gray-400">Power Draw</span>
                  <span className="text-sm font-medium text-gray-100">{cluster.power} MW</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-400">Avg Temperature</span>
                  <span className="text-sm font-medium text-gray-100">{cluster.temperature}°C</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-400">GPU Utilization</span>
                  <span className="text-sm font-medium text-gray-100">{cluster.utilization}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
