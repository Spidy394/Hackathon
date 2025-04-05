import React, { useState } from "react";

const LoadCSVSection = () => {
  const [importType, setImportType] = useState("items");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const endpoint = importType === "items" ? "/api/import/items" : "/api/import/containers";

    const res = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md text-black max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4 text-center">Import Items/Containers (CSV)</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <select
          value={importType}
          onChange={(e) => setImportType(e.target.value)}
          className="input w-full"
        >
          <option value="items">Import Items</option>
          <option value="containers">Import Containers</option>
        </select>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="input w-full"
        />

        <button
          type="submit"
          className="btn bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Upload CSV
        </button>
      </form>

      {result && (
        <div className="mt-4 text-sm">
          <p className="font-semibold text-green-700">
            {importType === "items" ? "Items Imported" : "Containers Imported"}:{" "}
            {importType === "items" ? result.itemsImported : result.containersImported}
          </p>
          {result.errors?.length > 0 && (
            <div className="mt-2 text-red-600">
              <h4 className="font-semibold">Errors:</h4>
              <ul className="list-disc list-inside">
                {result.errors.map((err, idx) => (
                  <li key={idx}>
                    Row {err.row}: {err.message}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LoadCSVSection;
