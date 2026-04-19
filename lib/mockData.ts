/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
import { DashboardData } from '@/types';

export const mockData: DashboardData = {
  clusters: [
    { id: '1', name: 'NVIDIA H100 Cluster', location: 'US-West', gpuCount: 256, activeGPUs: 243, powerConsumption: 1850, temperature: 72, utilization: 94.9, energyCost: 0.08, renewablePercentage: 65, status: 'optimal' },
    { id: '2', name: 'NVIDIA A100 Cluster', location: 'US-East', gpuCount: 128, activeGPUs: 115, powerConsumption: 920, temperature: 78, utilization: 89.8, energyCost: 0.12, renewablePercentage: 45, status: 'warning' },
  ],
  energyMetrics: [
    { timestamp: '00:00', totalPower: 3200, renewablePower: 1920, cost: 256, carbonFootprint: 1280 },
    { timestamp: '12:00', totalPower: 3900, renewablePower: 2730, cost: 351, carbonFootprint: 1170 },
  ],
  heatOutput: [
    { clusterId: '1', heatGenerated: 6315000, heatCaptured: 5683500, heatRedirected: 'greenhouses', efficiency: 90 },
  ],
  optimizations: [
    { id: '1', type: 'scheduling', description: 'Shift jobs to off-peak hours', potentialSavings: 18500, implementation: 'automatic', priority: 'high' },
    { id: '2', type: 'cooling', description: 'Improve thermal management', potentialSavings: 8700, implementation: 'manual', priority: 'medium' },
  ],
  totalCostSavings: 2847500,
  carbonReduction: 15680,
};
