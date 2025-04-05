import React from "react";

const ExportCSVSection = () => {
  const handleDownload = () => {
    fetch("/api/export/arrangement")
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "arrangement.csv");
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md text-black max-w-3xl mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4 text-center">Export Current Arrangement</h2>
      <button
        onClick={handleDownload}
        className="btn bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
      >
        Download Arrangement CSV
      </button>
    </div>
  );
};

export default ExportCSVSection;
