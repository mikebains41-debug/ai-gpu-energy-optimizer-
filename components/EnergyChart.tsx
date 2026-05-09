/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
 * Contact: mikebains41@gmail.com
 */
'use client';

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Hardcoded test data from A100 load ramp test (Test 4)
const fallbackData = [
  { timestamp: "0s", totalPower: 68, renewablePower: 0 },
  { timestamp: "30s", totalPower: 145, renewablePower: 0 },
  { timestamp: "60s", totalPower: 221, renewablePower: 0 },
  { timestamp: "90s", totalPower: 343, renewablePower: 0 },
  { timestamp: "120s", totalPower: 320, renewablePower: 0 },
];

interface EnergyChartProps {
  data?: Array<{
    timestamp: string;
    totalPower: number;
    renewablePower?: number;
  }>;
}

export default function EnergyChart({ data }: EnergyChartProps) {
  const chartData = data && data.length > 0 ? data : fallbackData;
  const maxPower = Math.max(...chartData.map(d => d.totalPower), 350);

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-100">Energy Consumption (Recorded Test Data)</h3>
      </div>

      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" fontSize={12} />
            <YAxis 
              stroke="#9ca3af" 
              fontSize={12} 
              domain={[0, 400]} 
              tickFormatter={(value) => `${value} W`} 
            />
            <Tooltip
              contentStyle={{ 
                backgroundColor: '#111827', 
                border: '1px solid #374151', 
                borderRadius: '8px',
                color: '#f3f4f6'
              }}
              formatter={(value: number) => [`${value} W`, 'Power']}
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
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
