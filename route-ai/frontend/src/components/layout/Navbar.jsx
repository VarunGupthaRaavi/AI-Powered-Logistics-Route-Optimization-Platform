import React from 'react';
import { useLocation } from 'react-router-dom';
import { Menu, Search, Bell, Activity, Sparkles } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Navbar({ toggleMobileSidebar }) {
  const location = useLocation();
  const { user } = useAuth();

  const getPageTitle = () => {
    const path = location.pathname;
    if (path.includes('/deliveries')) return 'Delivery Management';
    if (path.includes('/drivers')) return 'Fleet Drivers';
    if (path.includes('/vehicles')) return 'Fleet Vehicles';
    if (path.includes('/routes')) return 'Route Planning & Optimization';
    if (path.includes('/analytics')) return 'Logistics Telemetry Analytics';
    if (path.includes('/ai-assistant')) return 'AI Route Assistant';
    if (path.includes('/settings')) return 'System Settings';
    return 'Operations Dashboard';
  };

  return (
    <header className="h-16 bg-slate-900/80 border-b border-slate-800/80 backdrop-blur-md sticky top-0 z-30 px-4 md:px-6 flex items-center justify-between">
      {/* Left: Mobile Toggle & Breadcrumb */}
      <div className="flex items-center space-x-3">
        <button
          onClick={toggleMobileSidebar}
          className="md:hidden p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-500 hidden sm:inline">Platform /</span>
          <h2 className="text-sm font-bold text-slate-100">{getPageTitle()}</h2>
        </div>
      </div>

      {/* Right: Quick Search, Status Indicator, Notifications */}
      <div className="flex items-center space-x-3">
        {/* Live System Status Pill */}
        <div className="hidden lg:flex items-center space-x-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 text-xs">
          <Activity className="w-3.5 h-3.5 animate-pulse" />
          <span className="text-[11px] font-semibold">Telemetry Online</span>
        </div>

        {/* Global Quick Search Bar */}
        <div className="relative hidden md:block w-48 lg:w-64">
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Quick search... (Ctrl + K)"
            className="w-full pl-9 pr-3 py-1.5 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-200 text-xs focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Notifications Icon */}
        <button
          className="relative p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 rounded-xl transition-colors"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-indigo-500 rounded-full ring-2 ring-slate-900" />
        </button>

        {/* AI Assistant Quick Pill */}
        <div className="flex items-center space-x-1.5 px-3 py-1 bg-gradient-to-r from-indigo-600/20 to-violet-600/20 border border-indigo-500/30 rounded-xl text-indigo-300 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden sm:inline">AI v2.4</span>
        </div>
      </div>
    </header>
  );
}
