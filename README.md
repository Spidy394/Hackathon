# 🚀 Stellar Stash - Cargo Management System

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/cargoTest3)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.105.0-009688.svg)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-47A248.svg)](https://www.mongodb.com/)
[![React](https://img.shields.io/badge/React-Latest-61DAFB.svg)](https://reactjs.org/)

> Modern containerized inventory management system with MongoDB, FastAPI, and React

![Project Banner](https://via.placeholder.com/1200x300/3498db/FFFFFF?text=Stellar+Stash+Cargo+Management)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Environment Variables](#-environment-variables)
- [Development](#-development)
- [Docker Configuration](#-docker-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🔍 Overview

Stellar Stash is a containerized full-stack application designed for cargo management. It uses a modern tech stack including:

- [**MongoDB**](https://www.mongodb.com/) for data storage
- [**FastAPI**](https://fastapi.tiangolo.com/) for the backend REST API
- [**React**](https://reactjs.org/) for the frontend interface
- [**Docker**](https://www.docker.com/) for containerization and easy deployment

The application allows users to manage inventory items with features for creating, reading, updating, and deleting items, along with activity logging and data persistence.

## ✨ Features

- 🔄 Complete CRUD operations for inventory items
- 📱 Responsive UI for various device sizes
- 🔒 API validation and error handling
- 📝 Activity logging for audit trails
- 🐳 Containerized for easy deployment
- 📊 Data persistence with MongoDB
- 📚 Interactive API documentation

## 📸 Screenshots

<details>
<summary>Click to see screenshots</summary>

### Dashboard View
![Dashboard](https://via.placeholder.com/800x450/3498db/FFFFFF?text=Dashboard+View)

### Item Management
![Items Management](https://via.placeholder.com/800x450/2ecc71/FFFFFF?text=Item+Management)

### API Documentation
![API Docs](https://via.placeholder.com/800x450/e74c3c/FFFFFF?text=API+Documentation)

</details>

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd cargoTest3

# Start all services
docker compose up -d

# Access the application
Frontend: http://localhost:4173
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs
```

## 📁 Project Structure

<details>
<summary>Click to expand file structure</summary>

```
cargoTest3/
│
├── backend/
│   ├── routes/                # API route definitions
│   │   ├── item_routes.py     # CRUD operations for items
│   │   └── routes.py          # Main routes file
│   │
│   ├── Dockerfile             # Backend container configuration
│   ├── main.py                # FastAPI application entry point
│   ├── db.py                  # Database connection configuration
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/                   # Frontend source code
│   ├── public/                # Static assets
│   ├── Dockerfile             # Frontend container configuration
│   └── package.json           # Node.js dependencies
│
├── docker-compose.yml         # Multi-container Docker configuration
└── README.md                  # Project documentation
```
</details>

## 📋 Prerequisites

- 🐳 [Docker](https://www.docker.com/get-started) and Docker Compose
- 🌿 [Git](https://git-scm.com/downloads) (for cloning the repository)
- 💻 Terminal/Command Prompt

> 💡 **Note:** No local installations of MongoDB, Python, or Node.js are required as everything runs in containers.

## 🔧 Installation & Setup

<details>
<summary>Detailed Installation Steps</summary>

### 1. Clone the repository

```bash
git clone <repository-url>
cd cargoTest3
```

### 2. Start the application

```bash
docker compose up -d
```

This command builds and starts all services defined in your docker-compose.yml file.

### 3. Verify all services are running

```bash
docker compose ps
```

You should see all three services (backend, frontend, and mongo) running.

</details>

## 🖥️ Usage

After starting the application, you can access:

- 🌐 **Frontend**: [http://localhost:4173](http://localhost:4173)
- 🔌 **Backend API**: [http://localhost:8000](http://localhost:8000)
- 📝 **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### Basic Operations:

- 👁️ View all items through the UI or API
- ➕ Create new items
- 🔄 Update existing items
- 🗑️ Delete items
- 📋 Browse the activity logs

## 🔌 API Endpoints

The backend provides the following RESTful endpoints:

<details>
<summary>View all API endpoints</summary>

### Items

- `GET /items` - Retrieve all items (with pagination)
- `GET /items/{item_id}` - Retrieve a specific item
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `DELETE /items/{item_id}` - Delete an item

### Example Item JSON:

```json
{
  "name": "Test Item",
  "description": "A test item",
  "quantity": 1,
  "category": "Test",
  "weight": 1.5
}
```
</details>

## 🔑 Environment Variables

<details>
<summary>Configure environment variables</summary>

The application uses the following environment variables which can be configured in the docker-compose.yml file:

### Backend:
- `MONGO_URI`: MongoDB connection string (default: `mongodb://mongo:27017/`)
- `MONGO_DB_NAME`: Database name (default: `stellar_stash`)

### Frontend:
- `VITE_API_URL`: URL to the backend API (default: `http://localhost:8000`)

### MongoDB:
- `MONGO_INITDB_ROOT_USERNAME`: Root username (if authentication is enabled)
- `MONGO_INITDB_ROOT_PASSWORD`: Root password (if authentication is enabled)

</details>

## 💻 Development

<details>
<summary>Development guide</summary>

### Backend Development:

1. Make changes to the FastAPI application code in the `backend/` directory
2. Rebuild and restart the container:
   ```bash
   docker compose up -d --build backend
   ```

### Frontend Development:

1. Make changes to the React application code in the `frontend/` directory
2. Rebuild and restart the container:
   ```bash
   docker compose up -d --build frontend
   ```

### Working with MongoDB:

1. Access the MongoDB shell:
   ```bash
   docker compose exec mongo mongosh
   ```

2. Direct database operations:
   ```javascript
   use stellar_stash
   db.items.find()
   ```

### Hot Reloading (Dev Mode)

For active development with hot reloading, you can modify your docker-compose.yml to mount local directories as volumes:

```yaml
# For backend hot reloading
volumes:
  - ./backend:/app

# For frontend hot reloading
volumes:
  - ./frontend:/app
  - /app/node_modules
```

</details>

## 🐳 Docker Configuration

<details>
<summary>Docker services and configuration</summary>

The project uses Docker Compose to manage three services:

### 1. Backend Service
```yaml
backend:
  build: ./backend
  ports:
    - "8000:8000"
  depends_on:
    - mongo
  environment:
    - MONGO_URI=mongodb://mongo:27017/
    - MONGO_DB_NAME=stellar_stash
```

### 2. Frontend Service
```yaml
frontend:
  build: ./frontend
  ports:
    - "4173:4173"
  depends_on:
    - backend
  environment:
    - VITE_API_URL=http://localhost:8000
```

### 3. MongoDB Service
```yaml
mongo:
  image: mongo:6
  ports:
    - "27017:27017"
  volumes:
    - mongo_data:/data/db
```

### Volumes
```yaml
volumes:
  mongo_data:
```

> 💡 **Tip:** For production deployment, consider adding appropriate environment variables for security, such as database credentials and API keys.

</details>

## 🔧 Troubleshooting

<details>
<summary>Common issues and solutions</summary>

### 1. 🔴 MongoDB Connection Issues

```bash
# Check if MongoDB container is running
docker compose ps

# View MongoDB logs
docker compose logs mongo

# Verify connection string in db.py
cat backend/db.py | grep MONGO_URI
```

**Solution:** Ensure the MongoDB container is running and the connection string is correctly configured in the environment variables.

### 2. 🔴 Route Errors or "Method Not Allowed"

**Problem:** API endpoints return unexpected errors or methods not allowed.

**Solutions:**
- Check that route prefixes don't have duplicate `/api` segments
- Ensure routes are properly registered in `main.py`
- Compare the URL you're accessing with the defined routes

### 3. 🔴 ObjectId Serialization Errors

**Problem:** MongoDB ObjectId fields cause serialization errors.

**Solution:** Verify that MongoDB documents are being properly serialized using the `serialize_mongodb_doc` helper function for all responses.

### 4. 🔴 Container Build Failures

```bash
# Check detailed build logs
docker compose build --no-cache <service>

# Verify dependency files
cat backend/requirements.txt
cat frontend/package.json
```

**Solution:** Ensure all required dependencies are listed in the appropriate files.

### 5. 🔄 Restart Services

If you encounter unexplained issues:

```bash
docker compose restart
```

### 6. 🧹 Reset the Environment

For a clean start:

```bash
docker compose down -v
docker compose up -d
```

⚠️ **Warning:** This will remove all data stored in the database!

</details>

## 👥 Contributing

<details>
<summary>Contribution guidelines</summary>

We welcome contributions to the Stellar Stash project! Here's how you can help:

### 1. 🍴 Fork the Repository

Start by forking the repository and cloning it locally.

### 2. 🌿 Create a Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. 💻 Make Your Changes

Make your changes and ensure they follow the project's coding style.

### 4. 🧪 Test Your Changes

Test your changes thoroughly to ensure they work as expected.

### 5. 📝 Commit Your Changes

```bash
git commit -m "Add amazing feature"
```

### 6. 🚀 Push to Your Branch

```bash
git push origin feature/amazing-feature
```

### 7. 📬 Submit a Pull Request

Submit a pull request with a clear description of your changes.

### Coding Standards

- Use consistent indentation (4 spaces for Python, 2 spaces for JavaScript)
- Write clear, descriptive commit messages
- Add appropriate comments to complex code sections
- Include tests for new features

</details>

## 📜 License

<details>
<summary>License information</summary>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Your Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

## 📞 Support & Contact

<details>
<summary>Get help and contact information</summary>

### Need Help?

If you need help with Stellar Stash, here are some resources:

- 📚 Check the [documentation](https://github.com/yourusername/cargoTest3/wiki)
- 🔍 Look for similar issues on the [issue tracker](https://github.com/yourusername/cargoTest3/issues)
- 💬 Join our [community chat](https://discord.gg/yourdiscord)

### Contact

- 📧 Email: [support@stellarstash.com](mailto:support@stellarstash.com)
- 🌐 Website: [www.stellarstash.com](https://www.stellarstash.com)
- 🐦 Twitter: [@StellarStash](https://twitter.com/StellarStash)

For business inquiries, please contact [business@stellarstash.com](mailto:business@stellarstash.com).

</details>

## 🙏 Acknowledgments

<details>
<summary>Credits and acknowledgments</summary>

- 🚀 [FastAPI](https://fastapi.tiangolo.com/) for the amazing API framework
- 🍃 [MongoDB](https://www.mongodb.com/) for the robust database
- ⚛️ [React](https://reactjs.org/) for the powerful frontend framework
- 🐳 [Docker](https://www.docker.com/) for containerization
- 📚 [Swagger UI](https://swagger.io/tools/swagger-ui/) for API documentation
- 👩‍💻 All contributors who have helped with the project
- 🎨 [Shields.io](https://shields.io/) for the README badges

</details>

## 🔒 Security Considerations

<details>
<summary>Security best practices</summary>

### Production Deployment

When deploying to production:

1. 🔐 **Use Environment Variables for Secrets**
   - Never hardcode credentials in your code or Docker configuration
   - Use a secure method to manage secrets in production

2. 🛡️ **Enable MongoDB Authentication**
   - Configure MongoDB with appropriate user credentials
   - Limit database user permissions

3. 🔍 **Regular Security Updates**
   - Keep all dependencies updated
   - Regularly update base Docker images

4. 🌐 **Use HTTPS**
   - Configure SSL/TLS for production deployments
   - Consider using a reverse proxy like Nginx

5. 🧪 **Input Validation**
   - Ensure all API inputs are properly validated
   - Sanitize data to prevent injection attacks

6. 📝 **Logging and Monitoring**
   - Implement proper logging for security events
   - Set up monitoring for suspicious activities

7. 🚪 **Rate Limiting**
   - Implement rate limiting to prevent abuse
   - Consider using API keys for authentication

</details>

---

<p align="center">
  Made with ❤️ by the Stellar Stash Team
</p>

<p align="center">
  <a href="#-stellar-stash---cargo-management-system">Back to top ⬆️</a>
</p>
