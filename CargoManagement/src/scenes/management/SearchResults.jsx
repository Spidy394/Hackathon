import React from "react";

const SearchResults = ({ data }) => {
  if (!data || !data.success || !data.retrievalPlan) return null;

  return (
    <div className="mt-10 w-full max-w-4xl mx-auto text-white space-y-6">
      <h2 className="text-xl font-bold text-center">Search & Retrieval Results</h2>

      <div>
        <h3 className="text-lg font-semibold">Retrieval Plan</h3>
        {data.retrievalPlan.map((step, i) => (
          <div key={i} className="bg-white/10 p-4 rounded">
            Step {step.step}: <strong>{step.action}</strong> item <strong>{step.itemId}</strong> – {step.itemName}
          </div>
        ))}
      </div>

      <div>
        <h3 className="text-lg font-semibold">Item Location</h3>
        <div className="bg-white/10 p-4 rounded">
          <p><strong>Container:</strong> {data.itemLocation.containerId}</p>
          <p><strong>Start:</strong> ({data.itemLocation.startCoordinates.width},{data.itemLocation.startCoordinates.depth},{data.itemLocation.startCoordinates.height})</p>
          <p><strong>End:</strong> ({data.itemLocation.endCoordinates.width},{data.itemLocation.endCoordinates.depth},{data.itemLocation.endCoordinates.height})</p>
        </div>
      </div>
    </div>
  );
};

export default SearchResults;
