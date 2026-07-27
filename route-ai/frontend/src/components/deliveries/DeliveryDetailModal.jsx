import React from 'react';
import { X, Package, MapPin, Calendar, Clock, Tag, User, Truck, ShieldAlert } from 'lucide-react';

export default function DeliveryDetailModal({ delivery, onClose }) {
  if (!delivery) return null;

  const getStatusBadge = (status) => {
    const styles = {
      pending: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      scheduled: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
      assigned: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
      in_transit: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
      delivered: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      failed: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
      cancelled: 'bg-gray-500/10 text-gray-400 border-gray-500/20',
    };
    return styles[delivery.delivery_status?.toLowerCase()] || styles.pending;
  };

  const getPriorityBadge = (priority) => {
    const styles = {
      low: 'bg-gray-500/10 text-gray-400',
      normal: 'bg-blue-500/10 text-blue-400',
      high: 'bg-orange-500/10 text-orange-400',
      urgent: 'bg-rose-500/10 text-rose-400 font-semibold',
    };
    return styles[priority?.toLowerCase()] || styles.normal;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100">Delivery Details</h2>
              <p className="text-xs text-slate-400">Order ID #{delivery.delivery_id}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-6 max-h-[80vh] overflow-y-auto">
          {/* Status & Priority Badges */}
          <div className="flex items-center justify-between p-4 bg-slate-950/40 rounded-xl border border-slate-800/80">
            <div>
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Status</span>
              <span className={`inline-flex items-center px-3 py-1 text-xs font-medium rounded-full border ${getStatusBadge(delivery.delivery_status)}`}>
                {delivery.delivery_status?.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            <div>
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Priority</span>
              <span className={`inline-flex items-center px-3 py-1 text-xs font-medium rounded-full ${getPriorityBadge(delivery.priority)}`}>
                {delivery.priority?.toUpperCase()}
              </span>
            </div>
            <div>
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Package Weight</span>
              <span className="text-sm font-semibold text-slate-200">{delivery.package_weight} kg</span>
            </div>
          </div>

          {/* Locations */}
          <div className="space-y-4">
            <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Route Waypoints</h3>
            <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800 space-y-4">
              <div className="flex items-start space-x-3">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mt-0.5">
                  <MapPin className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-xs font-medium text-emerald-400 block">Pickup Location</span>
                  <p className="text-sm text-slate-200">{delivery.pickup_location}</p>
                </div>
              </div>
              <div className="border-l-2 border-dashed border-slate-800 ml-4 h-4" />
              <div className="flex items-start space-x-3">
                <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 mt-0.5">
                  <MapPin className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-xs font-medium text-rose-400 block">Drop-off Destination</span>
                  <p className="text-sm text-slate-200">{delivery.drop_location}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Customer & Assignments */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-slate-400 mb-2">
                <User className="w-4 h-4" />
                <span className="text-xs font-medium uppercase tracking-wider">Customer ID</span>
              </div>
              <p className="text-sm font-semibold text-slate-200">Customer #{delivery.customer_id}</p>
            </div>
            <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800">
              <div className="flex items-center space-x-2 text-slate-400 mb-2">
                <Truck className="w-4 h-4" />
                <span className="text-xs font-medium uppercase tracking-wider">Assigned Fleet</span>
              </div>
              <p className="text-sm text-slate-300">
                Driver ID: <span className="text-slate-100 font-medium">{delivery.driver_id || 'Unassigned'}</span> | Vehicle ID: <span className="text-slate-100 font-medium">{delivery.vehicle_id || 'Unassigned'}</span>
              </p>
            </div>
          </div>

          {/* Time Windows & Created At */}
          <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400 flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5" /> Order Created:</span>
              <span className="text-slate-200 font-mono">{new Date(delivery.created_at).toLocaleString()}</span>
            </div>
            {delivery.delivery_window_start && (
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" /> Window Start:</span>
                <span className="text-slate-200 font-mono">{new Date(delivery.delivery_window_start).toLocaleString()}</span>
              </div>
            )}
            {delivery.delivery_window_end && (
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" /> Window End:</span>
                <span className="text-slate-200 font-mono">{new Date(delivery.delivery_window_end).toLocaleString()}</span>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end px-6 py-4 bg-slate-950/60 border-t border-slate-800">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
