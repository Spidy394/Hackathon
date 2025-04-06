import React from "react";

const SearchResults = ({ data }) => {
  if (!data || !data.success) return null;
  
  if (!data.found) {
    return (
      <div className="mt-6 p-4 bg-red-100 text-red-800 rounded">
        Item not found. Please check the ID or name and try again.
      </div>
    );
  }

  return (
    <div className="mt-10 w-full max-w-4xl mx-auto space-y-6">
      <h2 className="text-xl font-bold text-center">Search & Retrieval Results</h2>

      {data.item && (
        <div className="bg-white/10 p-4 rounded-lg text-white">
          <h3 className="text-lg font-semibold">Item Location</h3>
          <div className="mt-2">
            <p><strong>Item:</strong> {data.item.name} (ID: {data.item.itemId})</p>
            <p><strong>Container:</strong> {data.item.containerId}</p>
            <p><strong>Zone:</strong> {data.item.zone}</p>
            <p><strong>Position:</strong></p>
            <div className="ml-4">
              <p><strong>Start:</strong> ({data.item.position.startCoordinates.width}, 
                {data.item.position.startCoordinates.depth}, 
                {data.item.position.startCoordinates.height})</p>
              <p><strong>End:</strong> ({data.item.position.endCoordinates.width}, 
                {data.item.position.endCoordinates.depth}, 
                {data.item.position.endCoordinates.height})</p>
            </div>
          </div>
        </div>
      )}

      {data.retrievalSteps && data.retrievalSteps.length > 0 && (
        <div className="bg-white/10 p-4 rounded-lg text-white">
          <h3 className="text-lg font-semibold">Retrieval Plan</h3>
          <div className="mt-2 space-y-2">
            {data.retrievalSteps.map((step, i) => (
              <div key={i} className="p-2 border border-gray-700 rounded">
                <p><strong>Step {step.step}:</strong> {step.action.toUpperCase()} - {step.itemName} (ID: {step.itemId})</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchResults;
