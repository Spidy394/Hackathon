import { UserCircle } from "lucide-react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-gray-900 to-blue-900 text-white px-6 py-4 flex justify-between items-center">
      {/* Left: Logo and Title */}
      <div className="flex items-center gap-2">
        <img src={logo} alt="Logo" className="w-10 h-10" />
        <div className="text-xl font-bold leading-tight">
          <div className="font-sans">STELLAR</div>
          <div className="-mt-2 font-sans">STASH</div>
        </div>
      </div>

      {/* Right: Navigation */}
      <div className="flex gap-6 items-center text-lg font-semibold tracking-widest">
        <Link to="/" className="hover:text-blue-300">HOME</Link>
        <Link to="/management" className="hover:text-blue-300">CARGO</Link>
        <Link to="/stats" className="hover:text-blue-300">STATS</Link>
        <UserCircle className="w-8 h-8 text-white" />
      </div>
    </nav>
  );
};

export default Navbar;
