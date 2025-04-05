import React from "react";

const DisposeResults = ({ data }) => {
  if (!data) return null;

  return (
    <div className="mt-8 text-white bg-white/10 p-4 rounded max-w-2xl mx-auto space-y-4">
      <h3 className="text-lg font-bold">Disposal Results</h3>
      {data.successful?.length > 0 && (
        <div>
          <h4 className="font-semibold">Disposed Items:</h4>
          <ul className="list-disc ml-6">
            {data.successful.map((id) => (
              <li key={id}>{id}</li>
            ))}
          </ul>
        </div>
      )}

      {data.failed?.length > 0 && (
        <div>
          <h4 className="font-semibold text-red-400">Failed to Dispose:</h4>
          <ul className="list-disc ml-6">
            {data.failed.map((item) => (
              <li key={item.itemId}>
                {item.itemId} – {item.reason || "Unknown error"}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DisposeResults;
