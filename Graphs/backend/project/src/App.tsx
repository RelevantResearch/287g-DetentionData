// import { useState, useEffect } from 'react';
// import { State, County, Status, Agency } from './types';
// import { apiService } from './services/api';
// import { useApi } from './hooks/useApi';
// import StateDropdown from './components/StateDropdown';
// import CountyDropdown from './components/CountyDropdown';
// import StatusDropdown from './components/StatusDropdown';
// import AgencyTable from './components/AgencyTable';
// import { Database } from 'lucide-react';

// function App() {
//   const [selectedStateId, setSelectedStateId] = useState<number | null>(null);
//   const [selectedCountyId, setSelectedCountyId] = useState<number | null>(null);
//   const [selectedStatusId, setSelectedStatusId] = useState<number | null>(null);

//   // API calls using custom hook
//   const { 
//     data: states, 
//     loading: statesLoading 
//   } = useApi<State[]>(() => apiService.getStates(), []);

//   const { 
//     data: counties, 
//     loading: countiesLoading 
//   } = useApi<County[]>(() => apiService.getCounties(), []);

//   const { 
//     data: statuses, 
//     loading: statusesLoading 
//   } = useApi<Status[]>(() => apiService.getStatus(), []);

//   // FIXED: Pass status_id instead of status_name
//   const { 
//     data: agencies, 
//     loading: agenciesLoading,
//     error: agenciesError 
//   } = useApi<Agency[]>(
//     () => {
//       const filters = {
//         ...(selectedStateId && { state_id: selectedStateId }),
//         ...(selectedCountyId && { county_id: selectedCountyId }),
//         ...(selectedStatusId && { status_id: selectedStatusId }) // FIXED: Use status_id
//       };
      
//       return apiService.getAgencies(filters);
//     },
//     [selectedStateId, selectedCountyId, selectedStatusId]
//   );

//   // Reset county selection when state changes
//   useEffect(() => {
//     if (selectedStateId !== null) {
//       setSelectedCountyId(null);
//     }
//   }, [selectedStateId]);

//   const handleStateChange = (stateId: number | null) => {
//     setSelectedStateId(stateId);
//   };

//   const handleCountyChange = (countyId: number | null) => {
//     setSelectedCountyId(countyId);
//   };

//   const handleStatusChange = (statusId: number | null) => {
//     setSelectedStatusId(statusId);
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
//       <div className="max-w-7lg mx-auto px-4 sm:px-6 lg:px-8 py-12">
//         {/* Header */}
//         <div className="mb-12 animate-fade-in">
//           <div className="flex items-center space-x-4 mb-6">
//             <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl shadow-lg transform hover:scale-105 transition-all duration-300">
//               <Database className="h-8 w-8 text-white" />
//             </div>
//             <div>
//               <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
//                 287g Database
//               </h1>
//               <p className="text-lg text-gray-600 mt-1">Immigration enforcement agency tracker</p>
//             </div>
//           </div>
//         </div>

//         {/* Filters */}
//         <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 mb-10 transform hover:shadow-2xl transition-all duration-500">
//           <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
//             <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
//             Filters
//           </h2>
//           <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
//             <StateDropdown
//               states={states || []}
//               selectedStateId={selectedStateId}
//               onStateChange={handleStateChange}
//               loading={statesLoading}
//             />
//             <CountyDropdown
//               counties={counties || []}
//               selectedCountyId={selectedCountyId}
//               onCountyChange={handleCountyChange}
//               loading={countiesLoading}
//               disabled={!selectedStateId}
//             />
//             <StatusDropdown
//               statuses={statuses || []}
//               selectedStatusId={selectedStatusId}
//               onStatusChange={handleStatusChange}
//               loading={statusesLoading}
//             />
//           </div>

//           {/* Active Filters Summary */}
//           {(selectedStateId || selectedCountyId || selectedStatusId) && (
//             <div className="mt-8 pt-6 border-t border-gray-200/60 animate-slide-in">
//               <div className="flex flex-wrap gap-3 items-center">
//                 <span className="text-sm font-medium text-gray-700">Active filters:</span>
//                 {selectedStateId && states && (
//                   <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-blue-100 to-blue-200 text-blue-800 rounded-full border border-blue-200/50 shadow-sm animate-scale-in">
//                     State: {states.find(s => s.state_id === selectedStateId)?.state_name}
//                   </span>
//                 )}
//                 {selectedCountyId && counties && (
//                   <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-emerald-100 to-emerald-200 text-emerald-800 rounded-full border border-emerald-200/50 shadow-sm animate-scale-in">
//                     County: {counties.find(c => c.county_id === selectedCountyId)?.county_name}
//                   </span>
//                 )}
//                 {selectedStatusId && statuses && (
//                   <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-purple-100 to-purple-200 text-purple-800 rounded-full border border-purple-200/50 shadow-sm animate-scale-in">
//                     Status: {statuses.find(s => s.status_id === selectedStatusId)?.status_name}
//                   </span>
//                 )}
//                 <button
//                   onClick={() => {
//                     setSelectedStateId(null);
//                     setSelectedCountyId(null);
//                     setSelectedStatusId(null);
//                   }}
//                   className="inline-flex px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-all duration-200 border border-transparent hover:border-gray-200"
//                 >
//                   Clear all
//                 </button>
//               </div>
//             </div>
//           )}

//         </div>

//         {/* Agency Table */}
//         <div className="animate-fade-in-up">
//           <AgencyTable
//             agencies={agencies || []}
//             loading={agenciesLoading}
//             error={agenciesError}
//           />
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;

import { useState, useEffect } from 'react';
import * as React from 'react';
import { State, County, Status, Agency } from './types';
import { apiService } from './services/api';
import { useApi } from './hooks/useApi';
import StateDropdown from './components/StateDropdown';
import CountyDropdown from './components/CountyDropdown';
import StatusDropdown from './components/StatusDropdown';
import SearchInput from './components/SearchInput';
import AgencyTable from './components/AgencyTable';
import { Database } from 'lucide-react';

function App() {
  const [selectedStateId, setSelectedStateId] = useState<number | null>(null);
  const [selectedCountyId, setSelectedCountyId] = useState<number | null>(null);
  const [selectedStatusId, setSelectedStatusId] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');

  // API calls using custom hook
  const { 
    data: states, 
    loading: statesLoading 
  } = useApi<State[]>(() => apiService.getStates(), []);

  const { 
    data: counties, 
    loading: countiesLoading 
  } = useApi<County[]>(() => apiService.getCounties(), []);

  const { 
    data: statuses, 
    loading: statusesLoading 
  } = useApi<Status[]>(() => apiService.getStatus(), []);

  // Get agencies with dropdown filters only (not search)
  const { 
    data: allAgencies, 
    loading: agenciesLoading,
    error: agenciesError 
  } = useApi<Agency[]>(
    () => {
      const filters = {
        ...(selectedStateId && { state_id: selectedStateId }),
        ...(selectedCountyId && { county_id: selectedCountyId }),
        ...(selectedStatusId && { status_id: selectedStatusId })
      };
      
      return apiService.getAgencies(filters);
    },
    [selectedStateId, selectedCountyId, selectedStatusId]
  );

  // Apply client-side search filtering
  const agencies = React.useMemo(() => {
    if (!allAgencies || !searchQuery.trim()) {
      return allAgencies || [];
    }

    const query = searchQuery.toLowerCase().trim();
    return allAgencies.filter((agency) => {
      // Search in multiple fields based on the actual data structure
      const searchFields = [
        agency.agency_name,
        agency.type,
        agency.support_type,
        agency.county?.county_name,
        agency.state?.state_name,
        agency.status?.status_name
      ].filter(Boolean); // Remove any undefined/null values

      return searchFields.some(field => 
        field?.toString().toLowerCase().includes(query)
      );
    });
  }, [allAgencies, searchQuery]);

  // Reset county selection when state changes
  useEffect(() => {
    if (selectedStateId !== null) {
      setSelectedCountyId(null);
    }
  }, [selectedStateId]);

  const handleStateChange = (stateId: number | null) => {
    setSelectedStateId(stateId);
  };

  const handleCountyChange = (countyId: number | null) => {
    setSelectedCountyId(countyId);
  };

  const handleStatusChange = (statusId: number | null) => {
    setSelectedStatusId(statusId);
  };

  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
  };

  const clearAllFilters = () => {
    setSelectedStateId(null);
    setSelectedCountyId(null);
    setSelectedStatusId(null);
    setSearchQuery('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="max-w-7lg mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-12 animate-fade-in">
          <div className="flex items-center space-x-4 mb-6">
            <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl shadow-lg transform hover:scale-105 transition-all duration-300">
              <Database className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                287g Database
              </h1>
              <p className="text-lg text-gray-600 mt-1">Immigration enforcement agency tracker</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-8 mb-10 transform hover:shadow-2xl transition-all duration-500">
          <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
            <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
            Filters
          </h2>
          
          {/* Search Input - Full Width */}
          <div className="mb-8">
            <SearchInput
              value={searchQuery}
              onChange={handleSearchChange}
              placeholder="Search agencies by name, location, or details..."
            />
          </div>

          {/* Dropdown Filters */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StateDropdown
              states={states || []}
              selectedStateId={selectedStateId}
              onStateChange={handleStateChange}
              loading={statesLoading}
            />
            <CountyDropdown
              counties={counties || []}
              selectedCountyId={selectedCountyId}
              onCountyChange={handleCountyChange}
              loading={countiesLoading}
              disabled={!selectedStateId}
            />
            <StatusDropdown
              statuses={statuses || []}
              selectedStatusId={selectedStatusId}
              onStatusChange={handleStatusChange}
              loading={statusesLoading}
            />
          </div>

          {/* Active Filters Summary */}
          {(selectedStateId || selectedCountyId || selectedStatusId || searchQuery.trim()) && (
            <div className="mt-8 pt-6 border-t border-gray-200/60 animate-slide-in">
              <div className="flex flex-wrap gap-3 items-center">
                <span className="text-sm font-medium text-gray-700">Active filters:</span>
                {searchQuery.trim() && (
                  <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-orange-100 to-orange-200 text-orange-800 rounded-full border border-orange-200/50 shadow-sm animate-scale-in">
                    Search: "{searchQuery.trim()}"
                  </span>
                )}
                {selectedStateId && states && (
                  <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-blue-100 to-blue-200 text-blue-800 rounded-full border border-blue-200/50 shadow-sm animate-scale-in">
                    State: {states.find(s => s.state_id === selectedStateId)?.state_name}
                  </span>
                )}
                {selectedCountyId && counties && (
                  <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-emerald-100 to-emerald-200 text-emerald-800 rounded-full border border-emerald-200/50 shadow-sm animate-scale-in">
                    County: {counties.find(c => c.county_id === selectedCountyId)?.county_name}
                  </span>
                )}
                {selectedStatusId && statuses && (
                  <span className="inline-flex px-3 py-1.5 text-xs font-semibold bg-gradient-to-r from-purple-100 to-purple-200 text-purple-800 rounded-full border border-purple-200/50 shadow-sm animate-scale-in">
                    Status: {statuses.find(s => s.status_id === selectedStatusId)?.status_name}
                  </span>
                )}
                <button
                  onClick={clearAllFilters}
                  className="inline-flex px-3 py-1.5 text-xs font-medium text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-all duration-200 border border-transparent hover:border-gray-200"
                >
                  Clear all
                </button>
              </div>
            </div>
          )}

        </div>

        {/* Agency Table */}
        <div className="animate-fade-in-up">
          <AgencyTable
            agencies={agencies || []}
            loading={agenciesLoading}
            error={agenciesError}
          />
        </div>
      </div>
    </div>
  );
}

export default App;