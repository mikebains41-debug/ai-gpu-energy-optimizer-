'use client';

import { EnergyMetric } from '@/types';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface EnergyChartProps {
  data: EnergyMetric[];
}

export default function EnergyChart({ data }: EnergyChartProps) {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <h3 className="text-lg font-semibold text-gray-100 mb-6">Energy Consumption</h3>
      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" tickFormatter={(v) => `${v} kW`} />
            <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151' }} />
            <Area type="monotone" dataKey="totalPower" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.2} name="Total Power" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
