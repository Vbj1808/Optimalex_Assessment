# Optimalex_Assessment

# Prompt Matching API

A Flask API that matches system prompts based on situation, level, and file type.

## Setup

```bash
# Create virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create logs directory
mkdir -p logs
```

## Run

```bash
python app.py
```

API runs at: `http://localhost:5000`

## Test

### Run Tests
```bash
pytest tests/test_api.py -v
```

### Test API Manually

**Test Prompt 1:**
```bash
curl -X POST http://localhost:5000/api/match-prompt \
  -H "Content-Type: application/json" \
  -d '{"situation": "Commercial Auto", "level": "Structure", "file_type": "Summary Report", "data": ""}'
```

**Test Prompt 2:**
```bash
curl -X POST http://localhost:5000/api/match-prompt \
  -H "Content-Type: application/json" \
  -d '{"situation": "General Liability", "level": "Summarize", "file_type": "Deposition", "data": ""}'
```

**Test Prompt 3:**
```bash
curl -X POST http://localhost:5000/api/match-prompt \
  -H "Content-Type: application/json" \
  -d '{"situation": "Commercial Auto", "level": "Summarize", "file_type": "Summons", "data": ""}'
```

**Test Prompt 4:**
```bash
curl -X POST http://localhost:5000/api/match-prompt \
  -H "Content-Type: application/json" \
  -d '{"situation": "Workers Compensation", "level": "Structure", "file_type": "Medical Records", "data": ""}'
```

**Test Prompt 5:**
```bash
curl -X POST http://localhost:5000/api/match-prompt \
  -H "Content-Type: application/json" \
  -d '{"situation": "Workers Compensation", "level": "Summarize", "file_type": "Summons", "data": ""}'
```