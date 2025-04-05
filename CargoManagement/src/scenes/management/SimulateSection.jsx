import React, { useState } from "react";
import axios from "axios";
import SimulateResults from "./SimulateResults";

const SimulateSection = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.get("http://localhost:8000/api/simulate", {
        params: {
          startDate,
          endDate,
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error("Simulation failed", err);
      alert("Simulation failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-10 p-6 bg-white text-black rounded shadow">
      <h2 className="text-xl font-bold mb-4">Simulate Time Progression</h2>
      <form onSubmit={handleSimulate} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="p-2 border border-gray-300 rounded"
            placeholder="Start Date"
          />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="p-2 border border-gray-300 rounded"
            placeholder="End Date"
          />
        </div>
        <button
          type="submit"
          className="btn bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
        >
          {loading ? "Simulating..." : "Simulate"}
        </button>
      </form>

      {result && <SimulateResults data={result} />}
    </div>
  );
};

export default SimulateSection;
