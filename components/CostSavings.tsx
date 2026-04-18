/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { DollarSign, Leaf, TrendingDown } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';

interface CostSavingsProps { totalSavings: number; carbonReduction: number; }

export default function CostSavings({ totalSavings, carbonReduction }: CostSavingsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Annual Savings */}
      <div className="rounded-xl border border-green-500/20 bg-gradient-to-br from-green-950/50 to-gray-900/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-green-500/10">
            <DollarSign className="h-6 w-6 text-green-400" />
          </div>
          <div>
            <p className="text-sm text-gray-400">Annual Savings</p>
            <p className="text-3xl font-bold text-green-400">
              {formatCurrency(totalSavings)}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <TrendingDown className="h-4 w-4 text-green-400" />
          <span className="text-green-400 font-medium">32%</span>
          <span className="text-gray-500">reduction in energy costs</span>
        </div>
      </div>

      {/* CO2 Reduction */}
      <div className="rounded-xl border border-blue-500/20 bg-gradient-to-br from-blue-950/50 to-gray-900/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-500/10">
            <Leaf className="h-6 w-6 text-blue-400" />
          </div>
          <div>
            <p className="text-sm text-gray-400">CO₂ Reduction</p>
            <p className="text-3xl font-bold text-blue-400">
              {carbonReduction.toLocaleString()} kg
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-400">Equivalent to</span>
          <span className="text-blue-400 font-medium">784 trees</span>
          <span className="text-gray-500">planted this year</span>
        </div>
      </div>

      {/* Efficiency Score */}
      <div className="rounded-xl border border-purple-500/20 bg-gradient-to-br from-purple-950/50 to-gray-900/50 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-500/10">
            <TrendingDown className="h-6 w-6 text-purple-400" />
          </div>
          <div>
            <p className="text-sm text-gray-400">Efficiency Score</p>
            <p className="text-3xl font-bold text-purple-400">
              94.2%
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-purple-400 font-medium">Top 5%</span>
          <span className="text-gray-500">of data centers globally</span>
        </div>
      </div>
    </div>
  );
}
