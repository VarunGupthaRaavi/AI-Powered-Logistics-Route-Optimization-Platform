import React, { useState, useEffect, useCallback } from 'react';
import {
  Package,
  Clock,
  Truck,
  CheckCircle2,
  Weight,
  Plus,
  ArrowRight,
  Sparkles,
  MapPin,
  RefreshCw,
} from 'lucide-react';
import deliveryService from '../../services/deliveryService';
import StatCard from '../../components/dashboard/StatCard';
import DeliveriesPage from '../deliveries/DeliveriesPage';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    inTransit: 0,
    delivered: 0,
    totalWeight: 0,
  });

  const [recentDeliveries, setRecentDeliveries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchDashboardMetrics = useCallback(async () => {
    setIsLoading(true);
    try {
      // Fetch all deliveries for metrics overview
      const data = await deliveryService.getDeliveries({ page: 1, limit: 50 });
      const items = data.items || [];

      const total = data.total || items.length;
      const pending = items.filter((d) => d.delivery_status?.toLowerCase() === 'pending').length;
      const inTransit = items.filter((d) => d.delivery_status?.toLowerCase() === 'in_transit').length;
      const delivered = items.filter((d) => d.delivery_status?.toLowerCase() === 'delivered').length;
      const totalWeight = items.reduce((acc, curr) => acc + (curr.package_weight || 0), 0);

      setStats({
        total,
        pending,
        inTransit,
        delivered,
        totalWeight: Math.round(totalWeight * 10) / 10,
      });

      setRecentDeliveries(items.slice(0, 5));
    } catch (err) {
      console.error('Failed to load dashboard metrics:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardMetrics();
  }, [fetchDashboardMetrics]);

  return (
    <div className="p-6 space-y-8">
      {/* Dashboard Top Banner */}
      <div className="relative overflow-hidden p-6 rounded-3xl bg-gradient-to-r from-indigo-950 via-slate-900 to-indigo-950 border border-indigo-500/20 shadow-2xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 bg-indigo-500/10 border border-indigo-500/20 rounded-full text-indigo-300 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
              <span>RouteAI Fleet Intelligence Engine v2.4</span>
            </div>
            <h1 className="text-2xl font-extrabold text-slate-100">Logistics Operations Control Center</h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Real-time telemetry monitoring, automated Vehicle Routing Problem (VRP) optimization, and last-mile dispatch management.
            </p>
          </div>

          <button
            onClick={fetchDashboardMetrics}
            disabled={isLoading}
            className="flex items-center space-x-2 px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition-all w-fit"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh Telemetry</span>
          </button>
        </div>
      </div>

      {/* Statistics Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Orders"
          value={stats.total}
          icon={Package}
          color="indigo"
          trend="up"
          trendValue="+14.2%"
          subtitle="Registered orders"
        />
        <StatCard
          title="Pending Orders"
          value={stats.pending}
          icon={Clock}
          color="amber"
          trend="up"
          trendValue="+5.1%"
          subtitle="Awaiting VRP dispatch"
        />
        <StatCard
          title="In-Transit Fleet"
          value={stats.inTransit}
          icon={Truck}
          color="cyan"
          trend="up"
          trendValue="+8.4%"
          subtitle="Active on road"
        />
        <StatCard
          title="Completed"
          value={stats.delivered}
          icon={CheckCircle2}
          color="emerald"
          trend="up"
          trendValue="+18.9%"
          subtitle="Successfully delivered"
        />
        <StatCard
          title="Fleet Weight"
          value={`${stats.totalWeight} kg`}
          icon={Weight}
          color="purple"
          subtitle="Total cargo volume"
        />
      </div>

      {/* Main Delivery Table Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Package className="w-5 h-5 text-indigo-400" />
            Live Delivery Order Feed
          </h2>
        </div>

        {/* Embedded Full Delivery Data Grid */}
        <DeliveriesPage />
      </div>
    </div>
  );
}
