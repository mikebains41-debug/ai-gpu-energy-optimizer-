'use client';

import { useState } from 'react';
import { Menu, X } from 'lucide-react';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Mobile Header */}
      <header className="bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between">
        <button onClick={() => setSidebarOpen(true)} className="p-2">
          <Menu className="h-6 w-6 text-gray-300" />
        </button>
        <h1 className="text-lg font-bold text-gray-100">GPU Optimizer</h1>
        <div className="w-10" />
      </header>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 bg-black/50" onClick={() => setSidebarOpen(false)}>
          <div className="absolute left-0 top-0 h-full w-64 bg-gray-900 p-4" onClick={(e) => e.stopPropagation()}>
            <button onClick={() => setSidebarOpen(false)} className="mb-6">
              <X className="h-6 w-6 text-gray-300" />
            </button>
            <nav className="space-y-2">
              <a href="/dashboard" className="block px-3 py-2 text-gray-300 hover:bg-gray-800 rounded">Dashboard</a>
              <a href="/analytics" className="block px-3 py-2 text-gray-300 hover:bg-gray-800 rounded">Analytics</a>
            </nav>
          </div>
        </div>
      )}

      <main className="p-4">{children}</main>
    </div>
  );
}
