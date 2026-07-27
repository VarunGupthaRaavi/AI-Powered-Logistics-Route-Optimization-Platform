import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  Users,
  Truck,
  Navigation,
  BarChart3,
  Bot,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Sidebar({ isCollapsed, toggleSidebar, isMobileOpen, closeMobileSidebar }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Deliveries', path: '/deliveries', icon: Package, badge: 'Active' },
    { name: 'Drivers', path: '/drivers', icon: Users },
    { name: 'Vehicles', path: '/vehicles', icon: Truck },
    { name: 'Routes', path: '/routes', icon: Navigation },
    { name: 'Analytics', path: '/analytics', icon: BarChart3 },
    { name: 'AI Assistant', path: '/ai-assistant', icon: Bot, highlight: true },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile Drawer Overlay Backdrop */}
      {isMobileOpen && (
        <div
          onClick={closeMobileSidebar}
          className="fixed inset-0 z-40 bg-black/70 backdrop-blur-sm md:hidden transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 flex flex-col bg-slate-900 border-r border-slate-800/80 transition-all duration-300 ${
          isCollapsed ? 'w-20' : 'w-64'
        } ${isMobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        {/* Brand Header */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-slate-800/80 bg-slate-950/40">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 text-white shadow-lg shadow-indigo-600/30 flex-shrink-0">
              <Navigation className="w-5 h-5" />
            </div>
            {!isCollapsed && (
              <div className="flex flex-col">
                <span className="text-base font-extrabold bg-gradient-to-r from-slate-100 via-indigo-200 to-indigo-400 bg-clip-text text-transparent tracking-tight">
                  RouteAI
                </span>
                <span className="text-[10px] font-medium text-slate-400 tracking-wider uppercase">
                  Logistics Platform
                </span>
              </div>
            )}
          </div>

          {/* Desktop Toggle Collapse Button */}
          <button
            onClick={toggleSidebar}
            className="hidden md:flex p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto custom-scrollbar">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={closeMobileSidebar}
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all group ${
                  isActive
                    ? 'bg-indigo-600/15 text-indigo-400 border border-indigo-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon
                    className={`w-4 h-4 flex-shrink-0 transition-transform group-hover:scale-110 ${
                      isActive ? 'text-indigo-400' : 'text-slate-400 group-hover:text-slate-200'
                    }`}
                  />
                  {!isCollapsed && <span>{item.name}</span>}
                </div>

                {!isCollapsed && item.badge && (
                  <span className="px-2 py-0.5 text-[10px] font-semibold rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* User Profile Footer */}
        <div className="p-3 border-t border-slate-800/80 bg-slate-950/40">
          <div
            className={`flex items-center ${
              isCollapsed ? 'justify-center' : 'justify-between'
            } p-2 rounded-xl bg-slate-800/40 border border-slate-800`}
          >
            <div className="flex items-center space-x-3 overflow-hidden">
              <div className="w-8 h-8 rounded-lg bg-indigo-600/20 border border-indigo-500/30 text-indigo-400 flex items-center justify-center font-bold text-xs flex-shrink-0">
                {user?.name?.[0] || 'U'}
              </div>
              {!isCollapsed && (
                <div className="flex flex-col truncate">
                  <span className="text-xs font-semibold text-slate-200 truncate">{user?.name || 'Dispatcher Admin'}</span>
                  <span className="text-[10px] text-indigo-400 font-medium flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" /> {user?.role || 'Admin'}
                  </span>
                </div>
              )}
            </div>

            {!isCollapsed && (
              <button
                onClick={logout}
                className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                title="Log Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </aside>
    </>
  );
}
