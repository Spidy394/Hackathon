import React, { useState } from "react";
import axios from "axios";
import DisposeResults from "./DisposeResults";

const DisposeSection = () => {
  const [itemIds, setItemIds] = useState([""]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleItemChange = (index, value) => {
    const updated = [...itemIds];
    updated[index] = value;
    setItemIds(updated);
  };

  const addItemField = () => {
    setItemIds([...itemIds, ""]);
  };

  const handleDispose = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post("http://localhost:8000/api/dispose", {
        itemIds,
      });
      setResult(response.data);
    } catch (err) {
      console.error("Dispose failed", err);
      alert("Disposal failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-10 p-6 bg-white text-black rounded shadow">
      <h2 className="text-xl font-bold mb-4">Dispose Items</h2>
      <form onSubmit={handleDispose} className="space-y-4">
        {itemIds.map((id, index) => (
          <input
            key={index}
            value={id}
            onChange={(e) => handleItemChange(index, e.target.value)}
            className="p-2 w-full border border-gray-300 rounded"
            placeholder={`Item ID #${index + 1}`}
          />
        ))}
        <button
          type="button"
          className="btn bg-gray-300 px-3 py-1 rounded hover:bg-gray-400"
          onClick={addItemField}
        >
          + Add Another
        </button>
        <br />
        <button
          type="submit"
          className="btn bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          {loading ? "Disposing..." : "Dispose"}
        </button>
      </form>

      {result && <DisposeResults data={result} />}
    </div>
  );
};

export default DisposeSection;
