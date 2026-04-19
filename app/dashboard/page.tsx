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
import TemperatureAlert from '@/components/TemperatureAlert';
import { useNotifications } from '@/contexts/NotificationContext';
import { useTheme } from '@/contexts/ThemeContext';
import { mockData } from '@/lib/mockData';
import { DashboardData } from '@/types';
import { RefreshCw, Download } from 'lucide-react';
import { exportToCSV } from '@/lib/exportData';

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData>(mockData);
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [activeAlerts, setActiveAlerts] = useState<Array<{
    id: string;
    clusterName: string;
    temperature: number;
    location: string;
  }>>([]);

  const { addNotification } = useNotifications();
  const { settings } = useTheme();

  const refreshData = () => {
    setIsLoading(true);
    setTimeout(() => {
      setData(mockData);
      setLastUpdated(new Date());
      setIsLoading(false);
    }, 1000);
  };

  const exportEnergyData = () => {
    exportToCSV(data.energyMetrics, 'energy_consumption');
  };

  const exportGPUData = () => {
    const gpuData = data.clusters.map(cluster => ({      cluster_name: cluster.name,
      location: cluster.location,
      status: cluster.status,
      gpu_utilization: `${cluster.gpuUtilization}%`,
      power_draw: cluster.powerDraw,
      temperature: `${cluster.temperature}°C`,
      renewable_energy: `${cluster.renewablePercentage}%`,
      active_gpus: `${cluster.activeGPUs}/${cluster.totalGPUs}`,
      cost_per_kwh: cluster.costPerKWh
    }));
    exportToCSV(gpuData, 'gpu_metrics');
  };

  // Monitor temperatures & trigger alerts/notifications
  useEffect(() => {
    const alerts = data.clusters
      .filter(cluster => cluster.temperature > 75)
      .map(cluster => ({
        id: cluster.id,
        clusterName: cluster.name,
        temperature: cluster.temperature,
        location: cluster.location
      }));
    
    setActiveAlerts(alerts);

    // Push to notification center
    alerts.forEach(alert => {
      const type = alert.temperature > 85 ? 'error' : 'warning';
      addNotification({
        type,
        title: type === 'error' ? 'Critical Temperature Alert' : 'Temperature Warning',
        message: `${alert.clusterName} (${alert.location}) is running at ${alert.temperature}°C`
      });
    });
  }, [data.clusters, addNotification]);

  const dismissAlert = (id: string) => {
    setActiveAlerts(prev => prev.filter(alert => alert.id !== id));
  };

  // Use saved refresh interval from settings
  useEffect(() => {
    const interval = setInterval(refreshData, settings.refreshInterval);
    return () => clearInterval(interval);
  }, [settings.refreshInterval]);

  return (
    <DashboardLayout>
      {/* Floating Temperature Alerts */}      {activeAlerts.map(alert => (
        <TemperatureAlert 
          key={alert.id}
          clusterName={alert.clusterName}
          temperature={alert.temperature}
          location={alert.location}
          onDismiss={() => dismissAlert(alert.id)}
        />
      ))}

      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-100">Dashboard</h2>
            <p className="text-gray-400 mt-1">Real-time GPU energy optimization and monitoring</p>
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <p className="text-sm text-gray-500">Last updated: {lastUpdated.toLocaleTimeString()}</p>
            <button 
              onClick={exportGPUData}
              className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
            >
              <Download className="h-4 w-4" />
              Export GPU Data
            </button>
            <button 
              onClick={exportEnergyData}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
            >
              <Download className="h-4 w-4" />
              Export Energy Data
            </button>
            <button 
              onClick={refreshData} 
              disabled={isLoading} 
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 rounded-lg transition-colors"
            >
              <RefreshCw className={isLoading ? "animate-spin h-4 w-4" : "h-4 w-4"} />
              Refresh
            </button>
          </div>
        </div>

        {/* Cost Savings */}
        <CostSavings 
          totalSavings={data.totalCostSavings} 
          carbonReduction={data.carbonReduction} 
        />
        {/* GPU Clusters */}
        <div>
          <h3 className="text-xl font-semibold text-gray-100 mb-4">GPU Clusters</h3>
          <div className="grid grid-cols
