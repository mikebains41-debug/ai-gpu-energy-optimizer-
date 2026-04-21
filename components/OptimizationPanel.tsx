/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { Zap, Globe, Thermometer, Clock, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface Recommendation {
  id: string;
  cluster_id: string;
  action: string;
  estimated_savings_monthly: number;
  priority: 'high' | 'medium' | 'low';
}

interface OptimizationPanelProps {
  optimizations: Recommendation[];
}

const typeIcons: Record<string, any> = {
  scheduling: Clock,
  'load-balancing': Globe,
  cooling: Thermometer,
  power: Zap,
};

const priorityColors = {
  high: 'bg-red-500/10 text-red-400 border-red-500/20',
  medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  low: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
};

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

export default function OptimizationPanel({ optimizations }: OptimizationPanelProps) {
  // Default icon is Zap (power)
  const Icon = Zap;

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-100">AI Optimization Recommendations</h3>
        <span className="text-sm text-gray-400">{optimizations.length} opportunities</span>
      </div>
      <div className="space-y-4">
        {optimizations.map((opt) => (
          <div key={opt.id} className="group rounded-lg border border-gray-800 p-4 hover:border-gray-700 hover:bg-gray-800/50 transition-all cursor-pointer">
            <div className="flex items-start gap-4">
              <div className={cn("flex h-10 w-10 items-center justify-center rounded-lg", opt.priority === 'high' ? 'bg-red-500/10' : opt.priority === 'medium' ? 'bg-yellow-500/10' : 'bg-blue-500/10')}>
                <Icon className={cn("h-5 w-5", opt.priority === 'high' ? 'text-red-400' : opt.priority === 'medium' ? 'text-yellow-400' : 'text-blue-400')} />
              </div>
              <div className="flex-1">
                <div className="flex items-start justify-between gap-4 mb-2">
                  <p className="text-sm font-medium text-gray-100">{opt.action}</p>
                  <span className={cn("px-2 py-1 rounded-full text-xs border", priorityColors[opt.priority])}>{opt.priority}</span>
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-1 text-green-400">
                    <Zap className="h-4 w-4" />
                    <span className="font-medium">{formatCurrency(opt.estimated_savings_monthly)}/mo</span>
                  </div>
                </div>
              </div>
              <ArrowRight className="h-5 w-5 text-gray-600 group-hover:text-gray-400 transition-colors" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
