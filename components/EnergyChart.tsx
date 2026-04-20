'use client';

import { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface EnergyChartProps {
  data: Array<{
    timestamp: string;
    totalPower: number;
    renewablePower?: number;
  }>;
}

export default function EnergyChart({ data }: EnergyChartProps) {
  const [showRenewable, setShowRenewable] = useState(true);

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-100">Energy Consumption</h3>
        <button
          onClick={() => setShowRenewable(!showRenewable)}
          className={`px-3 py-1 text-sm rounded-lg transition-colors ${
            showRenewable ? 'bg-green-600 text-white' : 'bg-gray-800 text-gray-400'
          }`}
        >
          Renewable
        </button>
      </div>

      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              {showRenewable && (
                <linearGradient id="colorRenewable" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              )}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis 
              dataKey="timestamp" 
              stroke="#9ca3af" 
              fontSize={12}
              tickFormatter={(value) => {
                const date = new Date(value);
                return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
              }}
            />
            <YAxis 
              stroke="#9ca3af" 
              fontSize={12} 
              tickFormatter={(value) => `${value} kW`}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#111827', 
                border: '1px solid #374151', 
                borderRadius: '8px',
                color: '#f3f4f6'
              }}
              formatter={(value: number) => [`${value} kW`, 'Power']}
            />
            <Area 
              type="monotone" 
              dataKey="totalPower" 
              name="Total Power" 
              stroke="#3b82f6" 
              fillOpacity={1} 
              fill="url(#colorTotal)" 
              strokeWidth={2} 
            />
            {showRenewable && (
              <Area 
                type="monotone" 
                dataKey="renewablePower" 
                name="Renewable Power" 
                stroke="#10b981" 
                fillOpacity={1} 
                fill="url(#colorRenewable)" 
                strokeWidth={2} 
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
