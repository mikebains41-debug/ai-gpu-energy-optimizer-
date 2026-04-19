/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

type Theme = 'dark' | 'light';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
  settings: UserSettings;
  updateSettings: (settings: Partial<UserSettings>) => void;
}

interface UserSettings {
  refreshInterval: number;
  showNotifications: boolean;
  soundEnabled: boolean;
  chartTimeRange: '1h' | '24h' | '7d' | '30d';
  collapsedPanels: string[];
}

const defaultSettings: UserSettings = {
  refreshInterval: 30000,
  showNotifications: true,
  soundEnabled: false,
  chartTimeRange: '24h',
  collapsedPanels: []
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('dark');
  const [settings, setSettings] = useState<UserSettings>(defaultSettings);
  const [mounted, setMounted] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    setMounted(true);
    const savedTheme = localStorage.getItem('theme') as Theme;
    const savedSettings = localStorage.getItem('settings');
    
    if (savedTheme) setTheme(savedTheme);
    if (savedSettings) setSettings(JSON.parse(savedSettings));
  }, []);

  // Save to localStorage
  useEffect(() => {
    if (mounted) {
      localStorage.setItem('theme', theme);
      document.documentElement.classList.toggle('dark', theme === 'dark');
    }
  }, [theme, mounted]);

  useEffect(() => {
    if (mounted) {
      localStorage.setItem('settings', JSON.stringify(settings));
    }
  }, [settings, mounted]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const updateSettings = (newSettings: Partial<UserSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  // Prevent flash of wrong theme
  if (!mounted) return null;

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, settings, updateSettings }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
