# PumpSwap Auto Trader

Automated trading application with React Vite frontend and FastAPI backend, containerized with Docker Compose. Uses technical analysis indicators (RSI, MACD) to generate trading signals for cryptocurrency tokens.

## Project Overview

This project provides a full-stack automated trading application that analyzes cryptocurrency tokens using technical analysis indicators to identify potential trading opportunities. The application uses **Relative Strength Index (RSI)** and **Moving Average Convergence Divergence (MACD)** indicators to generate buy/sell signals based on market momentum and trend analysis.

## Technical Trading Strategy

### Overview

The application uses technical analysis indicators to identify potential trading opportunities in cryptocurrency tokens. The primary indicators implemented are:

- **RSI (Relative Strength Index)**: Momentum oscillator for identifying overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Trend-following momentum indicator for identifying trend changes

The system analyzes token price movements, calculates technical indicators on OHLCV (Open, High, Low, Close, Volume) data, and filters tokens based on customizable criteria to generate trading signals.

### RSI (Relative Strength Index)

RSI is a momentum oscillator that measures the speed and magnitude of price movements. It ranges from 0 to 100 and helps identify overbought and oversold conditions.

#### RSI Calculation

The RSI is calculated using the pandas-ta library on OHLCV data fetched from Birdeye API:

1. **Data Fetching**: OHLCV data is fetched from Birdeye API for specified timeframes (default: 5-second candles)
2. **Data Processing**: Raw OHLCV data is converted to pandas DataFrame format
3. **RSI Calculation**: RSI is calculated using the formula:
   ```
   RSI = 100 - (100 / (1 + RS))
   where RS = Average Gain / Average Loss
   ```
4. **Default Period**: 14 periods (configurable via API parameters)

#### RSI Trading Signals

RSI values are interpreted as follows:

- **RSI < 30**: Oversold condition - Potential **buy signal** (token may be undervalued)
- **RSI > 70**: Overbought condition - Potential **sell signal** (token may be overvalued)
- **RSI 30-70**: Neutral zone - No strong signal

#### RSI Filtering Strategy

The application filters tokens based on RSI values:

- **Oversold Tokens**: `rsi_min=0, rsi_max=30` - Finds tokens that may be undervalued (potential buy opportunities)
- **Overbought Tokens**: `rsi_min=70, rsi_max=100` - Finds tokens that may be overvalued (potential sell opportunities)
- **Neutral Zone**: `rsi_min=30, rsi_max=70` - Finds tokens in neutral momentum range

#### RSI Divergence

RSI divergence occurs when price makes new highs/lows but RSI doesn't, indicating potential trend reversals:

- **Bullish Divergence**: Price makes lower lows, but RSI makes higher lows → Potential upward reversal
- **Bearish Divergence**: Price makes higher highs, but RSI makes lower highs → Potential downward reversal

### MACD (Moving Average Convergence Divergence)

MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a token's price. It consists of three components:

#### MACD Components

- **MACD Line**: 12-period EMA - 26-period EMA (fast EMA minus slow EMA)
- **Signal Line**: 9-period EMA of MACD line
- **Histogram**: MACD line - Signal line (visual representation of momentum)

#### MACD Trading Signals

MACD generates trading signals through crossovers and histogram analysis:

1. **Bullish Signal (Buy)**:
   - MACD line crosses **above** signal line (bullish crossover)
   - Histogram turns positive (momentum increasing)
   - Indicates potential upward trend

2. **Bearish Signal (Sell)**:
   - MACD line crosses **below** signal line (bearish crossover)
   - Histogram turns negative (momentum decreasing)
   - Indicates potential downward trend

3. **Divergence Signals**:
   - **Bullish Divergence**: Price makes lower lows, but MACD makes higher lows → Potential upward reversal
   - **Bearish Divergence**: Price makes higher highs, but MACD makes lower highs → Potential downward reversal

#### MACD Zero Line Crossovers

- **Above Zero Line**: Bullish momentum (uptrend)
- **Below Zero Line**: Bearish momentum (downtrend)
- **Crossing Above Zero**: Strong buy signal
- **Crossing Below Zero**: Strong sell signal

### Combined Trading Strategy

A comprehensive trading strategy combines multiple indicators and filters:

#### Multi-Criteria Filtering

The application filters tokens based on multiple criteria:

1. **RSI Range**: Filter tokens by RSI min/max values
   - Example: `rsi_min=20, rsi_max=40` finds oversold tokens
   - Example: `rsi_min=60, rsi_max=80` finds overbought tokens

2. **Market Cap**: Filter by market capitalization (in thousands)
   - Example: `mc_min=10, mc_max=1000` finds tokens with market cap between $10K and $1M

3. **Token Age**: Filter by token age (in minutes)
   - Example: `age_min=0, age_max=60` finds tokens less than 1 hour old

4. **Liquidity**: Filter by liquidity in USD
   - Example: `liquidity_min=50000` finds tokens with at least $50K liquidity

5. **Volume**: Filter by trading volume (1h, 4h, or 24h)
   - Example: `volume_min=100000, volume_timeframe=1h` finds tokens with at least $100K volume in 1 hour

#### Signal Generation Logic

**Example Combined Signals**:

- **Strong Buy Signal**: 
  - RSI < 30 (oversold) 
  - MACD bullish crossover (MACD line crosses above signal line)
  - High volume (validates interest)
  - Sufficient liquidity (ensures tradeability)
  - Market cap in target range (filters out micro/suspicious tokens)

- **Strong Sell Signal**: 
  - RSI > 70 (overbought)
  - MACD bearish crossover (MACD line crosses below signal line)
  - Decreasing volume (loss of momentum)
  - Histogram turning negative

- **Wait Signal**: 
  - RSI 30-70 (neutral)
  - MACD in consolidation (no clear crossover)
  - Low volume (lack of interest)
  - Insufficient liquidity (risk of slippage)

#### Risk Management

- **Liquidity Check**: Ensures sufficient liquidity to avoid slippage
- **Volume Validation**: Confirms real trading activity
- **Market Cap Filtering**: Avoids extremely small or suspicious tokens
- **Age Filtering**: Can focus on new tokens or established ones
- **Multi-Indicator Confirmation**: Requires both RSI and MACD signals for stronger confidence

### Data Flow

1. **Token Discovery**: Scheduled job fetches new tokens from Birdeye API
2. **Data Storage**: Token metadata (name, address, market cap, liquidity, volume) stored in SQLite database
3. **OHLCV Fetching**: On-demand OHLCV data fetching from Birdeye API for indicator calculation
4. **Indicator Calculation**: Real-time RSI and MACD calculation using pandas-ta on fetched OHLCV data
5. **Filtering**: Multi-criteria filtering applied to identify trading opportunities
6. **Signal Generation**: Trading signals generated based on indicator values and crossovers
7. **API Response**: Filtered tokens with indicator values and signals returned to frontend

### Rate Limiting & Performance

The system implements rate limiting to respect Birdeye API limits:

- **OHLCV API**: 15 requests per second (15 rps)
- **Token Fetching**: Configurable via `BIRDEYE_MAX_WORKERS` (default: 15 workers)
- **Concurrent Processing**: Uses ThreadPoolExecutor for parallel indicator calculations

#### Performance Optimization

- **Database-Level Filtering**: Age, market cap, liquidity, and volume filters applied at database query level for performance
- **Concurrent Calculation**: Multiple tokens processed in parallel (up to 15 concurrent workers)
- **Efficient Data Processing**: Uses pandas for fast OHLCV data manipulation
- **Caching**: OHLCV data can be cached to reduce API calls (future enhancement)

### Trading Signal Interpretation

#### Buy Signals (Oversold Conditions)

- **RSI < 30**: Token is oversold, potential reversal upward
- **MACD Bullish Crossover**: MACD line crosses above signal line
- **MACD Above Zero**: Strong bullish momentum
- **High Volume**: Confirms market interest
- **Adequate Liquidity**: Ensures ability to enter/exit positions
- **Reasonable Market Cap**: Filters out suspicious or manipulated tokens

#### Sell Signals (Overbought Conditions)

- **RSI > 70**: Token is overbought, potential reversal downward
- **MACD Bearish Crossover**: MACD line crosses below signal line
- **MACD Below Zero**: Strong bearish momentum
- **Decreasing Volume**: Loss of momentum
- **Negative Histogram**: Decreasing momentum

#### Neutral/Hold Signals

- **RSI 30-70**: Neutral momentum zone
- **MACD Consolidation**: No clear trend direction
- **Low Volume**: Lack of market interest
- **Insufficient Liquidity**: Risk of slippage

## Project Structure

```
pumpswap-auto-trade-x/
├── frontend/                    # React Vite frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   └── Layout.tsx       # Main layout component
│   │   ├── pages/               # Page components
│   │   │   ├── Home.tsx         # Home page
│   │   │   ├── Dashboard.tsx    # Dashboard page
│   │   │   └── Tokens.tsx       # Tokens page
│   │   ├── services/            # API services
│   │   │   └── api.ts           # API client configuration
│   │   ├── App.tsx              # Main App component with routing
│   │   ├── App.css              # App styles
│   │   ├── main.tsx             # Application entry point
│   │   └── index.css            # Global styles
│   ├── public/                  # Static assets
│   ├── Dockerfile               # Frontend Docker configuration
│   ├── package.json             # Frontend dependencies and scripts
│   ├── vite.config.ts           # Vite configuration
│   ├── tsconfig.json            # TypeScript configuration
│   └── tailwind.config.js       # Tailwind CSS configuration
│
├── backend/                     # FastAPI backend application
│   ├── app/
│   │   ├── api/                 # API routes
│   │   │   └── v1/              # API version 1
│   │   │       ├── endpoints/   # API endpoint modules
│   │   │       │   ├── health.py    # Health check endpoints
│   │   │       │   ├── stats.py     # Statistics endpoints
│   │   │       │   └── tokens.py     # Token-related endpoints
│   │   │       └── __init__.py      # API router configuration
│   │   ├── core/                # Core configuration
│   │   │   ├── config.py        # Application settings and configuration
│   │   │   └── database.py      # Database initialization and setup
│   │   ├── models/              # Data models
│   │   │   └── token.py         # Token data models
│   │   └── services/            # Business logic services
│   │       ├── scheduler.py     # Task scheduler service
│   │       └── ta.py            # Technical analysis utilities
│   ├── tests/                   # Test files
│   ├── main.py                  # FastAPI application entry point
│   ├── Dockerfile               # Backend Docker configuration
│   ├── requirements.txt         # Python dependencies
│   └── pyproject.toml           # Python project configuration
│
├── docker-compose.yml           # Docker Compose configuration
├── Makefile                     # Makefile for Docker Compose commands
└── README.md                    # Main project documentation
```

## Technology Stack

### Frontend
- **React 18** - UI library
- **Vite 5** - Build tool and dev server
- **TypeScript** - Type safety
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Vitest** - Testing framework

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Programming language
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM and database toolkit
- **Uvicorn** - ASGI server
- **APScheduler** - Task scheduling
- **Pandas** - Data manipulation
- **Pandas-TA** - Technical analysis indicators (RSI, MACD)

## Prerequisites

- **Docker** and **Docker Compose** (recommended)
- **Node.js** 20+ and npm (for local frontend development)
- **Python** 3.11+ (for local backend development)

## Quick Start

### Using Docker Compose (Recommended)

The easiest way to get started is using Docker Compose with the provided Makefile:

```bash
# Check if Docker is installed
make check-docker

# Install Docker (if not installed, Ubuntu/Debian)
make install-docker

# Deploy the application (build and start)
make deploy

# Or start services in detached mode
make up

# View logs
make logs

# Check service status
make status
```

**Services will be available at:**
- Frontend: `http://localhost:3000` (or `http://YOUR_SERVER_IP:3000`)
- Backend: `http://localhost:8000` (or `http://YOUR_SERVER_IP:8000`)
- API Docs: `http://localhost:8000/docs`

### Using Docker Compose Directly

```bash
# Build and start services
docker compose up --build

# Start in detached mode
docker compose up -d

# Stop services
docker compose down
```

## Makefile Commands

The project includes a comprehensive Makefile for managing Docker Compose operations:

### Service Management
- `make deploy` - Build and start all services (production ready)
- `make up` - Start all services in detached mode
- `make up-dev` - Start all services with logs (development mode)
- `make down` - Stop and remove all containers
- `make stop` - Stop all services
- `make start` - Start all services
- `make restart` - Restart all services
- `make status` - Show status of all services

### Building
- `make build` - Build all Docker images
- `make rebuild` - Rebuild all Docker images (no cache)

### Logs
- `make logs` - Show logs from all services
- `make logs-backend` - Show logs from backend service only
- `make logs-frontend` - Show logs from frontend service only
- `make logs-scheduler` - Show scheduler/cronjob logs (filtered)

### Development
- `make shell-backend` - Open shell in backend container
- `make shell-frontend` - Open shell in frontend container
- `make test-backend` - Run backend tests in container
- `make test-frontend` - Run frontend tests in container
- `make lint-backend` - Run backend linters in container
- `make lint-frontend` - Run frontend linters in container

### Utilities
- `make ps` - List running containers
- `make clean` - Remove containers, networks, and volumes
- `make clean-all` - Clean everything including images
- `make check-docker` - Check if Docker is installed and running
- `make install-docker` - Install Docker (Ubuntu/Debian)
- `make check-db` - Check backend database
- `make fetch-tokens` - Manually trigger token fetch job

### Help
- `make help` - Show all available commands

## Docker Compose Configuration

The `docker-compose.yml` file defines two main services:

### Backend Service
- **Container Name**: `pumpswap-backend`
- **Port**: `8000`
- **Build Context**: `./backend`
- **Volumes**: 
  - `./backend:/app` - Mounts backend code for development
  - `./backend/pumpswap.db:/app/pumpswap.db` - Persists database
- **Environment Variables**:
  - `DATABASE_URL`: SQLite database connection string
  - `CORS_ORIGINS`: CORS configuration (default: `*`)

### Frontend Service
- **Container Name**: `pumpswap-frontend`
- **Port**: `3000`
- **Build Context**: `./frontend`
- **Volumes**:
  - `./frontend:/app` - Mounts frontend code for development
  - `/app/node_modules` - Preserves node_modules
- **Environment Variables**:
  - `VITE_API_URL`: Backend API URL (default: `http://localhost:8000`)
- **Depends On**: Backend service

### Network
- **Network Name**: `pumpswap-network`
- **Driver**: Bridge

## Frontend Structure

### Components
- **Layout.tsx**: Main layout component that wraps all pages, typically includes navigation and common UI elements

### Pages
- **Home.tsx**: Landing/home page
- **Dashboard.tsx**: Main dashboard for viewing trading data and statistics
- **Tokens.tsx**: Token listing and management page

### Services
- **api.ts**: Centralized API client configuration using Axios, handles API base URL and request/response interceptors

### Configuration Files
- **vite.config.ts**: Vite build tool configuration
- **tsconfig.json**: TypeScript compiler configuration
- **tailwind.config.js**: Tailwind CSS utility configuration
- **package.json**: Dependencies and npm scripts

## Backend Structure

### API Endpoints (v1)

The API is organized under `/api/v1/`:

- **Health** (`/api/v1/health`): Health check endpoints
- **Stats** (`/api/v1/stats`): Statistics and summary endpoints
- **Tokens** (`/api/v1/tokens`): Token-related endpoints for fetching and managing tokens

### Core Modules

- **config.py**: Application settings loaded from environment variables using Pydantic Settings
- **database.py**: Database initialization, connection management, and session handling

### Models

- **token.py**: SQLAlchemy models for token data representation

### Services

- **scheduler.py**: Task scheduling service using APScheduler for periodic tasks
- **ta.py**: Technical analysis utilities and helper functions (RSI, MACD calculations)

### Main Application

- **main.py**: FastAPI application entry point, includes:
  - Application initialization
  - CORS middleware configuration
  - API router registration
  - Lifespan management (startup/shutdown)
  - Health check endpoints

## Environment Variables

### Backend

Create `backend/.env` file (or use environment variables):

- `DATABASE_URL`: Database connection string (default: `sqlite:///./pumpswap.db`)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated or `*` for all)
- `BIRDEYE_API_KEY`: Birdeye API key for token data
- `TOKEN_FETCH_INTERVAL_SECONDS`: Interval for token fetching (in seconds)

### Frontend

Create `frontend/.env` file:

- `VITE_API_URL`: Backend API URL (default: `http://localhost:8000`)

## Development

### Local Development (Without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Or using pyproject.toml: pip install -e ".[dev]"
cp .env.example .env  # Edit .env with your settings
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testing

#### Frontend Tests
```bash
cd frontend
npm test
```

#### Backend Tests
```bash
cd backend
pytest
```

Or using Docker:
```bash
make test-frontend
make test-backend
```

### Linting

#### Frontend
```bash
cd frontend
npm run lint
npm run lint:fix
```

#### Backend
```bash
cd backend
black .
flake8 .
mypy .
```

Or using Docker:
```bash
make lint-frontend
make lint-backend
```

## API Documentation

Once the backend is running, interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Contributing

1. Create a feature branch from `dev`
2. Make your changes
3. Run tests and linters
4. Submit a pull request

## License

[Add your license here]

