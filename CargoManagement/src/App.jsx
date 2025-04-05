import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "../src/components/navbar";
import Footer from "../src/components/footer";
import Home from "../src/scenes/home";
import Register from "../src/scenes/register";
import Login from "../src/scenes/login";
import Management from "../src/scenes/management";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-space bg-cover bg-center text-white flex flex-col">
        <Navbar />
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/management" element={<Management />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
