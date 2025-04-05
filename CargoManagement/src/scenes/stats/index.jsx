import React, { useEffect, useState } from "react";

export default function StatsPage() {
  const [items, setItems] = useState([]);
  const [containers, setContainers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const itemRes = await fetch("http://localhost:8000/api/items");
      const containerRes = await fetch("http://localhost:8000/api/containers");

      const itemData = await itemRes.json();
      const containerData = await containerRes.json();

      setItems(itemData.items);
      setContainers(containerData.containers);
    };

    fetchData();
  }, []);

  return (
    <div className="p-6 space-y-12">
      <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
        System Statistics
      </h1>

      {/* Item Stats Table */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-gray-600">
        <h2 className="text-2xl font-semibold text-blue-300 mb-4">Item Stats</h2>
        <div className="overflow-x-auto rounded-xl">
          <table className="min-w-full text-sm text-white">
            <thead className="bg-blue-950/60 text-blue-200">
              <tr>
                {[
                  "ID", "Name", "Width", "Depth", "Height",
                  "Mass", "Priority", "Expiry Date", "Usage Limit", "Preferred Zone"
                ].map((h) => <th key={h} className="px-4 py-2 text-left">{h}</th>)}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {items.map((item, idx) => (
                <tr key={item.id} className={idx % 2 === 0 ? "bg-gray-800/50" : "bg-gray-900/50"}>
                  <td className="px-4 py-2">{item.id}</td>
                  <td className="px-4 py-2">{item.name}</td>
                  <td className="px-4 py-2">{item.width}</td>
                  <td className="px-4 py-2">{item.depth}</td>
                  <td className="px-4 py-2">{item.height}</td>
                  <td className="px-4 py-2">{item.mass}</td>
                  <td className="px-4 py-2">{item.priority}</td>
                  <td className="px-4 py-2">{item.expiryDate}</td>
                  <td className="px-4 py-2">{item.usageLimit}</td>
                  <td className="px-4 py-2">{item.preferredZone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Container Stats Table */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-gray-600">
        <h2 className="text-2xl font-semibold text-purple-300 mb-4">Container Stats</h2>
        <div className="overflow-x-auto rounded-xl">
          <table className="min-w-full text-sm text-white">
            <thead className="bg-purple-950/60 text-purple-200">
              <tr>
                {["Zone", "Container ID", "Width", "Depth", "Height"].map((h) => (
                  <th key={h} className="px-4 py-2 text-left">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {containers.map((container, idx) => (
                <tr key={container.containerId} className={idx % 2 === 0 ? "bg-gray-800/50" : "bg-gray-900/50"}>
                  <td className="px-4 py-2">{container.zone}</td>
                  <td className="px-4 py-2">{container.containerId}</td>
                  <td className="px-4 py-2">{container.width}</td>
                  <td className="px-4 py-2">{container.depth}</td>
                  <td className="px-4 py-2">{container.height}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
