'use client';

import { useState, useEffect, useRef } from 'react';

// Use environment variable or default to Render backend
const API_URL = process.env.NEXT_PUBLIC_API_URL || 
  'https://ai-gpu-brain-v2.onrender.com';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 
  'wss://ai-gpu-brain-v2.onrender.com/ws';

interface ClusterData {
  id: string;
  name: string;
  gpu_utilization: number;
  memory_usage: number;
  temperature: number;
  power_draw: number;
  efficiency_score: number;
}

interface Recommendation {
  id: string;
  cluster_id: string;
  action: string;
  estimated_savings_monthly: number;
  priority: 'high' | 'medium' | 'low';
}

interface DashboardData {
  clusters: ClusterData[];
  recommendations: Recommendation[];
  total_power_mw: number;
  grid_carbon_intensity: number;
}

export function useOptimizationStream() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const pollIntervalRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    const connectWebSocket = () => {
      try {
        wsRef.current = new WebSocket(WS_URL);

        wsRef.current.onopen = () => {
          console.log('✅ Connected to AI Engine');
          setConnected(true);
        };
        
        wsRef.current.onmessage = (event) => {
          try {
            const newData = JSON.parse(event.data);
            // Skip ping messages
            if (newData.type === 'ping') return;
            setData(newData);
          } catch (error) {
            console.error('❌ Error parsing WebSocket message:', error);
          }
        };

        wsRef.current.onerror = (error) => {
          console.error('❌ WebSocket error:', error);
          setConnected(false);
        };

        wsRef.current.onclose = () => {
          console.log('🔌 WebSocket closed, reconnecting...');
          setConnected(false);
          reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
        };
      } catch (error) {
        console.error('❌ Failed to connect WebSocket:', error);
        setConnected(false);
        startPolling();
      }
    };

    const startPolling = () => {
      const fetchData = async () => {
        try {
          const response = await fetch(`${API_URL}/optimize`);
          const newData = await response.json();
          setData(newData);
          setConnected(true);
        } catch (error) {
          console.error('❌ Polling error:', error);
          setConnected(false);
        }
      };

      fetchData();
      pollIntervalRef.current = setInterval(fetchData, 5000);
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  return { data, connected };
}
