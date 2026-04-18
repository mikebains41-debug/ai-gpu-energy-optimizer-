/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
import { DashboardData } from '@/types';

export const mockData: DashboardData = {
  clusters: [
    { id: '1', name: 'NVIDIA H100 Cluster A', location: 'US-West (Oregon)', gpuCount: 256, activeGPUs: 243, powerConsumption: 1850, temperature: 72, utilization: 94.9, energyCost: 0.08, renewablePercentage: 65, status: 'optimal' },
    { id: '2', name: 'NVIDIA A100 Cluster B', location: 'US-East (Virginia)', gpuCount: 128, activeGPUs: 115, powerConsumption: 920, temperature: 78, utilization: 89.8, energyCost: 0.12, renewablePercentage: 45, status: 'warning' },
    { id: '3', name: 'Training Cluster C', location: 'EU-West (Ireland)', gpuCount: 64, activeGPUs: 62, powerConsumption: 480, temperature: 68, utilization: 96.9, energyCost: 0.15, renewablePercentage: 82, status: 'optimal' },
    { id: '4', name: 'Inference Cluster D', location: 'Asia-Pacific (Singapore)', gpuCount: 96, activeGPUs: 88, powerConsumption: 720, temperature: 81, utilization: 91.7, energyCost: 0.11, renewablePercentage: 38, status: 'critical' },
  ],
  energyMetrics: [
    { timestamp: '00:00', totalPower: 3200, renewablePower: 1920, cost: 256, carbonFootprint: 1280 },
    { timestamp: '04:00', totalPower: 2800, renewablePower: 1960, cost: 196, carbonFootprint: 980 },
    { timestamp: '08:00', totalPower: 3500, renewablePower: 2100, cost: 315, carbonFootprint: 1225 },
    { timestamp: '12:00', totalPower: 3900, renewablePower: 2730, cost: 351, carbonFootprint: 1170 },
    { timestamp: '16:00', totalPower: 4100, renewablePower: 2460, cost: 410, carbonFootprint: 1435 },
    { timestamp: '20:00', totalPower: 3700, renewablePower: 2220, cost: 333, carbonFootprint: 1295 },
    { timestamp: '23:59', totalPower: 3400, renewablePower: 2040, cost: 272, carbonFootprint: 1190 },
  ],
  heatOutput: [
    { clusterId: '1', heatGenerated: 6315000, heatCaptured: 5683500, heatRedirected: 'greenhouses', efficiency: 90 },
    { clusterId: '2', heatGenerated: 3139200, heatCaptured: 2511360, heatRedirected: 'buildings', efficiency: 80 },
    { clusterId: '3', heatGenerated: 1637760, heatCaptured: 1555872, heatRedirected: 'industrial', efficiency: 95 },
    { clusterId: '4', heatGenerated: 2456640, heatCaptured: 1965312, heatRedirected: 'buildings', efficiency: 80 },
  ],
  optimizations: [
    { id: '1', type: 'scheduling', description: 'Shift 40% of batch training jobs to 2-6 AM when renewable energy peaks at 85%', potentialSavings: 18500, implementation: 'automatic', priority: 'high' },
    { id: '2', type: 'load-balancing', description: 'Redirect inference workloads from Singapore to Ireland during EU solar peak hours', potentialSavings: 12300, implementation: 'automatic', priority: 'high' },
    { id: '3', type: 'cooling', description: 'Increase cooling efficiency in Cluster D by 15% using predictive thermal management', potentialSavings: 8700, implementation: 'manual', priority: 'medium' },
    { id: '4', type: 'power', description: 'Enable GPU power capping at 85% for non-critical workloads during peak pricing', potentialSavings: 15200, implementation: 'automatic', priority: 'high' },
   
