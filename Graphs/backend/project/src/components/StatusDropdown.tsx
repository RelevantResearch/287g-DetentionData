// import React from 'react';
// import { Status } from '../types';
// import LoadingSpinner from './LoadingSpinner';

// interface StatusDropdownProps {
//   statuses: Status[];
//   selectedStatusId: number | null;
//   onStatusChange: (statusId: number | null) => void;
//   loading?: boolean;
// }

// const StatusDropdown: React.FC<StatusDropdownProps> = ({
//   statuses,
//   selectedStatusId,
//   onStatusChange,
//   loading = false
// }) => {
//   const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
//     const value = e.target.value;
//     onStatusChange(value ? parseInt(value, 10) : null);
//   };

//   return (
//     <div className="flex flex-col group">
//       <label htmlFor="status-select" className="text-sm font-semibold text-gray-700 mb-3 transition-colors duration-200 group-focus-within:text-blue-600">
//         Status
//       </label>
//       <div className="relative">
//         <select
//           id="status-select"
//           value={selectedStatusId || ''}
//           onChange={handleChange}
//           disabled={loading}
//           className="w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white disabled:bg-gray-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-md hover:border-gray-300"
//         >
//           <option value="">All Statuses</option>
//           {statuses.map((status) => (
//             <option key={status.status_id} value={status.status_id}>
//               {status.status_name}
//             </option>
//           ))}
//         </select>
//         {loading && (
//           <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
//             <LoadingSpinner size="sm" />
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default StatusDropdown;
import React from 'react';
import { Status } from '../types';
import LoadingSpinner from './LoadingSpinner';

interface StatusDropdownProps {
  statuses: Status[];
  selectedStatusId: number | null;
  onStatusChange: (statusId: number | null) => void;
  loading?: boolean;
}

const StatusDropdown: React.FC<StatusDropdownProps> = ({
  statuses,
  selectedStatusId,
  onStatusChange,
  loading = false
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    const statusId = value ? parseInt(value, 10) : null;
    
  
    
    onStatusChange(statusId);
  };

  // Debug logging for component state
  React.useEffect(() => {
  }, [statuses, selectedStatusId]);

  return (
    <div className="flex flex-col group">
      <label htmlFor="status-select" className="text-sm font-semibold text-gray-700 mb-3 transition-colors duration-200 group-focus-within:text-blue-600">
        Status
      </label>
      <div className="relative">
        <select
          id="status-select"
          value={selectedStatusId || ''}
          onChange={handleChange}
          disabled={loading}
          className="w-full px-4 py-3 border border-gray-200 rounded-xl shadow-sm bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:bg-white disabled:bg-gray-50 disabled:cursor-not-allowed transition-all duration-300 hover:shadow-md hover:border-gray-300"
        >
          <option value="">All Status</option>
          {statuses.map((status) => (
            <option key={status.status_id} value={status.status_id}>
              {status.status_name}
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

export default StatusDropdown;