# 🏦 Digital Legacy Vault

> A secure, automated system for managing digital assets and ensuring their seamless transfer to beneficiaries upon verified death.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

## 📖 Table of Contents

- [Overview](#-overview)
- [✨ Features](#-features)
- [🛠 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📁 Project Structure](#-project-structure)
- [🔧 API Documentation](#-api-documentation)
- [🎯 Demo Workflow](#-demo-workflow)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Overview

The **Digital Legacy Vault** is a sophisticated system designed to solve the modern problem of digital asset inheritance. It provides a secure platform for users to catalog their digital assets, designate beneficiaries, and automate the transfer process through a verified multi-signature death confirmation workflow.

**Use Cases:**
- 💼 Estate planning for digital natives
- 🔐 Secure cryptocurrency wallet inheritance  
- 📱 Social media account memorialization
- ☁️ Cloud storage and document transfer
- 🏦 Financial account access management

## ✨ Features

### 🔒 Security & Authentication
- **JWT Token Authentication** - Secure API access
- **Password Hashing** - bcrypt for user credentials
- **Role-based Access** - User-specific data visibility

### 💾 Data Management
- **MariaDB Temporal Tables** - Automatic audit trails and historical tracking
- **JSON Column Support** - Flexible metadata storage for diverse asset types
- **Data Integrity** - Foreign key constraints and transaction safety

### ⚡ Core Functionality
- **Digital Asset Cataloging** - Support for crypto wallets, social media, documents, and more
- **Beneficiary Management** - Percentage-based asset distribution
- **Multi-signature Verification** - Death confirmation requiring multiple approvals
- **Automated Transfers** - Seamless asset transfer upon verified death events
- **Legal Audit Trail** - Complete transaction history for compliance

### 🐳 Deployment & Development
- **Docker Containerization** - Consistent development and production environments
- **Health Checks** - Automated service monitoring
- **Hot Reload** - Development-friendly auto-reload functionality

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | FastAPI (Python 3.9) | High-performance REST API framework |
| **Database** | MariaDB 10.8 | Enterprise-grade SQL with temporal tables |
| **ORM** | SQLAlchemy 2.0 | Python database toolkit and ORM |
| **Authentication** | JWT + bcrypt | Secure token-based authentication |
| **Containerization** | Docker + Docker Compose | Environment consistency and deployment |
| **API Documentation** | Swagger UI | Interactive API documentation |

## 🚀 Quick Start

### Prerequisites

- **Docker** & **Docker Compose** ([Install Guide](https://docs.docker.com/get-docker/))
- **Git** (for version control)
- **4GB RAM** available for containers

### 📥 Installation

#### Step 1: Clone and Setup
```bash
# Create project directory
mkdir digital_legacy_vault && cd digital_legacy_vault

# Create the complete project structure (copy all files from the provided codebase)
# Ensure all files are in their correct locations as per the structure below
```

#### Step 2: Start Services
```bash
# Build and start all services in detached mode
docker-compose up -d --build

# Verify services are running
docker-compose ps
```

**Expected Output:**
```
Name                          Command              State           Ports         
-----------------------------------------------------------------------------------
legacy_vault-api-1   uvicorn app.main:app --host ...   Up      0.0.0.0:8000->8000/tcp
legacy_vault-db-1    docker-entrypoint.sh mysqld      Up      0.0.0.0:3306->3306/tcp
```

#### Step 3: Wait for Initialization
```bash
# Services need 30-60 seconds to initialize completely
echo "⏳ Initializing services... (this may take up to 60 seconds)"
sleep 45
```

#### Step 4: Run Demo
```bash
# Execute the comprehensive demo script
python demo_script.py
```

#### Step 5: Access API Documentation
Open your browser and navigate to:
```
http://localhost:8000/docs
```

## 📁 Project Structure

```
digital_legacy_vault/
├── 🐳 docker-compose.yml          # Multi-container orchestration
├── 🐳 Dockerfile                  # API service container definition
├── 📄 requirements.txt            # Python dependencies
├── 🐍 demo_script.py              # Comprehensive system demonstration
├── 📁 migrations/
│   └── 📄 init.sql                # Database schema with temporal tables
└── 📁 app/                        # FastAPI application
    ├── 🐍 main.py                 # FastAPI application and route definitions
    ├── 🐍 config.py               # Application configuration and settings
    ├── 🐍 database.py             # Database connection and session management
    ├── 🐍 auth.py                 # Authentication and security utilities
    ├── 📁 models/                 # SQLAlchemy database models
    │   ├── 🐍 user.py             # User model with temporal versioning
    │   ├── 🐍 asset.py            # Digital asset and beneficiary models
    │   └── 🐍 event.py            # Death verification and transfer models
    ├── 📁 schemas/                # Pydantic request/response schemas
    │   ├── 🐍 user.py             # User validation schemas
    │   ├── 🐍 asset.py            # Asset and beneficiary schemas
    │   └── 🐍 event.py            # Event and transfer schemas
    └── 📁 crud/                   # Database operations
        ├── 🐍 user.py             # User CRUD operations
        ├── 🐍 asset.py            # Asset and beneficiary operations
        └── 🐍 event.py            # Death verification and transfer operations
```

## 🔧 API Documentation

### 🔑 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Register new user | ❌ |
| `POST` | `/auth/login` | Login and receive JWT token | ❌ |

**Example Registration:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "full_name": "John Doe",
    "date_of_birth": "1980-01-15"
  }'
```

### 💼 Asset Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/assets` | Create new digital asset | ✅ |
| `GET` | `/assets` | List user's assets | ✅ |
| `GET` | `/assets/{id}` | Get asset details with beneficiaries | ✅ |
| `POST` | `/assets/{id}/beneficiaries` | Add beneficiary to asset | ✅ |

**Example Asset Creation:**
```bash
curl -X POST "http://localhost:8000/assets" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "crypto_wallet",
    "name": "Bitcoin Main Wallet",
    "description": "Primary Bitcoin cold storage",
    "access_instructions": {
      "wallet_address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "recovery_phrase": "encrypted_data"
    },
    "metadata": {
      "currency": "BTC",
      "estimated_value": 50000
    }
  }'
```

### 📋 Death Verification Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/death-verifications` | Initiate death verification process | ✅ |
| `POST` | `/death-verifications/{id}/approvals` | Approve/reject death event | ✅ |

### 🔄 Transfer Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/transfers` | View asset transfer history | ✅ |

### 🎪 Demo Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/demo/users` | View all users (demo only) | ❌ |
| `GET` | `/demo/death-verifications` | View all death events | ❌ |
| `GET` | `/demo/asset-transfers` | View all transfers | ❌ |

## 🎯 Demo Workflow

The comprehensive demo script (`demo_script.py`) demonstrates a complete user journey:

### 👥 User Registration & Authentication
1. **Three users register**: John (asset owner), Jane and Bob (beneficiaries)
2. **JWT tokens acquired** for authenticated API access

### 💾 Digital Asset Creation
1. **John creates assets**:
   - Bitcoin cryptocurrency wallet
   - Twitter social media account
2. **Assets stored** with encrypted access instructions and metadata

### 👥 Beneficiary Assignment
1. **John designates beneficiaries** for Bitcoin wallet:
   - Jane: 60% share
   - Bob: 40% share
2. **Multi-signature approval** required for both beneficiaries

### 📜 Death Verification Process
1. **Jane initiates death verification** for John with:
   - Death certificate evidence
   - Required approvals: 2
2. **Multi-signature workflow**:
   - Jane approves the verification
   - Bob approves the verification
3. **Automatic status update** to "verified" upon sufficient approvals

### 🔄 Automated Asset Transfer
1. **System automatically creates** transfer records for all John's assets
2. **Transfers distributed** according to beneficiary percentages
3. **Complete audit trail** maintained for legal compliance

### 📊 Demo Output Example
```
🚀 DIGITAL LEGACY VAULT - DEMO WORKFLOW
============================================================

1. 📝 CREATING USERS
   ✅ Registered: john@example.com
   ✅ Logged in: john@example.com (ID: 1)
   ✅ Registered: jane@example.com (ID: 2)
   ✅ Registered: bob@example.com (ID: 3)

2. 💼 JOHN CREATING DIGITAL ASSETS
   ✅ Created asset: Bitcoin Wallet (ID: 1)
   ✅ Created asset: Twitter Account (ID: 2)

3. 👥 ADDING BENEFICIARIES TO BITCOIN WALLET
   ✅ Added beneficiary: jane@example.com (60.0%)
   ✅ Added beneficiary: bob@example.com (40.0%)

4. 📋 JANE INITIATING DEATH VERIFICATION FOR JOHN
   ✅ Created death verification event: ID 1
   📊 Status: pending
   👥 Required approvals: 2

5. 🔐 MULTI-SIGNATURE APPROVAL PROCESS
   ✅ Jane approved the death verification
   📊 Current approvals: 1/2
   ✅ Bob approved the death verification
   📊 Current approvals: 2/2
   📊 Event status: verified

6. 🔄 CHECKING ASSET TRANSFERS
   ✅ Created 2 asset transfers
   ⏳ Transfer: Bitcoin Wallet to jane@example.com (pending)
   ⏳ Transfer: Bitcoin Wallet to bob@example.com (pending)

🎉 DEMO COMPLETED SUCCESSFULLY!
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### ❌ "Connection Refused" Errors
**Problem:** API or database not responding
```bash
# Check service status
docker-compose ps

# View logs for errors
docker-compose logs api
docker-compose logs db

# Restart services
docker-compose restart
```

#### ❌ "Port Already in Use"
**Problem:** Ports 8000 or 3306 occupied
```bash
# Find processes using ports
lsof -i :8000
lsof -i :3306

# Alternative: Change ports in docker-compose.yml
# ports:
#   - "8001:8000"  # Change host port
#   - "3307:3306"
```

#### ❌ Database Connection Issues
**Problem:** MariaDB not initializing properly
```bash
# Check database logs
docker-compose logs db

# Reset database (warning: deletes all data)
docker-compose down -v
docker-compose up -d

# Manual database connection test
docker-compose exec db mysql -u user -ppassword legacy_vault -e "SHOW TABLES;"
```

#### ❌ Demo Script Failures
**Problem:** Demo script can't connect to API
```bash
# Wait longer for initialization
sleep 60
python demo_script.py

# Check API health manually
curl http://localhost:8000/
```

#### ❌ "Module Not Found" Errors
**Problem:** Python dependencies issues
```bash
# Rebuild containers
docker-compose build --no-cache

# Check requirements installation
docker-compose exec api pip list | grep fastapi
```

### 🛠 Debugging Commands

**Service Status Check:**
```bash
docker-compose ps
docker-compose logs -f api      # Follow API logs
docker-compose logs -f db       # Follow database logs
```

**Database Inspection:**
```bash
# Connect to database
docker-compose exec db mysql -u user -ppassword legacy_vault

# Check tables and data
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM digital_assets;
SELECT * FROM death_verification_events;
```

**API Health Check:**
```bash
curl http://localhost:8000/
# Expected: {"message":"Digital Legacy Vault API",...}
```

## 🤝 Contributing

We welcome contributions to the Digital Legacy Vault! Here's how you can help:

### 🎯 Development Setup

1. **Fork the repository**
2. **Set up development environment:**
```bash
git clone https://github.com/your-username/digital-legacy-vault.git
cd digital-legacy-vault

# Start development environment
docker-compose up -d

# Run tests (when available)
docker-compose exec api pytest
```

### 📝 Contribution Guidelines

- **Code Style**: Follow PEP 8 and use Black formatter
- **Testing**: Include tests for new features
- **Documentation**: Update README and API docs for changes
- **Commits**: Use conventional commit messages
- **Branches**: Create feature branches from `main`

### 🐛 Reporting Issues

When reporting bugs, please include:
- **Environment details** (OS, Docker version, etc.)
- **Steps to reproduce** the issue
- **Error messages** and logs
- **Expected vs actual behavior**

### 💡 Feature Requests

We're particularly interested in:
- 🔐 Enhanced encryption mechanisms
- 🌐 Blockchain integration for verification
- 📱 Mobile application development
- 🏛 Legal compliance frameworks
- 🔌 Third-party service integrations

## 📄 License

This project is proprietary.  
Use, distribution, or modification of any part of this codebase requires written permission from the author.


### 🎓 Educational Use
This project is excellent for:
- **Computer Science students** learning API development
- **DevOps engineers** understanding containerization
- **Security researchers** studying authentication systems
- **Database administrators** exploring temporal tables

### 📞 Support

- **Documentation**: [API Docs](http://localhost:8000/docs)
- **Issues**: [GitHub Issues](https://github.com/your-username/digital-legacy-vault/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/digital-legacy-vault/discussions)

---

<div align="center">

**Built with ❤️ for a more secure digital future**

*If this project helps you, please consider giving it a ⭐!*

</div>