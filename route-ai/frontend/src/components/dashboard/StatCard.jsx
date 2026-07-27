import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function StatCard({ title, value, icon: Icon, trend, trendValue, color = 'indigo', subtitle }) {
  const colorThemes = {
    indigo: {
      bg: 'bg-indigo-500/10',
      text: 'text-indigo-400',
      border: 'border-indigo-500/20',
      glow: 'shadow-indigo-500/5',
    },
    amber: {
      bg: 'bg-amber-500/10',
      text: 'text-amber-400',
      border: 'border-amber-500/20',
      glow: 'shadow-amber-500/5',
    },
    cyan: {
      bg: 'bg-cyan-500/10',
      text: 'text-cyan-400',
      border: 'border-cyan-500/20',
      glow: 'shadow-cyan-500/5',
    },
    emerald: {
      bg: 'bg-emerald-500/10',
      text: 'text-emerald-400',
      border: 'border-emerald-500/20',
      glow: 'shadow-emerald-500/5',
    },
    purple: {
      bg: 'bg-purple-500/10',
      text: 'text-purple-400',
      border: 'border-purple-500/20',
      glow: 'shadow-purple-500/5',
    },
  };

  const theme = colorThemes[color] || colorThemes.indigo;

  return (
    <div className={`p-5 bg-slate-900/60 border border-slate-800 rounded-2xl backdrop-blur-md shadow-lg ${theme.glow} hover:border-slate-700/80 transition-all group`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        <div className={`p-2.5 rounded-xl ${theme.bg} ${theme.text} border ${theme.border} group-hover:scale-110 transition-transform`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline justify-between">
        <h3 className="text-2xl font-bold text-slate-100 font-mono tracking-tight">{value}</h3>
        {trend && (
          <div className={`flex items-center space-x-1 text-xs font-semibold ${trend === 'up' ? 'text-emerald-400' : 'text-rose-400'}`}>
            {trend === 'up' ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
            <span>{trendValue}</span>
          </div>
        )}
      </div>

      {subtitle && <p className="mt-1 text-[11px] text-slate-500">{subtitle}</p>}
    </div>
  );
}
