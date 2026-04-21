'use client';

import { AlertTriangle, Thermometer, Zap, Cpu, Droplet } from 'lucide-react';

interface GPUMetricsCardProps {
  cluster: any;
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

export default function GPUMetricsCard({ cluster }: GPUMetricsCardProps) {
  const tempStatus = getTempStatus(cluster.temperature.gpu || 65);
  const TempIcon = tempStatus.icon;

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6 hover:border-gray-700 transition-colors">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Cpu className="h-6 w-6 text-blue-500" />
          <div>
            <h3 className="text-lg font-semibold text-gray-100">{cluster.name || 'GPU Cluster'}</h3>
            <p className="text-sm text-gray-400">{cluster.location || 'US-West'}</p>
          </div>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          cluster.status === 'optimal' ? 'bg-green-500/20 text-green-400' :
          cluster.status === 'warning' ? 'bg-yellow-500/20 text-yellow-400' :
          'bg-red-500/20 text-red-400'        }`}>
          {cluster.status === 'optimal' ? 'Optimal' :
           cluster.status === 'warning' ? 'Warning' : 'Critical'}
        </span>
      </div>

      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-gray-400 text-sm">
              <Zap className="h-4 w-4" />
              <span>GPU Utilization</span>
            </div>
            <p className="text-2xl font-bold text-gray-100">{(cluster.gpu_utilization || 0).toFixed(1)}%</p>
            <div className="w-full bg-gray-800 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${
                  (cluster.gpu_utilization || 0) > 90 ? 'bg-green-500' :
                  (cluster.gpu_utilization || 0) > 75 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${cluster.gpu_utilization || 0}%` }}
              />
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-2 text-gray-400 text-sm">
              <Droplet className="h-4 w-4" />
              <span>Power Draw</span>
            </div>
            <p className="text-2xl font-bold text-gray-100">{cluster.power_draw_kw ? `${cluster.power_draw_kw.toFixed(1)} kW` : 'N/A'}</p>
            <p className="text-xs text-gray-500">${(cluster.power_draw_kw * 0.08 || 0).toFixed(3)}/kWh</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-gray-400 text-sm">
              <TempIcon className={`h-4 w-4 ${tempStatus.color}`} />
              <span>Temperature</span>
            </div>
            <p className="text-2xl font-bold text-gray-100">{cluster.temperature ? `${cluster.temperature.gpu}°C` : 'N/A'}</p>
            <p className={`text-xs ${tempStatus.color}`}>{tempStatus.label}</p>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-2 text-gray-400 text-sm">
              <Droplet className="h-4 w-4" />
              <span>Renewable</span>
            </div>            <p className="text-2xl font-bold text-gray-100">{cluster.renewable ? `${cluster.renewable}%` : 'N/A'}</p>
            <p className="text-xs text-gray-500">{cluster.renewable && cluster.renewable >= 50 ? 'Good' : 'Low'}</p>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-800">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Capacity</span>
            <span className="text-gray-100 font-medium">
              {cluster.active_gpus || 0}/{cluster.total_gpus || 0} active
            </span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-1.5 mt-2">
            <div 
              className="bg-blue-500 h-1.5 rounded-full"
              style={{ width: `${((cluster.active_gpus || 0) / (cluster.total_gpus || 1)) * 100}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
