import React, { useState } from "react";
import axios from "axios";

const LogSection = () => {
  const [filters, setFilters] = useState({
    startDate: "",
    endDate: "",
    itemId: "",
    userId: "",
    actionType: ""
  });

  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (key, value) => {
    setFilters({ ...filters, [key]: value });
  };

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const params = {};
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params[key] = value;
      });

      const response = await axios.get("http://localhost:8000/api/logs", {
        params
      });

      setLogs(response.data.logs || []);
    } catch (err) {
      console.error("Failed to fetch logs:", err);
      alert("Failed to fetch logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white text-black rounded p-6 shadow max-w-4xl mx-auto mt-10">
      <h2 className="text-xl font-bold mb-4">View Action Logs</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <input
          type="date"
          value={filters.startDate}
          onChange={(e) => handleChange("startDate", e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="date"
          value={filters.endDate}
          onChange={(e) => handleChange("endDate", e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          placeholder="Item ID"
          value={filters.itemId}
          onChange={(e) => handleChange("itemId", e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          placeholder="User ID"
          value={filters.userId}
          onChange={(e) => handleChange("userId", e.target.value)}
          className="p-2 border border-gray-300 rounded"
        />
        <select
          value={filters.actionType}
          onChange={(e) => handleChange("actionType", e.target.value)}
          className="p-2 border border-gray-300 rounded"
        >
          <option value="">All Action Types</option>
          <option value="placement">Placement</option>
          <option value="retrieval">Retrieval</option>
          <option value="rearrangement">Rearrangement</option>
          <option value="disposal">Disposal</option>
        </select>
      </div>
      <button
        onClick={fetchLogs}
        className="btn bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Fetching..." : "Fetch Logs"}
      </button>

      {logs.length > 0 && (
        <div className="mt-8 space-y-4">
          <h3 className="text-lg font-bold">Logs:</h3>
          {logs.map((log, idx) => (
            <div key={idx} className="bg-white/10 text-white p-4 rounded shadow">
              <p>
                <strong>Time:</strong> {new Date(log.timestamp).toLocaleString()}
              </p>
              <p>
                <strong>User:</strong> {log.userId}
              </p>
              <p>
                <strong>Action:</strong> {log.actionType}
              </p>
              <p>
                <strong>Item:</strong> {log.itemId}
              </p>
              {log.details && (
                <div className="mt-2 pl-4 border-l-2 border-blue-300 space-y-1">
                  {log.details.fromContainer && (
                    <p>From: {log.details.fromContainer}</p>
                  )}
                  {log.details.toContainer && (
                    <p>To: {log.details.toContainer}</p>
                  )}
                  {log.details.reason && <p>Reason: {log.details.reason}</p>}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {logs.length === 0 && !loading && (
        <p className="mt-4 text-gray-500">No logs found for the given filters.</p>
      )}
    </div>
  );
};

export default LogSection;
