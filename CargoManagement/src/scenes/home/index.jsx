import { useNavigate } from "react-router-dom";
import HText from "../../shared/HText"

function Home() {
  const navigate = useNavigate();

  return (
    <main className="flex flex-col items-center justify-center h-[80vh] text-center px-4">
      <HText>Welcome Astronomer</HText>
      <div className="flex flex-col gap-4 w-40">
        <button
          onClick={() => navigate("/register")}
          className="bg-blue-800 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-2xl transition"
        >
          Register
        </button>
        <button
          onClick={() => navigate("/login")}
          className="bg-blue-800 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-2xl transition"
        >
          Login
        </button>
      </div>
    </main>
  );
}

export default Home;
