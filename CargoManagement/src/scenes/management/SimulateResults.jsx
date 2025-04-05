import React from "react";

const SimulateResults = ({ data }) => {
  if (!data) return null;

  return (
    <div className="mt-8 text-white bg-white/10 p-6 rounded space-y-4 max-w-2xl mx-auto">
      <h3 className="text-lg font-bold">Simulation Results</h3>

      <p><strong>Start:</strong> {data.startDate}</p>
      <p><strong>End:</strong> {data.endDate}</p>

      <div className="space-y-2">
        <h4 className="font-semibold">Summary:</h4>
        <p>📦 <strong>{data.totalItems}</strong> items processed</p>
        <p>⏰ <strong>{data.expiredItems?.length}</strong> items expired</p>
        <p>♻️ <strong>{data.rearrangedItems?.length}</strong> items rearranged</p>
        <p>🗑️ <strong>{data.disposedItems?.length}</strong> items disposed</p>
      </div>

      {data.expiredItems?.length > 0 && (
        <div>
          <h4 className="font-semibold mt-4">Expired Items</h4>
          <ul className="list-disc ml-6">
            {data.expiredItems.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}

      {data.rearrangedItems?.length > 0 && (
        <div>
          <h4 className="font-semibold mt-4">Rearranged Items</h4>
          <ul className="list-disc ml-6">
            {data.rearrangedItems.map((item) => (
              <li key={item.itemId}>
                {item.itemId} — from {item.fromContainer} to {item.toContainer}
              </li>
            ))}
          </ul>
        </div>
      )}

      {data.disposedItems?.length > 0 && (
        <div>
          <h4 className="font-semibold mt-4 text-red-400">Disposed Items</h4>
          <ul className="list-disc ml-6">
            {data.disposedItems.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SimulateResults;
