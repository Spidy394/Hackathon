import React, { useState } from "react";
import axios from "axios";
import PlacementResults from "./PlacementResults";

const PlacementSection = () => {
  const [items, setItems] = useState([]);
  const [containers, setContainers] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const addItem = () =>
    setItems([
      ...items,
      {
        itemId: "",
        name: "",
        width: 1,
        depth: 1,
        height: 1,
        priority: 1,
        expiryDate: "",
        usageLimit: 1,
        preferredZone: "",
      },
    ]);

  const addContainer = () =>
    setContainers([
      ...containers,
      {
        containerId: "",
        zone: "",
        width: 10,
        depth: 10,
        height: 10,
      },
    ]);

  const handleChange = (list, setList, index, key, value) => {
    const updated = [...list];
    updated[index][key] = value;
    setList(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post("http://localhost:8000/api/place", {
        items,
        containers,
      });
      setResult(response.data);
    } catch (err) {
      console.error("Placement failed", err);
      alert("Placement failed. Please check your data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full">
      <form
        onSubmit={handleSubmit}
        className="space-y-6 text-black bg-white p-6 rounded-xl shadow-md w-full max-w-4xl mx-auto"
      >
        <h2 className="text-xl font-bold text-center text-black">
          Placement Recommendation
        </h2>

        <div>
          <h3 className="font-semibold mb-2">Items</h3>
          {items.map((item, i) => (
            <div key={i} className="grid grid-cols-2 gap-2 mb-4">
              <input
                placeholder="Item ID"
                value={item.itemId}
                onChange={(e) =>
                  handleChange(items, setItems, i, "itemId", e.target.value)
                }
              />
              <input
                placeholder="Name"
                value={item.name}
                onChange={(e) =>
                  handleChange(items, setItems, i, "name", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Width"
                value={item.width}
                onChange={(e) =>
                  handleChange(items, setItems, i, "width", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Depth"
                value={item.depth}
                onChange={(e) =>
                  handleChange(items, setItems, i, "depth", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Height"
                value={item.height}
                onChange={(e) =>
                  handleChange(items, setItems, i, "height", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Priority"
                value={item.priority}
                onChange={(e) =>
                  handleChange(items, setItems, i, "priority", e.target.value)
                }
              />
              <input
                type="date"
                placeholder="Expiry Date"
                onChange={(e) =>
                  handleChange(items, setItems, i, "expiryDate", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Usage Limit"
                value={item.usageLimit}
                onChange={(e) =>
                  handleChange(items, setItems, i, "usageLimit", e.target.value)
                }
              />
              <input
                placeholder="Preferred Zone"
                value={item.preferredZone}
                onChange={(e) =>
                  handleChange(items, setItems, i, "preferredZone", e.target.value)
                }
              />
            </div>
          ))}
          <button type="button" className="btn" onClick={addItem}>
            + Add Item
          </button>
        </div>

        <div>
          <h3 className="font-semibold mb-2">Containers</h3>
          {containers.map((c, i) => (
            <div key={i} className="grid grid-cols-2 gap-2 mb-4">
              <input
                placeholder="Container ID"
                value={c.containerId}
                onChange={(e) =>
                  handleChange(containers, setContainers, i, "containerId", e.target.value)
                }
              />
              <input
                placeholder="Zone"
                value={c.zone}
                onChange={(e) =>
                  handleChange(containers, setContainers, i, "zone", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Width"
                value={c.width}
                onChange={(e) =>
                  handleChange(containers, setContainers, i, "width", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Depth"
                value={c.depth}
                onChange={(e) =>
                  handleChange(containers, setContainers, i, "depth", e.target.value)
                }
              />
              <input
                type="number"
                placeholder="Height"
                value={c.height}
                onChange={(e) =>
                  handleChange(containers, setContainers, i, "height", e.target.value)
                }
              />
            </div>
          ))}
          <button type="button" className="btn" onClick={addContainer}>
            + Add Container
          </button>
        </div>

        <button
          type="submit"
          className="btn bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Placing..." : "Submit"}
        </button>
      </form>

      {result && <PlacementResults data={result} />}
    </div>
  );
};

export default PlacementSection;
