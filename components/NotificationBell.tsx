/**
 * PROPRIETARY & CONFIDENTIAL
 * Copyright (c) 2026 Mike Bains. All Rights Reserved.
 * Contact: Mikebains41@gmail.com
 */
'use client';

import { Bell, X } from 'lucide-react';
import { useNotification } from '@/contexts/NotificationContext';
import { useState } from 'react';

interface Notification {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: string;
}

export default function NotificationBell() {
  const [isOpen, setIsOpen] = useState(false);
  const { notifications, removeNotification } = useNotification();

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success': return '🟢';
      case 'warning': return '⚠️';
      case 'error': return '🔴';
      case 'info': return 'ℹ️';
      default: return '📢';
    }
  };

  const notificationList = notifications as Notification[];

  if (!notificationList || notificationList.length === 0) return null;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
      >
        <Bell className="h-5 w-5 text-gray-300" />
        {notificationList.length > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {notificationList.length > 9 ? '9+' : notificationList.length}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-gray-900 border border-gray-700 rounded-lg shadow-xl z-50 max-h-96 overflow-y-auto">
          <div className="p-4 border-b border-gray-700 flex items-center justify-between">
            <h3 className="font-semibold text-gray-100">Notifications</h3>
            <button onClick={() => setIsOpen(false)} className="text-xs text-gray-400 hover:text-gray-200">
              <X className="h-4 w-4" />
            </button>
          </div>
          
          <div className="divide-y divide-gray-700">
            {notificationList.map((notification) => (
              <div
                key={notification.id}
                className="p-4 hover:bg-gray-800 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <span className="text-xl">{getNotificationIcon(notification.type)}</span>
                  <div className="flex-1">
                    <h4 className="text-sm font-semibold text-gray-100">
                      {notification.title}
                    </h4>
                    <p className="text-xs text-gray-500 mt-1">{notification.message}</p>
                    <p className="text-xs text-gray-600 mt-2">
                      {new Date(notification.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                  <button
                    onClick={() => removeNotification(notification.id)}
                    className="text-gray-500 hover:text-gray-300"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
