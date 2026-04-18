/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
export interface GPUCluster {
  id: string;
  name: string;
  location: string;
  gpuCount: number;
  activeGPUs: number;
  powerConsumption: number;
  temperature: number;
  utilization: number;
  energyCost: number;
  renewablePercentage: number;
  status: 'optimal' | 'warning' | 'critical';
}

export interface EnergyMetric {
  timestamp: string;
  totalPower: number;
  renewablePower: number;
  cost: number;
  carbonFootprint: number;
}

export interface HeatOutput {
  clusterId: string;
  heatGenerated: number;
  heatCaptured: number;
  heatRedirected: string;
  efficiency: number;
}

export interface Optimization {
  id: string;
  type: 'scheduling' | 'load-balancing' | 'cooling' | 'power';
  description: string;
  potentialSavings: number;
  implementation: 'automatic' | 'manual';
  priority: 'high' | 'medium' | 'low';
}

export interface DashboardData {
  clusters: GPUCluster[];
  energyMetrics: EnergyMetric[];
  heatOutput: HeatOutput[];
  optimizations: Optimization[];
  totalCostSavings: number;
  carbonReduction: number;
}
