import { useEffect, useState } from 'react';

export interface StreamData {
  clusters: any[];
  recommendations: any[];
  grid_carbon_intensity: number;
  total_power_mw: number;
  avg_utilization: number;
  timestamp: string;
}

export function useOptimizationStream() {
  const [data, setData] = useState<StreamData | null>(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Point to your AI Engine URL
    // Note: If your AI Engine is hosted elsewhere, change 'localhost:8000' to that URL
    const ws = new WebSocket('ws://localhost:8000/ws/stream');
    
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    
    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData(parsed);
      } catch (e) {
        console.error('WebSocket parse error:', e);
      }
    };

    return () => ws.close();
  }, []);

  return { data, connected };
}
