# Campaign Management API

A RESTful API built with FastAPI for managing marketing campaigns with full CRUD operations, SQLite database persistence, and comprehensive OpenAPI documentation.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete campaigns
- **Database Persistence**: SQLite database with SQLModel ORM
- **Input Validation**: Pydantic models for robust data validation
- **Auto-generated Documentation**: Interactive API docs at `/docs`
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Type Safety**: Full type hints throughout the codebase
- **Auto-incrementing IDs**: Database-managed campaign identifiers

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🔧 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository** (or create a new directory):

```bash
mkdir campaign-api
cd campaign-api
```

2. **Create a virtual environment**:

```bash
# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install fastapi uvicorn sqlmodel pydantic
```

4. **Save dependencies to requirements.txt**:

```bash
pip freeze > requirements.txt
```

Your `requirements.txt` should contain:

```
annotated-types==0.7.0
anyio==4.7.0
click==8.1.8
fastapi==0.115.6
greenlet==3.1.1
h11==0.14.0
idna==3.10
pydantic==2.11.1
pydantic-core==2.33.2
sniffio==1.3.1
SQLAlchemy==2.0.45
sqlmodel==0.0.30
starlette==0.41.3
typing-extensions==4.15.0
uvicorn==0.34.0
```

## 🏃 Quick Start

1. **Run the development server**:

```bash
fastapi dev main.py
```

Or alternatively:

```bash
uvicorn main:app --reload
```

2. **Access the API**:

- **API Base URL**: `http://127.0.0.1:8000/api/v1`
- **Interactive Documentation**: `http://127.0.0.1:8000/docs`
- **Alternative Documentation**: `http://127.0.0.1:8000/redoc`

3. **Test the API**:

```bash
# Get all campaigns
curl http://127.0.0.1:8000/api/v1/campaigns

# Create a new campaign
curl -X POST http://127.0.0.1:8000/api/v1/campaigns \
  -H "Content-Type: application/json" \
  -d '{"name": "Holiday Sale", "due_date": "2025-12-25T00:00:00"}'
```

## 📚 API Endpoints

### Root Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check - returns welcome message |

### Campaign Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/campaigns` | Get all campaigns | No |
| GET | `/campaigns/{id}` | Get campaign by ID | No |
| POST | `/campaigns` | Create new campaign | No |
| PUT | `/campaigns/{id}` | Update campaign | No |
| DELETE | `/campaigns/{id}` | Delete campaign | No |

## 📖 Request/Response Examples

### 1. Get All Campaigns

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/campaigns" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "campaigns": [
    {
      "campaign_id": 1,
      "name": "Summer Launch",
      "due_date": "2025-12-28T18:07:12.675599",
      "created_at": "2025-12-28T18:07:12.675811"
    },
    {
      "campaign_id": 2,
      "name": "Winter Launch",
      "due_date": "2025-12-28T18:07:12.675862",
      "created_at": "2025-12-28T18:07:12.675961"
    }
  ],
  "total": 2
}
```

### 2. Get Campaign by ID

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/campaigns/1" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "campaign_id": 1,
  "name": "Summer Launch",
  "due_date": "2025-12-28T18:07:12.675599",
  "created_at": "2025-12-28T18:07:12.675811"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Campaign with ID 999 not found"
}
```

### 3. Create Campaign

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/campaigns" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Black Friday Sale",
    "due_date": "2025-11-29T23:59:59"
  }'
```

**Response (201 Created):**
```json
{
  "campaign_id": 3,
  "name": "Black Friday Sale",
  "due_date": "2025-11-29T23:59:59",
  "created_at": "2025-12-28T18:30:00.123456"
}
```

**Validation Error (400 Bad Request):**
```json
{
  "detail": "Campaign name cannot be empty or whitespace"
}
```

### 4. Update Campaign

**Request:**
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/campaigns/1" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Summer Launch",
    "due_date": "2025-08-31T23:59:59"
  }'
```

**Response (200 OK):**
```json
{
  "campaign_id": 1,
  "name": "Updated Summer Launch",
  "due_date": "2025-08-31T23:59:59",
  "created_at": "2025-12-28T18:07:12.675811"
}
```

### 5. Delete Campaign

**Request:**
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/campaigns/1" \
  -H "accept: application/json"
```

**Response (204 No Content):**
```
(Empty response body)
```

## 🗄️ Database Schema

### Campaign Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique campaign identifier |
| `name` | VARCHAR | NOT NULL | Campaign name (1-200 characters) |
| `due_date` | DATETIME | NULLABLE, INDEXED | Campaign deadline |
| `created_at` | DATETIME | NULLABLE, INDEXED, DEFAULT NOW | Creation timestamp |

### Relationships

Currently, the Campaign table has no foreign key relationships. Future enhancements may include:
- User associations (created_by)
- Campaign categories
- Campaign metrics/analytics

## 📁 Project Structure

```
campaign-api/
│
├── main.py                 # Main application file
├── database.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── .venv/                 # Virtual environment (not in git)
│
└── __pycache__/           # Python cache (not in git)
```

### Code Organization in main.py

```python
# 1. Imports and Dependencies
# 2. Database Configuration (Campaign model)
# 3. Database Engine Setup
# 4. Session Management
# 5. Lifespan Manager (startup/shutdown)
# 6. FastAPI App Initialization
# 7. Pydantic Models (request/response validation)
# 8. API Endpoints
# 9. Error Handlers
```

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload (recommended for development)
fastapi dev main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.1 --port 8000
```

### Running in Production Mode

```bash
fastapi run main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables

You can customize the application using environment variables:

```bash
# Change the database file location
export DATABASE_URL="sqlite:///./custom_database.db"

# Change the port
uvicorn main:app --port 3000
```

## 🧪 Testing

### Manual Testing with curl

**Health Check:**
```bash
curl http://127.0.0.1:8000/api/v1/
```

**Create and Verify:**
```bash
# Create a campaign
curl -X POST http://127.0.0.1:8000/api/v1/campaigns \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Campaign", "due_date": "2025-12-31T23:59:59"}'

# Get all campaigns to verify
curl http://127.0.0.1:8000/api/v1/campaigns
```

### Testing with Swagger UI

1. Navigate to `http://127.0.0.1:8000/docs`
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"
6. View the response

### Automated Testing (Future Enhancement)

To add pytest tests, install:
```bash
pip install pytest httpx
```

Create `test_main.py`:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_campaign():
    response = client.post(
        "/api/v1/campaigns",
        json={"name": "Test Campaign", "due_date": "2025-12-31T00:00:00"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Campaign"
```

Run tests:
```bash
pytest test_main.py -v
```

## 🐛 Troubleshooting

### Issue: Module not found errors

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database locked error

**Solution:**
```bash
# Stop all running instances
# Delete the database file
rm database.db

# Restart the application (will create fresh database)
fastapi dev main.py
```

### Issue: Port already in use

**Solution:**
```bash
# Find and kill the process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
uvicorn main:app --port 8001
```

### Issue: CORS errors in browser

**Solution:** Add CORS middleware to `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: 422 Validation Error

**Solution:** Check your request body format matches the expected schema:
```bash
# Correct format:
curl -X POST http://127.0.0.1:8000/api/v1/campaigns \
  -H "Content-Type: application/json" \
  -d '{"name": "Campaign Name", "due_date": "2025-12-31T23:59:59"}'

# Common mistakes:
# - Missing Content-Type header
# - Invalid JSON format
# - Wrong date format (must be ISO 8601)
```

## 📝 API Validation Rules

### Campaign Name
- **Required**: Yes
- **Type**: String
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Cannot be**: Empty string or whitespace only
- **Auto-trimmed**: Leading/trailing whitespace removed

### Due Date
- **Required**: No (optional)
- **Type**: String (ISO 8601 format)
- **Format**: `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`
- **Examples**: 
  - `"2025-12-31"`
  - `"2025-12-31T23:59:59"`

## 🔒 Security Considerations

**Current Implementation:**
- No authentication/authorization
- Suitable for internal APIs or development only

**Production Recommendations:**
1. Add API key authentication
2. Implement OAuth2 or JWT tokens
3. Add rate limiting
4. Use HTTPS only
5. Validate and sanitize all inputs
6. Add request logging and monitoring
7. Set up database backups

## 🚀 Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement pagination for list endpoints
- [ ] Add search and filtering capabilities
- [ ] Include campaign status tracking
- [ ] Add file upload for campaign assets
- [ ] Implement soft deletes (archive campaigns)
- [ ] Add audit logging
- [ ] Create automated tests
- [ ] Add Docker support
- [ ] Implement caching
- [ ] Add API versioning
- [ ] Create admin dashboard

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the repository.

## 💡 PM's Tech Exploration: Learnings & Insights

As a Product Manager exploring this technology stack, here are key insights about the tools and frameworks used in this project:

### 🐍 Python as Backend Language

**Why It Works Well:**
- **Readability**: Python's syntax is clean and intuitive, making it easier for PMs to read and understand code
- **Rapid Development**: Quick iteration cycles mean faster prototyping and validation of product ideas
- **Rich Ecosystem**: Extensive libraries for data analysis, ML, and APIs make it versatile for product experiments
- **Lower Learning Curve**: Easier for non-engineers to pick up, enabling better technical conversations

**Trade-offs to Consider:**
- **Performance**: Slower than compiled languages (Go, Rust, Java) for high-traffic applications
- **Memory Usage**: Can be resource-intensive at scale
- **Type Safety**: Dynamically typed (though type hints help), which can lead to runtime errors
- **Mobile Development**: Not ideal for mobile apps (need Swift/Kotlin)

**PM Takeaway**: Perfect for MVPs, internal tools, data APIs, and ML services. Consider other languages for high-performance, real-time systems.

---

### ⚡ FastAPI Framework

**Advantages:**
- **Speed to Market**: Build APIs incredibly fast - this entire CRUD API was built in under 200 lines
- **Auto Documentation**: `/docs` endpoint automatically generates interactive API documentation (huge win for developer experience)
- **Modern Python**: Uses latest Python features (type hints, async/await) making code more maintainable
- **Data Validation**: Built-in request/response validation reduces bugs and improves reliability
- **Performance**: One of the fastest Python frameworks, comparable to Node.js and Go
- **Developer Experience**: Excellent error messages and IDE autocomplete support

**Disadvantages:**
- **Newer Framework**: Smaller community compared to Flask/Django (fewer Stack Overflow answers)
- **Learning Curve**: Requires understanding of Python type hints and async programming
- **Ecosystem Maturity**: Fewer third-party plugins compared to Django
- **Over-engineering Risk**: Can be overkill for simple scripts or one-off tasks

**PM Perspective:**
- **When to Use**: Building microservices, RESTful APIs, data pipelines, ML model APIs
- **When to Avoid**: Simple websites (use Flask), full-stack apps with admin panels (use Django)
- **Team Impact**: Reduces API development time by 30-40% vs traditional frameworks

---

### 🗄️ SQLModel + SQLite

**SQLModel Advantages:**
- **Type Safety**: Combines Pydantic validation with SQLAlchemy ORM - catches errors before runtime
- **Code Reduction**: Single model definition for both API and database (DRY principle)
- **Developer Productivity**: Less boilerplate code means faster feature development
- **Easy Testing**: Simple to mock and test database operations
- **Modern Python**: Leverages type hints for better IDE support

**SQLite Advantages:**
- **Zero Configuration**: No database server to install, configure, or maintain
- **Perfect for Prototypes**: Get started in seconds, not hours
- **Portable**: Single file database - easy to backup, copy, and share
- **Low Resource Usage**: Minimal memory footprint
- **Good Enough**: Handles 100K+ records easily for most product prototypes

**Disadvantages:**
- **Scalability Limits**: SQLite struggles with >100K requests/day or multiple concurrent writers
- **No Built-in Replication**: Can't easily scale horizontally
- **Limited Data Types**: Fewer column types vs PostgreSQL/MySQL
- **File-based Locking**: Entire database locks on write operations
- **Production Concerns**: Not recommended for production apps with multiple servers

**PM Decision Framework:**

| Use SQLite When: | Use PostgreSQL/MySQL When: |
|------------------|----------------------------|
| Building MVP/prototype | Production application |
| Internal tools | >10K daily active users |
| Single server deployment | Multiple servers needed |
| Read-heavy workloads | Write-heavy workloads |
| Quick demos | Mission-critical data |

---

### 📊 Technical Debt Considerations

**Current Architecture Strengths:**
1. ✅ **Fast to build** - Perfect for validating product ideas quickly
2. ✅ **Easy to understand** - Simple codebase that new developers can grok in an hour
3. ✅ **Low operational complexity** - No database server to manage

**Known Technical Debt:**
1. ⚠️ **No authentication** - Anyone can access/modify data
2. ⚠️ **No rate limiting** - Vulnerable to abuse
3. ⚠️ **Single database file** - No redundancy or backups
4. ⚠️ **No monitoring** - Can't track usage or errors in production
5. ⚠️ **No caching** - Every request hits the database

**Migration Path to Production:**

```
Phase 1: MVP (Current) ✅
- SQLite + FastAPI
- No auth
- Single server
- Cost: $5-10/month (Heroku/Railway)

Phase 2: Beta (0-1K users) 🎯
- Migrate to PostgreSQL
- Add API key authentication
- Add basic monitoring (Sentry)
- Cost: $25-50/month

Phase 3: Production (1K-10K users) 🚀
- Add JWT authentication
- Implement caching (Redis)
- Add rate limiting
- Horizontal scaling (multiple servers)
- Cost: $100-200/month

Phase 4: Scale (10K+ users) 📈
- Database read replicas
- CDN for static assets
- Auto-scaling infrastructure
- Advanced monitoring and alerting
- Cost: $500+/month
```

---

### 🎯 Key Learnings for Product Managers

**1. Technology Choices Are Product Decisions**
- The right tech stack can 3x your development speed
- Wrong choices create technical debt that slows down every future feature
- Always match technology to your product stage (MVP vs Scale)

**2. Developer Experience = Product Velocity**
- FastAPI's auto-documentation means engineers spend less time writing docs
- Good error messages reduce debugging time by 50%+
- Type safety catches bugs before they reach production

**3. Trade-offs Are Inevitable**
- SQLite is fast to start but limits scale
- FastAPI is great for APIs but not for server-rendered HTML
- Every technology choice is a trade-off between development speed, performance, and scalability

**4. Start Simple, Migrate When Needed**
- Don't over-engineer for scale you don't have yet
- It's easier to migrate from SQLite → PostgreSQL than to debug a complex microservices setup
- Premature optimization is the root of all evil (and delayed launches)

**5. Documentation Is a Feature**
- Auto-generated API docs (`/docs`) dramatically improve developer adoption
- Good README reduces onboarding time for new engineers from days to hours
- Clear examples are more valuable than comprehensive reference docs

---

### 🔮 When to Choose This Stack

**✅ Perfect For:**
- Internal tools and admin dashboards
- MVP and prototype APIs
- Data processing pipelines
- ML model serving
- Microservices in larger systems
- Projects where time-to-market is critical

**❌ Not Ideal For:**
- Consumer-facing mobile apps (use Swift/Kotlin + Firebase)
- Real-time applications (use WebSockets, Go, or Node.js)
- WordPress-style websites (use PHP or Next.js)
- High-frequency trading systems (use C++ or Rust)
- Embedded systems (use C or Rust)

---

### 📚 Recommended Learning Path for PMs

1. **Week 1**: Learn Python basics (variables, functions, loops)
2. **Week 2**: Understand HTTP/REST APIs (GET, POST, PUT, DELETE)
3. **Week 3**: Build this project from scratch
4. **Week 4**: Add features (search, pagination, filtering)
5. **Month 2**: Learn SQL and database design
6. **Month 3**: Explore authentication and security

**Resources:**
- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

---

### 💼 Business Impact Summary

| Metric | Impact |
|--------|--------|
| **Development Time** | 10-20 hours for full CRUD API (vs 40-60 with traditional frameworks) |
| **Time to First API Call** | 15 minutes (vs 2-4 hours with other stacks) |
| **Maintenance Overhead** | Low - single file database, no servers to manage |
| **Scaling Ceiling** | ~10K daily active users before migration needed |
| **Learning Curve** | Medium - 2-4 weeks for PMs with no coding background |
| **Cost to Run (MVP)** | $5-10/month on cloud platforms |

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database ORM: [SQLModel](https://sqlmodel.tiangolo.com/)
- Data validation: [Pydantic](https://docs.pydantic.dev/)

---

**Happy Coding!** 🎉

*Built with ❤️ by a PM exploring the world of backend development*
