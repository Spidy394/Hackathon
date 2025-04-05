function Footer() {
    return (
      <footer className="bg-gray-900 text-white py-6 mt-auto">
        <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-center md:text-left">
            &copy; {new Date().getFullYear()} Cargo Management. All rights reserved.
          </p>
          <div className="flex space-x-4 mt-2 md:mt-0">
            <a
              href="#"
              className="hover:text-blue-400 transition duration-200 text-sm"
            >
              About
            </a>
            <a
              href="#"
              className="hover:text-blue-400 transition duration-200 text-sm"
            >
              Contact
            </a>
            <a
              href="#"
              className="hover:text-blue-400 transition duration-200 text-sm"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    );
  }
  
  export default Footer;
  