'use client';

import { useState } from 'react';
import { Menu, X, Bell, Zap } from 'lucide-react';
import Link from 'next/link';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Mobile Header */}
      <header className="lg:hidden bg-gray-900 border-b border-gray-800 px-4 py-3 flex items-center justify-between sticky top-0 z-40">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700"
        >
          <Menu className="h-6 w-6" />
        </button>
        
        <div className="flex items-center gap-2">
          <Zap className="h-6 w-6 text-blue-500" />
          <span className="text-lg font-bold text-gray-100">GPU Optimizer</span>
        </div>

        <button className="p-2 rounded-lg bg-gray-800 text-gray-300">
          <Bell className="h-5 w-5" />
        </button>
      </header>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <div 
          className="lg:hidden fixed inset-0 z-50 bg-black/50"
          onClick={() => setSidebarOpen(false)}
        >
          <div 
            className="absolute left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-800 p-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <span className="text-lg font-bold text-gray-100">Menu</span>
              <button
                onClick={() => setSidebarOpen(false)}
                className="p-2 rounded-lg text-gray-400 hover:bg-gray-800"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <nav className="space-y-2">
              <Link
                href="/dashboard"
                className="block px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800"
                onClick={() => setSidebarOpen(false)}
              >
                Dashboard
              </Link>
              <Link
                href="/analytics"
                className="block px-3 py-2 rounded-lg text-gray-300 hover:bg-gray-800"
                onClick={() => setSidebarOpen(false)}
              >
                Analytics
              </Link>
            </nav>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="p-4">
        {children}
      </main>
    </div>
  );
}
