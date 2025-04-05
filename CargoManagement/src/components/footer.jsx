function Footer() {
    return (
      <footer className="bg-gradient-to-r from-gray-800 via-gray-900 to-black text-white py-8 mt-auto">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-center md:text-left">
            &copy; {new Date().getFullYear()} Cargo Management. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a
              href="#"
              className="hover:text-blue-500 transition duration-300 text-sm"
            >
              About
            </a>
            <a
              href="#"
              className="hover:text-blue-500 transition duration-300 text-sm"
            >
              Contact
            </a>
            <a
              href="#"
              className="hover:text-blue-500 transition duration-300 text-sm"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    );
  }
  
  export default Footer;
