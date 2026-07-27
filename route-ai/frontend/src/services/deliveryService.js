import apiClient from '../api/client';

export const deliveryService = {
  getDeliveries: async (params = {}) => {
    const response = await apiClient.get('/deliveries', { params });
    return response.data;
  },

  getDeliveryById: async (id) => {
    const response = await apiClient.get(`/deliveries/${id}`);
    return response.data;
  },

  createDelivery: async (deliveryData) => {
    const response = await apiClient.post('/deliveries', deliveryData);
    return response.data;
  },

  updateDelivery: async (id, deliveryData) => {
    const response = await apiClient.put(`/deliveries/${id}`, deliveryData);
    return response.data;
  },

  deleteDelivery: async (id) => {
    const response = await apiClient.delete(`/deliveries/${id}`);
    return response.data;
  },
};

export default deliveryService;
