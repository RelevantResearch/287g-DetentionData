import React from 'react';
import { State } from '../types';
import LoadingSpinner from './LoadingSpinner';

interface StateDropdownProps {
  states: State[];
  selectedStateId: number | null;
  onStateChange: (stateId: number | null) => void;
  loading?: boolean;
}

const StateDropdown: React.FC<StateDropdownProps> = ({
  states,
  selectedStateId,
  onStateChange,
  loading = false
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onStateChange(value ? parseInt(value, 10) : null);
  };

  return (
    <div className="flex flex-col group">
      <label htmlFor="state-select" className="text-sm font-semibold text-gray-700 mb-3 transition-colors duration-200 group-focus-within:text-blue-600">
        State
      </label>
      <div className="relative">
        <select
          id="state-select"
          value={selectedStateId || ''}
          onChange={handleChange}
          disabled={loading}
          className="w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white disabled:bg-gray-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-md hover:border-gray-300"
        >
          <option value="">All States</option>
          {states.map((state) => (
            <option key={state.state_id} value={state.state_id}>
              {state.state_name}
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

export default StateDropdown;