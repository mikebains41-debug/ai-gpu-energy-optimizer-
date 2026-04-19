/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { useState } from 'react';
import { EnergyMetric } from '@/types';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Download } from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';

interface EnergyChartProps {
   EnergyMetric[];
}

type TimeRange = '1h' | '24h' | '7d' | '30d';

export default function EnergyChart({ data }: EnergyChartProps) {
  const { settings, updateSettings } = useTheme();
  const [showRenewable, setShowRenewable] = useState(true);

  const timeRanges: TimeRange[] = ['1h', '24h', '7d', '30d'];

  const filteredData = data.filter(item => {
    const now = new Date();
    const itemTime = new Date(item.timestamp);
    const diffMs = now.getTime() - itemTime.getTime();
    const diffHours = diffMs / (1000 * 60 * 60);

    switch (settings.chartTimeRange) {
      case '1h': return diffHours <= 1;
      case '24h': return diffHours <= 24;
      case '7d': return diffHours <= 24 * 7;
      case '30d': return diffHours <= 24 * 30;
      default: return true;
    }
  });

  const exportChart = () => {
    // Could add chart export functionality here
    alert('Chart export coming soon!');
  };

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
        <h3 className="text-lg font-semibold text-gray-100">Energy Consumption</h3>
                <div className="flex items-center gap-3 flex-wrap">
          {/* Time Range Selector */}
          <div className="flex rounded-lg overflow-hidden border border-gray-700">
            {timeRanges.map(range => (
              <button
                key={range}
                onClick={() => updateSettings({ chartTimeRange: range })}
                className={`px-3 py-1 text-sm transition-colors ${
                  settings.chartTimeRange === range
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}
              >
                {range}
              </button>
            ))}
          </div>

          {/* Toggle Renewable */}
          <button
            onClick={() => setShowRenewable(!showRenewable)}
            className={`px-3 py-1 text-sm rounded-lg transition-colors ${
              showRenewable ? 'bg-green-600 text-white' : 'bg-gray-800 text-gray-400'
            }`}
          >
            Renewable
          </button>

          {/* Export Button */}
          <button
            onClick={exportChart}
            className="flex items-center gap-2 px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-gray-300"
          >
            <Download className="h-4 w-4" />
            Export
          </button>
        </div>
      </div>

      <div className="h-[400px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={filteredData}>
            <defs>
              <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              {showRenewable && (
                <linearGradient id="colorRenewable" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              )}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" fontSize={12} />
            <YAxis stroke="#9ca3af" fontSize={12} tickFormatter={(value) => `${value} kW`} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#111827', 
                border: '1px solid #374151', 
                borderRadius: '8px' 
              }}
              formatter={(value: number, name: string) => [`${value} kW`, name]}
            />
            <Legend />
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
