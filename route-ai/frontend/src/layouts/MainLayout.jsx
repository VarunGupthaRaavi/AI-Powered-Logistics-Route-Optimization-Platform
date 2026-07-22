import React from 'react';
import { Outlet, Link } from 'react-router-dom';

export default function MainLayout() {
  return (
    <div className="flex h-screen bg-slate-900 text-slate-100">
      <aside className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
        <div className="p-4 border-b border-slate-700">
          <h1 className="text-xl font-bold text-sky-400">RouteAI Platform</h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/dashboard" className="block px-3 py-2 rounded hover:bg-slate-700">Dashboard</Link>
          <Link to="/deliveries" className="block px-3 py-2 rounded hover:bg-slate-700">Deliveries</Link>
          <Link to="/drivers" className="block px-3 py-2 rounded hover:bg-slate-700">Drivers</Link>
          <Link to="/vehicles" className="block px-3 py-2 rounded hover:bg-slate-700">Vehicles</Link>
          <Link to="/routes" className="block px-3 py-2 rounded hover:bg-slate-700">Routes</Link>
          <Link to="/analytics" className="block px-3 py-2 rounded hover:bg-slate-700">Analytics</Link>
          <Link to="/ai-assistant" className="block px-3 py-2 rounded hover:bg-slate-700">AI Assistant</Link>
          <Link to="/settings" className="block px-3 py-2 rounded hover:bg-slate-700">Settings</Link>
        </nav>
      </aside>
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}
