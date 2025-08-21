
import axios from 'axios';
import { State, County, Status, Agency, ApiFilters } from '../types';

const API_URL = import.meta.env.VITE_REACT_APP_API_URL || 'http://localhost:5000';

const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const apiService = {
  async getStates(): Promise<State[]> {
    try {
      const response = await axios.get<State[]>(`${API_URL}/api/states`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getCounties(): Promise<County[]> {
    try {
      const url = `${API_URL}/api/counties`;
      const response = await axios.get<County[]>(url);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getStatus(): Promise<Status[]> {
    try {
      const url = `${API_URL}/api/status`;
      const response = await axios.get<Status[]>(url);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async getAgencies(filters?: ApiFilters): Promise<Agency[]> {
    try {
      await delay(400);
      const params = new URLSearchParams();


      if (filters?.state_id) {
        params.append('state_id', filters.state_id.toString());
      }
      
      if (filters?.county_id) {
        params.append('county_id', filters.county_id.toString());
      }
      
      if (filters?.status_id) {
        params.append('status_id', filters.status_id.toString());
      }

      const url = `${API_URL}/api/agencies?${params.toString()}`; 

      const res = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!res.ok) {
        throw new Error(`Failed to fetch agencies: ${res.statusText}`);
      }

      const agencies: Agency[] = await res.json();
      
      
      return agencies;
    } catch (error) {
      throw error;
    }
  }
};