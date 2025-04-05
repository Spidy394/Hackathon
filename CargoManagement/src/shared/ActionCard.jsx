// shared/ActionCard.jsx or .tsx
const ActionCard = ({ icon, label, onClick }) => (
  <div
    onClick={onClick}
    className="cursor-pointer w-36 h-36 bg-white/10 hover:bg-white/20 rounded-xl flex flex-col items-center justify-center text-center transition"
  >
    <div className="mb-2">{icon}</div>
    <div className="text-sm font-semibold">{label}</div>
  </div>
);

export default ActionCard;