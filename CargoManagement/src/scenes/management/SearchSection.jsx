import React, { useState } from "react";
import axios from "axios";
import SearchResults from "./SearchResults";

const SearchSection = () => {
  const [itemId, setItemId] = useState("");
  const [itemName, setItemName] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSearch = async () => {
    setErrorMsg("");
    setResult(null);

    if (!itemId && !itemName) {
      setErrorMsg("Please enter Item ID or Item Name to search.");
      return;
    }

    try {
      setLoading(true);
      const params = itemId ? { itemId } : { name: itemName };
      const res = await axios.get("http://localhost:8000/api/retrieve/item", { params });
      setResult(res.data);
    } catch (error) {
      console.error("Search failed", error);
      setErrorMsg("Search failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white text-black rounded-lg shadow-md max-w-2xl mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4">Search & Retrieve Item</h2>

      <div className="flex flex-col gap-4">
        <input
          className="p-2 border border-gray-300 rounded"
          placeholder="Item ID (or leave blank)"
          value={itemId}
          onChange={(e) => setItemId(e.target.value)}
        />
        <input
          className="p-2 border border-gray-300 rounded"
          placeholder="Item Name (if ID not provided)"
          value={itemName}
          onChange={(e) => setItemName(e.target.value)}
        />
        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Searching..." : "Search"}
        </button>
        {errorMsg && <p className="text-red-600">{errorMsg}</p>}
      </div>

      <SearchResults data={result} />
    </div>
  );
};

export default SearchSection;
