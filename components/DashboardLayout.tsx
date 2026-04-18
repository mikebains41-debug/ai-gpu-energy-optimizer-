/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { ReactNode } from 'react';
import { Cpu, Zap, Thermometer, TrendingUp, Menu, BarChart3, Settings, Bell } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

interface DashboardLayoutProps { children: ReactNode; }

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Analytics', href: '/analytics', icon: TrendingUp },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="sticky top-0 z-50 w-full border-b border-gray-800 bg-gray-950/80 backdrop-blur-xl">
        <div className="flex h-16 items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-gray-800 rounded-lg lg:hidden"><Menu className="h-5 w-5" /></button>
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-purple-600"><Cpu className="h-5 w-5 text-white" /></div>
              <div>
                <h1 className="text-lg sm:text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">AI + GPU + Energy Optimization Platform</h1>
                <p className="text-xs text-gray-400">Infrastructure Management</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 hover:bg-gray-800 rounded-lg"><Bell className="h-5 w-5 text-gray-400" /><span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500"></span></button>
            <div className="flex items-center gap-3 pl-4 border-l border-gray-800">
              <div className="text-right hidden sm:block"><p className="text-sm font-medium">Admin User</p><p className="text-xs text-gray-400">Data Center Ops</p></div>
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-green-400 to-blue-500" />
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0 lg:pt-16">
          <div className="flex flex-1 flex-col border-r border-gray-800 bg-gray-950 px-4 py-6">
            <nav className="flex flex-1 flex-col gap-2">
              {navigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link key={item.name} href={item.href} className={cn('flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors', isActive ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'text-gray-400 hover:bg-gray-800 hover:text-gray-100')}>
                    <item.icon className="h-5 w-5" />{item.name}
                  </Link>
                );
              })}
            </nav>
            <div className="mt-auto space-y-4">
              <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
                <div className="flex items-center gap-2 mb-2"><Zap className="h-4 w-4 text-yellow-500" /><span className="text-xs font-medium text-gray-400">Total Power</span></div>
                <p className="text-2xl font-bold text-gray-100">3.97 MW</p>
                <p className="text-xs text-green-400 mt-1">↓ 12% from last hour</p>
              </div>
              <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
                <div className="flex items-center gap-2 mb-2"><Thermometer className="h-4 w-4 text-orange-500" /><span className="text-xs font-medium text-gray-400">Avg Temperature</span></div>
                <p className="text-2xl font-bold text-gray-100">74.8°C</p>
                <p className="text-xs text-yellow-400 mt-1">↑ 2° from baseline</p>
              </div>
            </div>
          </div>
        </aside>
        <main className="flex-1 lg:pl-64"><div className="p-6 lg:p-8">{children}</div></main>
      </div>
    </div>
  );
}
