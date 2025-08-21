import React from 'react';
// import { County } from '../types';
import LoadingSpinner from './LoadingSpinner';

export interface County {
  county_id: number;
  county_name: string;
  state_id: number;
}


interface CountyDropdownProps {
  counties: County[];
  selectedCountyId: number | null;
  onCountyChange: (countyId: number | null) => void;
  loading?: boolean;
  disabled?: boolean;
}

const CountyDropdown: React.FC<CountyDropdownProps> = ({
  counties,
  selectedCountyId,
  onCountyChange,
  loading = false,
  disabled = false
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onCountyChange(value ? parseInt(value, 10) : null);
  };

  return (
    <div className="flex flex-col group">
      <label htmlFor="county-select" className="text-sm font-semibold text-gray-700 mb-3 transition-colors duration-200 group-focus-within:text-blue-600">
        County
      </label>
      <div className="relative">
        <select
          id="county-select"
          value={selectedCountyId || ''}
          onChange={handleChange}
          disabled={loading || disabled}
          className="w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white disabled:bg-gray-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-md hover:border-gray-300"
        >
          <option value="">All Counties</option>
          {counties.map((county) => (
            <option key={county.county_id} value={county.county_id}>
              {county.county_name}
            </option>
          ))}


        </select>
        {loading && (
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
            <LoadingSpinner size="sm" />
          </div>
        )}
      </div>
    </div>
  );
};

export default CountyDropdown;