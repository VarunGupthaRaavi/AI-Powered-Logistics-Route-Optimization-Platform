import React, { useState, useEffect } from 'react';
import { X, Package, MapPin, AlertCircle, Loader2 } from 'lucide-react';

export default function DeliveryFormModal({ isOpen, onClose, onSubmit, delivery = null, isLoading = false }) {
  const isEditMode = !!delivery;

  const [formData, setFormData] = useState({
    customer_id: 1,
    pickup_location: '',
    drop_location: '',
    package_weight: 1.0,
    priority: 'normal',
    delivery_status: 'pending',
  });

  const [errors, setErrors] = useState({});
  const [globalError, setGlobalError] = useState('');

  useEffect(() => {
    if (delivery) {
      setFormData({
        customer_id: delivery.customer_id || 1,
        pickup_location: delivery.pickup_location || '',
        drop_location: delivery.drop_location || '',
        package_weight: delivery.package_weight || 1.0,
        priority: delivery.priority || 'normal',
        delivery_status: delivery.delivery_status || 'pending',
      });
    } else {
      setFormData({
        customer_id: 1,
        pickup_location: '',
        drop_location: '',
        package_weight: 1.0,
        priority: 'normal',
        delivery_status: 'pending',
      });
    }
    setErrors({});
    setGlobalError('');
  }, [delivery, isOpen]);

  if (!isOpen) return null;

  const validateForm = () => {
    const newErrors = {};

    // 1. Pickup Location Validation
    if (!formData.pickup_location || formData.pickup_location.trim().length < 3) {
      newErrors.pickup_location = 'Pickup location must be at least 3 characters long.';
    }

    // 2. Drop Location Validation
    if (!formData.drop_location || formData.drop_location.trim().length < 3) {
      newErrors.drop_location = 'Drop-off destination must be at least 3 characters long.';
    }

    // 3. Cross-field Validation: Identical addresses check
    if (
      formData.pickup_location &&
      formData.drop_location &&
      formData.pickup_location.trim().toLowerCase() === formData.drop_location.trim().toLowerCase()
    ) {
      newErrors.drop_location = 'Drop-off destination cannot be identical to pickup location.';
    }

    // 4. Package Weight Validation
    const weight = parseFloat(formData.package_weight);
    if (isNaN(weight) || weight <= 0) {
      newErrors.package_weight = 'Package weight must be greater than 0 kg.';
    } else if (weight > 1000) {
      newErrors.package_weight = 'Package weight cannot exceed 1000 kg.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'customer_id' || name === 'package_weight' ? parseFloat(value) || value : value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setGlobalError('');

    if (!validateForm()) {
      return;
    }

    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Package className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100">
                {isEditMode ? `Update Delivery #${delivery.delivery_id}` : 'Create Delivery Order'}
              </h2>
              <p className="text-xs text-slate-400">
                {isEditMode ? 'Modify delivery status and waypoint details' : 'Enter package dimensions and destination coordinates'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {globalError && (
            <div className="flex items-center space-x-2 p-3 text-xs text-rose-400 bg-rose-500/10 border border-rose-500/20 rounded-xl">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{globalError}</span>
            </div>
          )}

          {/* Customer ID & Package Weight */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Customer ID</label>
              <input
                type="number"
                name="customer_id"
                min="1"
                required
                value={formData.customer_id}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Package Weight (kg)</label>
              <input
                type="number"
                name="package_weight"
                step="0.1"
                min="0.1"
                max="1000"
                required
                value={formData.package_weight}
                onChange={handleChange}
                className={`w-full px-3.5 py-2.5 bg-slate-950/60 border rounded-xl text-slate-100 text-sm focus:outline-none ${
                  errors.package_weight ? 'border-rose-500' : 'border-slate-800 focus:border-indigo-500'
                }`}
              />
              {errors.package_weight && (
                <p className="mt-1 text-[11px] text-rose-400">{errors.package_weight}</p>
              )}
            </div>
          </div>

          {/* Pickup Location */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Pickup Location Address</label>
            <div className="relative">
              <MapPin className="w-4 h-4 text-emerald-400 absolute left-3.5 top-3" />
              <input
                type="text"
                name="pickup_location"
                required
                placeholder="e.g. Central Depot Hub, Hyderabad"
                value={formData.pickup_location}
                onChange={handleChange}
                className={`w-full pl-10 pr-3.5 py-2.5 bg-slate-950/60 border rounded-xl text-slate-100 text-sm focus:outline-none ${
                  errors.pickup_location ? 'border-rose-500' : 'border-slate-800 focus:border-indigo-500'
                }`}
              />
            </div>
            {errors.pickup_location && (
              <p className="mt-1 text-[11px] text-rose-400">{errors.pickup_location}</p>
            )}
          </div>

          {/* Drop Location */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">Drop-off Destination Address</label>
            <div className="relative">
              <MapPin className="w-4 h-4 text-rose-400 absolute left-3.5 top-3" />
              <input
                type="text"
                name="drop_location"
                required
                placeholder="e.g. Hitec City Phase 2, Hyderabad"
                value={formData.drop_location}
                onChange={handleChange}
                className={`w-full pl-10 pr-3.5 py-2.5 bg-slate-950/60 border rounded-xl text-slate-100 text-sm focus:outline-none ${
                  errors.drop_location ? 'border-rose-500' : 'border-slate-800 focus:border-indigo-500'
                }`}
              />
            </div>
            {errors.drop_location && (
              <p className="mt-1 text-[11px] text-rose-400">{errors.drop_location}</p>
            )}
          </div>

          {/* Priority & Status */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1.5">Order Priority</label>
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                className="w-full px-3.5 py-2.5 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
              >
                <option value="low">Low</option>
                <option value="normal">Normal</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
            </div>

            {isEditMode && (
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1.5">Delivery Status</label>
                <select
                  name="delivery_status"
                  value={formData.delivery_status}
                  onChange={handleChange}
                  className="w-full px-3.5 py-2.5 bg-slate-950/60 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:border-indigo-500"
                >
                  <option value="pending">Pending</option>
                  <option value="scheduled">Scheduled</option>
                  <option value="assigned">Assigned</option>
                  <option value="in_transit">In Transit</option>
                  <option value="delivered">Delivered</option>
                  <option value="failed">Failed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 text-xs font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex items-center space-x-2 px-5 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 rounded-xl transition-all shadow-lg shadow-indigo-600/30"
            >
              {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
              <span>{isEditMode ? 'Save Changes' : 'Create Delivery'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
