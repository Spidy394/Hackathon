import React from "react";

const PlacementResults = ({ data }) => {
  if (!data) return null;
  return (
    <div className="mt-10 w-full max-w-4xl mx-auto text-white space-y-6">
      <h2 className="text-xl font-bold text-center">Placement Results</h2>

      <div>
        <h3 className="text-lg font-semibold">Placements</h3>
        {data.placements?.map((p, i) => (
          <div key={i} className="bg-white/10 p-4 rounded">
            Item <strong>{p.itemId}</strong> placed in <strong>{p.containerId}</strong> from 
            ({p.position.startCoordinates.width},{p.position.startCoordinates.depth},{p.position.startCoordinates.height}) 
            to 
            ({p.position.endCoordinates.width},{p.position.endCoordinates.depth},{p.position.endCoordinates.height})
          </div>
        ))}
      </div>

      <div>
        <h3 className="text-lg font-semibold">Rearrangements</h3>
        {data.rearrangements?.map((r, i) => (
          <div key={i} className="bg-white/10 p-4 rounded">
            Step {r.step}: {r.action} item <strong>{r.itemId}</strong> from {r.fromContainer} to {r.toContainer}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PlacementResults;
