/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Manmohan Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { useState } from 'react';
import { Menu, X, Home, BarChart3, Settings, TrendingUp, Zap } from 'lucide-react';
import Link from 'next/link';

const menuItems = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Optimization', href: '/optimization', icon: TrendingUp },
  { name: 'Energy', href: '/energy', icon: Zap },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export default function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
      >
        {isOpen ? <X className="h-6 w-6 text-gray-300" /> : <Menu className="h-6 w-6 text-gray-300" />}
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="fixed inset-0 bg-black/50" onClick={() => setIsOpen(false)} />
          <div className="fixed left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-800 p-6 overflow-y-auto">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xl font-bold text-gray-100">Menu</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700"
              >
                <X className="h-5 w-5 text-gray-300" />
              </button>
            </div>
            
            <nav className="space-y-2">
              {menuItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg bg-gray-800/50 hover:bg-gray-800 text-gray-300 hover:text-gray-100 transition-colors"
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      )}
    </>
  );
}
