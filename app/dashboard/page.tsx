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
    const gpuData = data.clusters.map(cluster => ({
      cluster_name: cluster.name,
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
        clusterName: cluster
