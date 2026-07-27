import React, { useState, useEffect, useCallback } from 'react';
import {
  Package,
  Plus,
  Search,
  Filter,
  ArrowUpDown,
  Eye,
  Edit2,
  Trash2,
  ChevronLeft,
  ChevronRight,
  Loader2,
  AlertCircle,
  CheckCircle2,
  MapPin,
} from 'lucide-react';
import deliveryService from '../../services/deliveryService';
import { useAuth } from '../../context/AuthContext';

import DeliveryDetailModal from '../../components/deliveries/DeliveryDetailModal';
import DeliveryFormModal from '../../components/deliveries/DeliveryFormModal';
import DeleteConfirmModal from '../../components/deliveries/DeleteConfirmModal';

export default function DeliveriesPage() {
  const { user } = useAuth();

  // State Declarations
  const [deliveries, setDeliveries] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);

  // Filters & Search State
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [sortField, setSortField] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');

  // UI Feedback States
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [toastMessage, setToastMessage] = useState('');

  // Modal Control States
  const [selectedDelivery, setSelectedDelivery] = useState(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [editingDelivery, setEditingDelivery] = useState(null);
  const [deletingDeliveryId, setDeletingDeliveryId] = useState(null);

  // Fetch Deliveries API Call
  const fetchDeliveries = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const params = {
        page,
        limit,
        status: statusFilter || undefined,
        priority: priorityFilter || undefined,
        search: search.trim() || undefined,
        sort: sortField,
        order: sortOrder,
      };
      const data = await deliveryService.getDeliveries(params);
      setDeliveries(data.items || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch delivery records.');
    } finally {
      setIsLoading(false);
    }
  }, [page, limit, statusFilter, priorityFilter, search, sortField, sortOrder]);

  useEffect(() => {
    fetchDeliveries();
  }, [fetchDeliveries]);

  // Toast Helper
  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 4000);
  };

  // Handlers for Modals
  const handleOpenCreateForm = () => {
    setEditingDelivery(null);
    setIsFormModalOpen(true);
  };

  const handleOpenEditForm = (delivery) => {
    setEditingDelivery(delivery);
    setIsFormModalOpen(true);
  };

  const handleOpenDetailModal = (delivery) => {
    setSelectedDelivery(delivery);
    setIsDetailModalOpen(true);
  };

  const handleOpenDeleteModal = (deliveryId) => {
    setDeletingDeliveryId(deliveryId);
    setIsDeleteModalOpen(true);
  };

  // Form Submit Handler (Create & Update)
  const handleFormSubmit = async (formData) => {
    setIsSubmitting(true);
    setError('');
    try {
      if (editingDelivery) {
        await deliveryService.updateDelivery(editingDelivery.delivery_id, formData);
        showToast(`Delivery #${editingDelivery.delivery_id} updated successfully.`);
      } else {
        await deliveryService.createDelivery(formData);
        showToast('New delivery order created successfully.');
      }
      setIsFormModalOpen(false);
      fetchDeliveries();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save delivery order.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Delete Handler
  const handleDeleteConfirm = async () => {
    if (!deletingDeliveryId) return;
    setIsSubmitting(true);
    try {
      await deliveryService.deleteDelivery(deletingDeliveryId);
      showToast(`Delivery #${deletingDeliveryId} deleted successfully.`);
      setIsDeleteModalOpen(false);
      fetchDeliveries();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete delivery order.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Status Badge Helper
  const getStatusBadgeClass = (statusStr) => {
    const s = statusStr?.toLowerCase();
    if (s === 'delivered') return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
    if (s === 'in_transit') return 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
    if (s === 'assigned') return 'bg-purple-500/10 text-purple-400 border-purple-500/20';
    if (s === 'scheduled') return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
    if (s === 'failed') return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
    return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
  };

  const totalPages = Math.ceil(total / limit) || 1;

  return (
    <div className="p-6 space-y-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-5 right-5 z-50 flex items-center space-x-2 px-4 py-3 bg-emerald-950/90 text-emerald-300 border border-emerald-500/30 rounded-xl shadow-2xl animate-bounce">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <span className="text-xs font-medium">{toastMessage}</span>
        </div>
      )}

      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Package className="w-7 h-7 text-indigo-400" />
            Delivery Management
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage last-mile package orders, track statuses, and dispatch fleet operations.
          </p>
        </div>

        <button
          onClick={handleOpenCreateForm}
          className="flex items-center space-x-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl transition-all shadow-lg shadow-indigo-600/30 w-fit"
        >
          <Plus className="w-4 h-4" />
          <span>New Delivery Order</span>
        </button>
      </div>

      {/* Global Error Banner */}
      {error && (
        <div className="flex items-center space-x-3 p-4 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-rose-400 text-xs">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Search, Filter & Controls Bar */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3 bg-slate-900/60 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        {/* Search Bar */}
        <div className="md:col-span-5 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search by pickup or drop location (e.g. Hyderabad)..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="w-full pl-10 pr-3 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 text-xs focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Status Filter */}
        <div className="md:col-span-2">
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="w-full px-3 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-300 text-xs focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Statuses</option>
            <option value="pending">Pending</option>
            <option value="scheduled">Scheduled</option>
            <option value="assigned">Assigned</option>
            <option value="in_transit">In Transit</option>
            <option value="delivered">Delivered</option>
            <option value="failed">Failed</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div className="md:col-span-2">
          <select
            value={priorityFilter}
            onChange={(e) => {
              setPriorityFilter(e.target.value);
              setPage(1);
            }}
            className="w-full px-3 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-300 text-xs focus:outline-none focus:border-indigo-500"
          >
            <option value="">All Priorities</option>
            <option value="low">Low</option>
            <option value="normal">Normal</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        {/* Sorting Controls */}
        <div className="md:col-span-3 flex items-center space-x-2">
          <select
            value={sortField}
            onChange={(e) => setSortField(e.target.value)}
            className="w-full px-3 py-2 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-300 text-xs focus:outline-none focus:border-indigo-500"
          >
            <option value="created_at">Sort: Created Date</option>
            <option value="package_weight">Sort: Weight</option>
            <option value="priority">Sort: Priority</option>
            <option value="delivery_id">Sort: Delivery ID</option>
          </select>

          <button
            onClick={() => setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'))}
            className="p-2 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-300 hover:text-slate-100 transition-colors"
            title={`Sort Direction: ${sortOrder.toUpperCase()}`}
          >
            <ArrowUpDown className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Deliveries Data Table */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl backdrop-blur-md">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20 text-slate-400 space-y-3">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
            <span className="text-xs font-medium">Loading deliveries data...</span>
          </div>
        ) : deliveries.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-slate-400 space-y-3">
            <Package className="w-12 h-12 text-slate-600" />
            <p className="text-sm font-semibold text-slate-300">No delivery orders found</p>
            <p className="text-xs text-slate-500">Try adjusting your search terms or filters.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-950/50 border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
                  <th className="py-3.5 px-4">Order ID</th>
                  <th className="py-3.5 px-4">Pickup Location</th>
                  <th className="py-3.5 px-4">Drop-off Destination</th>
                  <th className="py-3.5 px-4">Weight</th>
                  <th className="py-3.5 px-4">Priority</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {deliveries.map((delivery) => (
                  <tr key={delivery.delivery_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-indigo-400 font-semibold">
                      #{delivery.delivery_id}
                    </td>
                    <td className="py-3.5 px-4 max-w-xs truncate">
                      <div className="flex items-center space-x-1.5">
                        <MapPin className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                        <span className="truncate">{delivery.pickup_location}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 max-w-xs truncate">
                      <div className="flex items-center space-x-1.5">
                        <MapPin className="w-3.5 h-3.5 text-rose-400 flex-shrink-0" />
                        <span className="truncate">{delivery.drop_location}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 font-medium">{delivery.package_weight} kg</td>
                    <td className="py-3.5 px-4 uppercase text-[10px] font-semibold text-slate-400">
                      {delivery.priority}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 text-[10px] font-semibold rounded-full border ${getStatusBadgeClass(delivery.delivery_status)}`}>
                        {delivery.delivery_status?.replace('_', ' ').toUpperCase()}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => handleOpenDetailModal(delivery)}
                          className="p-1.5 text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10 rounded-lg transition-colors"
                          title="View Details"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleOpenEditForm(delivery)}
                          className="p-1.5 text-slate-400 hover:text-amber-400 hover:bg-amber-500/10 rounded-lg transition-colors"
                          title="Edit Order"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleOpenDeleteModal(delivery.delivery_id)}
                          className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
                          title="Delete Order (Admin)"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Bar */}
        <div className="flex items-center justify-between px-6 py-4 bg-slate-950/40 border-t border-slate-800 text-xs text-slate-400">
          <div>
            Showing <span className="font-semibold text-slate-200">{deliveries.length}</span> of{' '}
            <span className="font-semibold text-slate-200">{total}</span> total deliveries
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page <= 1 || isLoading}
              className="p-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 rounded-xl transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            <span className="text-slate-300 font-medium">
              Page {page} of {totalPages}
            </span>

            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page >= totalPages || isLoading}
              className="p-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-300 rounded-xl transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Modals */}
      <DeliveryDetailModal
        delivery={selectedDelivery}
        onClose={() => setIsDetailModalOpen(false)}
      />

      <DeliveryFormModal
        isOpen={isFormModalOpen}
        onClose={() => setIsFormModalOpen(false)}
        onSubmit={handleFormSubmit}
        delivery={editingDelivery}
        isLoading={isSubmitting}
      />

      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleDeleteConfirm}
        deliveryId={deletingDeliveryId}
        isLoading={isSubmitting}
      />
    </div>
  );
}
