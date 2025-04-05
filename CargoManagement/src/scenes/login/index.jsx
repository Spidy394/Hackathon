function Login() {
    return (
      <div className="min-h-screen flex items-center justify-center bg-space bg-cover bg-center text-white">
        <div className="bg-gray-800 bg-opacity-70 p-8 rounded-2xl w-80 shadow-lg">
          <h1 className="text-3xl font-bold text-center mb-6">LOGIN</h1>
          <form className="flex flex-col gap-4">
            <div>
              <label className="text-sm font-semibold block mb-1" htmlFor="userid">USER ID</label>
              <input
                id="userid"
                type="text"
                className="w-full p-2 rounded-md bg-gray-700 text-white focus:outline-none"
                placeholder="Enter user ID"
              />
            </div>
            <div>
              <label className="text-sm font-semibold block mb-1" htmlFor="password">PASSWORD</label>
              <input
                id="password"
                type="password"
                className="w-full p-2 rounded-md bg-gray-700 text-white focus:outline-none"
                placeholder="Enter password"
              />
            </div>
            <button
              type="submit"
              className="bg-blue-800 hover:bg-blue-700 rounded-2xl py-2 font-semibold transition"
            >
              ENTER
            </button>
          </form>
        </div>
      </div>
    );
  }
  
  export default Login;
  