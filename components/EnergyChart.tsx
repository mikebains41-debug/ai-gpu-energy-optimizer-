/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { EnergyMetric } from '@/types';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { formatPower, formatCurrency } from '@/lib/utils';

interface EnergyChartProps {  EnergyMetric[]; }

export default function EnergyChart({ data }: EnergyChartProps) {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <h3 className="text-lg font-semibold text-gray-100 mb-6">Energy Consumption Over Time</h3>
      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/><stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/></linearGradient>
              <linearGradient id="colorRenewable" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/><stop offset="95%" stopColor="#10b981" stopOpacity={0}/></linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" fontSize={12} />
            <YAxis stroke="#9ca3af" fontSize={12} tickFormatter={(value) => formatPower(value)} />
            <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} formatter={(value: number, name: string) => {
              if (name === 'Total Power') return [formatPower(value), name];
              if (name === 'Renewable Power') return [formatPower(value), name];
              if (name === 'Cost') return [formatCurrency(value), name];
              return [value, name];
            }} />
            <Legend />
            <Area type="monotone" dataKey="totalPower" name="Total Power" stroke="#3b82f6" fillOpacity={1} fill="url(#colorTotal)" strokeWidth={2} />
            <Area type="monotone" dataKey="renewablePower" name="Renewable Power" stroke="#10b981" fillOpacity={1} fill="url(#colorRenewable)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
