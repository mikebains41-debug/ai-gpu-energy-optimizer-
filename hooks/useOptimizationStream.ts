'use client';

import { useState, useEffect, useRef } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 
  'https://ai-gpu-brain-v2.onrender.com';

interface DashboardData {
  clusters: any[];
  recommendations: any[];
  total_power_mw: number;
  grid_carbon_intensity: number;
}

export function useOptimizationStream() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [connected, setConnected] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    // Fetch data immediately
    fetchData();

    // Then fetch every 3 seconds
    intervalRef.current = setInterval(fetchData, 3000);

    async function fetchData() {
      try {
        const response = await fetch(`${API_URL}/optimize`);
        if (response.ok) {
          const newData = await response.json();
          setData(newData);
          setConnected(true);
        } else {
          setConnected(false);
        }
      } catch (error) {
        console.error('Fetch error:', error);
        setConnected(false);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return { data, connected };
}
