import React from "react";

const ActionCard = ({ icon, label }) => {
  return (
    <div className="bg-gray-800 hover:bg-gray-700 transition-colors p-6 rounded-2xl w-40 h-40 flex flex-col items-center justify-center text-center shadow-lg">
      <div className="mb-3">{icon}</div>
      <div className="font-semibold">{label}</div>
    </div>
  );
};

export default ActionCard;
