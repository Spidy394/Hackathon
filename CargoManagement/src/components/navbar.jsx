import { UserCircle } from "lucide-react";
import { NavLink, Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Navbar = () => {
  const navLinkBaseClasses =
    "hover:text-blue-300 transition-colors duration-200 ease-in-out";
  const navLinkActiveClasses = "text-blue-400 font-bold";

  return (
    <nav className="bg-gradient-to-r from-gray-900 to-blue-900 text-white px-8 py-4 flex justify-between items-center border-b border-gray-700/50">
      <Link to="/" className="flex items-center gap-2 group">
        <img src={logo} alt="Logo" className="w-10 h-10" />
        <div className="text-xl font-bold leading-tight">
          <div className="font-sans">STELLAR</div>
          <div className="-mt-2 font-sans">STASH</div>
        </div>
      </Link>

      <div className="flex gap-8 items-center text-lg font-semibold tracking-wider">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `${navLinkBaseClasses} ${isActive ? navLinkActiveClasses : ""}`
          }
        >
          HOME
        </NavLink>
        <NavLink
          to="/management"
          className={({ isActive }) =>
            `${navLinkBaseClasses} ${isActive ? navLinkActiveClasses : ""}`
          }
        >
          CARGO
        </NavLink>
        <NavLink
          to="/stats"
          className={({ isActive }) =>
            `${navLinkBaseClasses} ${isActive ? navLinkActiveClasses : ""}`
          }
        >
          STATS
        </NavLink>
        <button
          type="button"
          className="hover:text-blue-300 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 rounded-full"
          aria-label="User menu"
        >
          <UserCircle className="w-8 h-8" />
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
