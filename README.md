# Feasibility Report Engine

A comprehensive Python-based system to generate standardized feasibility reports with financial modeling, risk analysis, PEST/SWOT analysis, multi-year projections, data persistence, file uploads, and market data integration.

## Features

✅ **Financial Modeling**
- Revenue and expense projections (5-25 years)
- NPV, IRR, ROI, and Payback Period calculations
- Scenario analysis (Best/Base/Worst case)
- Cashflow projections

✅ **Strategic Analysis**
- PEST Analysis (Political, Economic, Social, Technical)
- SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
- Risk Matrix and Risk Assessment

✅ **Market Data Integration**
- Economic indicators (GDP, inflation, unemployment) via FRED & World Bank
- Industry sector data and commodity prices via yfinance
- Company financial data and benchmarks
- Cached data for offline access

✅ **Data Management**
- SQLite database for persistent storage
- File upload support (CSV, Excel, JSON)
- Direct data entry via web interface
- Version control and audit trail for reports

✅ **Reporting & Export**
- Professional PDF reports
- Excel spreadsheets with detailed projections
- HTML interactive dashboards
- Interactive visualizations with Plotly

✅ **Web Interface**
- Clean, intuitive UI for creating projects
- Data collection and upload
- Real-time report generation
- Report history and versioning

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/muraleegithub/feasibility-report-engine.git
cd feasibility-report-engine
```

2. **Create virtual environment**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**
```bash
python
>>> from database.models import init_db
>>> init_db()
>>> exit()
```

5. **Get FRED API Key (free)**
- Visit: https://fred.stlouisfed.org/docs/api/api_key.html
- Register for a free API key
- Create `.env` file in project root:
```
FRED_API_KEY=your_api_key_here
```

6. **Run the application**
```bash
python app.py
```

The application will start at `http://localhost:5000`

## Project Structure

```
feasibility-report-engine/
├── config/                          # Configuration files
│   ├── database.py                 # Database settings
│   ├── market_data_config.py       # Market data API configs
│   └── logging_config.py           # Logging configuration
│
├── database/                        # Database layer
│   ├── models.py                   # SQLAlchemy ORM models
│   ├── db_connection.py            # Database connection
│   └── migrations/                 # Alembic migrations
│
├── src/                             # Core application logic
│   ├── inputs/                     # Data input handling
│   │   ├── file_handler.py         # File upload processing
│   │   ├── form_handler.py         # Form data handling
│   │   └── data_validator.py       # Input validation
│   ├── market_data/                # Market data integration
│   │   ├── economic_indicators.py  # FRED, World Bank data
│   │   ├── industry_data.py        # yfinance sector data
│   │   ├── company_data.py         # Company financials
│   │   ├── cache_manager.py        # Data caching
│   │   └── data_aggregator.py      # Data aggregation
│   ├── core/                       # Financial analysis
│   │   ├── financial_model.py      # Revenue/expense modeling
│   │   ├── metrics_calculator.py   # ROI, NPV, IRR calculations
│   │   ├── scenario_analyzer.py    # Scenario analysis
│   │   └── risk_analyzer.py        # Risk assessment
│   ├── strategic/                  # Strategic analysis
│   │   ├── pest_analysis.py        # PEST framework
│   │   ├── swot_analysis.py        # SWOT framework
│   │   └── strategic_templates.py  # Analysis templates
│   ├── visualization/              # Chart generation
│   │   ├── charts.py               # Plotly charts
│   │   ├── heatmaps.py             # Risk matrices
│   │   └── tables.py               # Data tables
│   ├── reporting/                  # Report generation
│   │   ├── template_engine.py      # Jinja2 templates
│   │   ├── pdf_export.py           # PDF export
│   │   └── excel_export.py         # Excel export
│   ├── utils/                      # Utilities
│   │   ├── validators.py           # Data validators
│   │   └── helpers.py              # Helper functions
│   └── engine.py                   # Main orchestrator
│
├── api/                             # Flask API routes
│   ├── app.py                      # Flask application
│   └── routes/                     # API endpoints
│       ├── projects.py             # Project endpoints
│       ├── reports.py              # Report endpoints
│       ├── uploads.py              # File upload endpoints
│       ├── market_data.py          # Market data endpoints
│       └── exports.py              # Export endpoints
│
├── templates/                       # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── create_project.html         # Project creation
│   ├── data_input.html             # Data entry form
│   ├── market_data.html            # Market data viewer
│   ├── report_view.html            # Report display
│   └── report_history.html         # Version history
│
├── static/                          # Static files
│   ├── css/
│   │   └── style.css               # Stylesheet
│   └── js/
│       └── main.js                 # JavaScript
│
├── examples/                        # Example data and scripts
│   ├── sample_project_data.json    # Sample project
│   ├── sample_data.csv             # Sample CSV
│   ├── sample_data.xlsx            # Sample Excel
│   └── generate_sample_report.py   # Script to generate sample
│
├── tests/                           # Unit tests
│   ├── test_financial_model.py
│   ├── test_file_handler.py
│   ├── test_market_data.py
│   └── test_risk_analyzer.py
│
├── output/                          # Generated reports
│   └── .gitkeep
│
├── main.py                          # Entry point
├── app.py                           # Flask app
└── requirements.txt                 # Python dependencies
```

## Usage

### Web Interface

1. **Open browser** to `http://localhost:5000`
2. **Create Project** - Enter project name and basic info
3. **Add Data** - Upload files or enter data manually
4. **Collect Market Data** - Fetch economic/industry data
5. **Generate Report** - Run analysis and generate reports
6. **Export** - Download as PDF, Excel, or HTML

### Command Line

```bash
# Generate report from CLI
python main.py --project-id 1 --generate-report

# Export to PDF
python main.py --report-id 1 --export pdf

# List all projects
python main.py --list-projects
```

## API Endpoints

### Projects
```
GET    /api/projects              - List all projects
POST   /api/projects              - Create new project
GET    /api/projects/<id>         - Get project details
PUT    /api/projects/<id>         - Update project
DELETE /api/projects/<id>         - Archive project
```

### Reports
```
GET    /api/projects/<id>/reports     - List project reports
POST   /api/projects/<id>/reports     - Generate new report
GET    /api/reports/<id>              - Get report details
PUT    /api/reports/<id>              - Update report
GET    /api/reports/<id>/versions     - Report version history
```

### Exports
```
GET    /api/reports/<id>/export/pdf   - Export as PDF
GET    /api/reports/<id>/export/excel - Export as Excel
GET    /api/reports/<id>/export/html  - Export as HTML
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src
```

## License

MIT License - See LICENSE file for details
