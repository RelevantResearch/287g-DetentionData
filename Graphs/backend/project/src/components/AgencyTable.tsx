import React, { useState, useMemo } from 'react';
import { Database } from 'lucide-react';
import { Agency } from '../types';
import { ExternalLink } from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import Pagination from './Pagination';

interface AgencyTableProps {
  agencies: Agency[];
  loading?: boolean;
  error?: string | null;
  itemsPerPage?: number;
}

const AgencyTable: React.FC<AgencyTableProps> = ({
  agencies,
  loading = false,
  error,
  itemsPerPage = 20
}) => {
  const [currentPage, setCurrentPage] = useState(1);

  // Calculate pagination data
  const totalItems = agencies.length;
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  
  // Get current page items
  const paginatedAgencies = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return agencies.slice(startIndex, endIndex);
  }, [agencies, currentPage, itemsPerPage]);

  // Reset to first page when agencies change
  React.useEffect(() => {
    setCurrentPage(1);
  }, [agencies]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  if (loading) {
    return (
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 p-12">
        <div className="flex items-center justify-center animate-pulse">
          <LoadingSpinner size="lg" />
          <span className="ml-4 text-lg text-gray-600 font-medium">Loading agencies...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-red-200/50 p-12">
        <div className="text-center text-red-600 animate-fade-in">
          <div className="w-16 h-16 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center">
            <span className="text-2xl">⚠️</span>
          </div>
          <p className="font-semibold text-lg">Error loading agencies</p>
          <p className="text-xm mt-2 text-red-500">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/20 overflow-hidden transform hover:shadow-2xl transition-all duration-500">
      <div className="px-8 py-6 border-b border-gray-200/60 bg-gradient-to-r from-gray-50/50 to-white/50">
        <h3 className="text-xl font-bold text-gray-900 flex items-center">
          <div className="w-1 h-6 bg-gradient-to-b from-blue-500 to-indigo-600 rounded-full mr-3"></div>
          Agencies ({totalItems})
        </h3>
      </div>

      {agencies.length === 0 ? (
        <div className="p-16 text-center text-gray-500 animate-fade-in">
          <div className="w-20 h-20 mx-auto mb-6 bg-gray-100 rounded-full flex items-center justify-center">
            <Database className="h-10 w-10 text-gray-400" />
          </div>
          <p className="text-lg font-medium">No agencies found</p>
          <p className="text-xm mt-2">Try adjusting your filter criteria</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto animate-fade-in">
            <table className="min-w-full divide-y divide-gray-200/60">
              <thead className="bg-gradient-to-r from-blue-50/80 to-blue-100/80 backdrop-blur-sm">
                <tr>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Agency Name
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Type
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Support Type
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Signed
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Last Seen
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    County
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    State
                  </th>
                  <th className="px-6 py-4 text-left text-xm font-bold text-gray-600 uppercase tracking-wider">
                    Link
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white/50 backdrop-blur-sm divide-y divide-gray-200/40">
                {paginatedAgencies.map((agency, index) => (
                  <tr key={`${agency.id}-${currentPage}-${index}`} className="transition-all duration-300 hover:shadow-lg hover:bg-gradient-to-r hover:from-gray-50/70 hover:to-gray-200/70 hover:backdrop-blur-sm">
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm font-semibold text-gray-900">
                        {agency.agency_name}
                      </div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">{agency.type}</div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">{agency.support_type}</div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">
                        {new Date(agency.signed).toLocaleDateString()}
                      </div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">{new Date(agency.last_seen).toLocaleDateString()}</div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <span
                        className={`inline-flex px-3 py-1.5 text-xs font-bold rounded-full shadow-sm border transition-all duration-200 ${agency.status?.status_name?.toLowerCase().includes("active")
                            ? "bg-gradient-to-r from-emerald-100 to-emerald-200 text-emerald-800 border-emerald-200"
                            : agency.status?.status_name?.toLowerCase().includes("inactive")
                              ? "bg-gradient-to-r from-red-100 to-red-200 text-red-800 border-red-200"
                              : agency.status?.status_name?.toLowerCase().includes("pending")
                                ? "bg-gradient-to-r from-yellow-100 to-yellow-200 text-yellow-800 border-yellow-200"
                                : agency.status?.status_name?.toLowerCase().includes("suspended")
                                  ? "bg-gradient-to-r from-orange-100 to-orange-200 text-orange-800 border-orange-200"
                                  : "bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 border-gray-200"
                          }`}
                      >
                        {agency.status?.status_name || "Unknown"}
                      </span>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">{agency.county?.county_name}</div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="text-xm text-gray-900">{agency.state?.state_name}</div>
                    </td>
                    <td className="px-6 py-5 whitespace-nowrap">
                      {agency.extracted_link ? (
                        <a
                          href={agency.extracted_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center justify-center w-8 h-8 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-full transition-all duration-200 transform hover:scale-110"
                        >
                          <ExternalLink className="h-4 w-4" />
                        </a>
                      ) : (
                        <span className="text-gray-400 text-lg">—</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              totalItems={totalItems}
              itemsPerPage={itemsPerPage}
              onPageChange={handlePageChange}
            />
          )}
        </>
      )}
    </div>
  );
};

export default AgencyTable;