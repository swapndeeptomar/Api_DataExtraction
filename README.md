# Github API ETL Pipeline 🚀

A modular, resilient Python ETL pipeline that extracts repository data from the GitHub REST API, transforms it into a structured format, and loads it into both **CSV** files and a **MySQL** database.

## 📌 Features
- **Resilient Extraction**: Implements `requests.Session` with **Exponential Backoff** retries to handle network flickers and 5xx errors.
- **Dynamic Pagination**: Traverses GitHub's `Link` headers to fetch multiple pages of data dynamically.
- **Data Transformation**: Flattens nested JSON, standardizes ISO dates, and enforces a strict schema.
- **Dual-Load Strategy**: Supports concurrent loading to local CSV files (Data Lake) and MySQL (Data Warehouse).
- **Idempotency**: Uses MySQL `UPSERT` logic (`ON DUPLICATE KEY UPDATE`) to prevent duplicate records.
- **Production Hardening**: 
  - **Logging**: Simultaneous console and UTF-8 file logging.
  - **Checkpointing**: State-management allows the script to resume from the last failed page.
  - **Security**: Environment variable management for API tokens and DB credentials.

## 📁 Project Structure
```text
api_etl/
│── src/
│   ├── client.py          # API connection & Retry logic
│   ├── processor.py       # Data cleaning & Flattening
│   ├── writer.py          # CSV File I/O
│   ├── database.py        # MySQL connection & Upsert logic
│   ├── logger_config.py   # Professional logging setup
│   └── main.py            # Orchestration & Pagination loop
│── data/                  # CSV outputs & Checkpoint files
│── logs/                  # Execution history (etl_process.log)
│── .env                   # Secret credentials (Gitignored)
│── requirements.txt       # Project dependencies
└── README.md              # Documentation

🛠️ Setup & Installation1. Clone the Repository git clone [https://github.com/swapndeeptomar/api_etl.git](https://github.com/swapndeeptomar/api_etl.git)
cd api_etl

2. Configure EnvironmentCreate a .env file in the root directory:Code snippet# GitHub Configuration
GITHUB_TOKEN=your_personal_access_token_here

# MySQL Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=github_etl

# App Settings
LOG_LEVEL=INFO

3. Install Dependencies
python -m venv .venv
source .venv/bin/activate 
# On Windows: .venv\Scripts\activate
pip install -r requirements.txt

🚀 UsageTo run the full pipeline:
python src/main.py

```text 

📊 Data Schema (MySQL)The pipeline automatically creates a repositories table with the following structure:ColumnTypeDescriptionrepo_idINT (PK)Unique GitHub Repository IDnameVARCHARName of the repoowner_loginVARCHARUsername of the ownerstarsINTNumber of stargazerscreated_atDATETIMENormalized creation timestampextracted_atTIMESTAMPAuto-generated timestamp of extraction

🛡️ Error HandlingRate Limits: The script detects GitHub's 403 Forbidden and logs the reset time.Unicode Errors: Logging is configured with utf-8 to handle emojis and special characters common in repo descriptions.Database Crashes: Implements rollback() on batch failure to ensure data integrity.

📝 LicenseDistributed under the MIT License. See LICENSE for more information.