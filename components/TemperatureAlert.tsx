/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { AlertTriangle, X } from 'lucide-react';

interface TemperatureAlertProps {
  clusterName: string;
  temperature: number;
  location: string;
  onDismiss: () => void;
}

export default function TemperatureAlert({ 
  clusterName, 
  temperature, 
  location,
  onDismiss 
}: TemperatureAlertProps) {
  const severity = temperature > 85 ? 'critical' : 'warning';
  
  return (
    <div className={`fixed top-4 right-4 z-50 p-4 rounded-lg border-2 shadow-lg max-w-md animate-slide-in ${
      severity === 'critical' 
        ? 'bg-red-900/90 border-red-500' 
        : 'bg-yellow-900/90 border-yellow-500'
    }`}>
      <div className="flex items-start gap-3">
        <AlertTriangle className={`h-6 w-6 flex-shrink-0 ${
          severity === 'critical' ? 'text-red-400' : 'text-yellow-400'
        }`} />
        <div className="flex-1">
          <h4 className={`font-semibold ${
            severity === 'critical' ? 'text-red-100' : 'text-yellow-100'
          }`}>
            {severity === 'critical' ? '🚨 Critical Temperature Alert!' : '⚠️ Temperature Warning'}
          </h4>
          <p className="text-sm text-gray-300 mt-1">
            <strong>{clusterName}</strong> ({location}) is running at <strong>{temperature}°C</strong>
          </p>
          <p className="text-xs text-gray-400 mt-2">
            {severity === 'critical' 
              ? 'Immediate action required! Risk of hardware damage.' 
              : 'Monitor closely and consider improving cooling.'}
          </p>
        </div>
        <button 
          onClick={onDismiss}
          className="text-gray-400 hover:text-gray-200 transition-colors"
        >
          <X className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
}
