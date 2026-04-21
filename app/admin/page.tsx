/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { useState, useEffect } from 'react';
import { Users, CheckCircle, XCircle, Eye, Copy } from 'lucide-react';

interface Application {
  id: string;
  companyName: string;
  email: string;
  gpuTypes: string;
  monthlyEnergySpend: number;
  reason: string;
  clusterId: string;
  apiKey: string;
  expiresAt: string;
  status: string;
  createdAt: string;
}

export default function AdminPage() {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await fetch('/api/beta/signup');
      const data = await response.json();
      setApplications(data);
    } catch (error) {
      console.error('Failed to fetch:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-100">Admin Dashboard</h1>
            <p className="text-gray-400 mt-1">Manage beta applications and credentials</p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-blue-600/20 rounded-lg">
            <Users className="h-5 w-5 text-blue-400" />
            <span className="text-blue-300">{applications.length} Applications</span>
          </div>
        </div>

        <div className="space-y-6">
          {applications.map((app) => (
            <div key={app.id} className="bg-gray-900/50 border border-gray-800 rounded-xl p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-gray-100">{app.companyName}</h2>
                  <p className="text-gray-400">{app.email}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  app.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-green-500/20 text-green-400'
                }`}>
                  {app.status}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-500">GPU Types</p>
                  <p className="text-gray-300">{app.gpuTypes}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Monthly Spend</p>
                  <p className="text-gray-300">${app.monthlyEnergySpend.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Applied</p>
                  <p className="text-gray-300">{new Date(app.createdAt).toLocaleDateString()}</p>
                </div>
              </div>

              <div className="bg-gray-800/50 rounded-lg p-4 mb-4">
                <p className="text-sm text-gray-500 mb-2">Credentials</p>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <code className="flex-1 text-xs bg-gray-900 p-2 rounded text-gray-300">{app.clusterId}</code>
                    <button onClick={() => copyToClipboard(app.clusterId)} className="p-2 hover:bg-gray-700 rounded">
                      <Copy className="h-4 w-4 text-gray-400" />
                    </button>
                  </div>
                  <div className="flex items-center gap-2">
                    <code className="flex-1 text-xs bg-gray-900 p-2 rounded text-gray-300">{app.apiKey}</code>
                    <button onClick={() => copyToClipboard(app.apiKey)} className="p-2 hover:bg-gray-700 rounded">
                      <Copy className="h-4 w-4 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="flex gap-3">
                <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                  <CheckCircle className="h-4 w-4" />
                  Approve
                </button>
                <button className="px-4 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                  <XCircle className="h-4 w-4" />
                  Reject
                </button>
                <button className="px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 text-sm font-medium rounded-lg transition-colors flex items-center gap-2">
                  <Eye className="h-4 w-4" />
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
