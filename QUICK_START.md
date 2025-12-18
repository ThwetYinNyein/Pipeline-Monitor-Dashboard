# Terminus Pipeline - Quick Start Guide

### Step 1: Setup Environment
```bash
# Navigate to project
cd "D:\your_local_directory\terminus"

# Create .env file from template
copy env.example .env

# Edit .env with your credentials
notepad .env
```

### Step 2: Test Installation
```bash
python test_pipeline.py
```

Expected output: `[SUCCESS] ALL TESTS PASSED`

### Step 3: Run Your First Pipeline
```bash
# Example: Run CocoTran pipeline
python pipelines\ayapay\CocoTran.py

# Check the log
dir log\CocoTran
```

## 📁 Project Structure

```
terminus/
├── pipelines/
│   ├── ayapay/          # Ayapay pipelines
│   ├── mbx/             # Mobile banking pipelines
│   └── milestone/       # Milestone pipelines
├── log/                 # Auto-generated logs
├── bootstrap.py         # Pipeline initialization
├── logging_setup.py     # Logging configuration
├── .env                 # Your credentials
└── test_pipeline.py     # Test script
```

### Dashboard
```bash
streamlit run app.py
```

**Version**: 1.0.0

