# Name Verification Application

A FastAPI-based system that generates target names from prompts and verifies candidate names against stored targets using deterministic string matching algorithms.

## Overview

The Name Verification Application provides two primary functions:

1. Name Generation: Creates target names from user prompts using LLM
2. Name Verification: Verifies candidate names against stored targets using multiple matching algorithms including:
   - Token similarity matching
   - Damerau-Levenshtein edit distance
   - Double Metaphone phonetic encoding
   - Nickname mapping

The system enforces strict isolation between generation and verification to ensure deterministic, testable results.

## Features

- RESTful API with FastAPI
- Deterministic name matching with configurable confidence threshold
- Multiple matching algorithms for robust verification
- Unicode normalization and text preprocessing
- Property-based testing with Hypothesis
- Comprehensive error handling

## Requirements

- Python 3.11 or higher
- OpenAI API key (for name generation)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd name-verification
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

The application requires the following environment variable:

- `OPENAI_API_KEY` (required): Your OpenAI API key for name generation

Set the environment variable:

Linux/macOS:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Windows:
```cmd
set OPENAI_API_KEY=your-api-key-here
```

Or create a .env file (recommended for development):
```bash
cp .env.example .env
# Edit .env and add your actual API key
```

## Running the Application

### Development Mode

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Production Mode

For production deployment:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /generate

Generate a target name from a prompt.

**Request:**
```json
{
  "prompt": "Generate a traditional Arabic name"
}
```

**Response:**
```json
{
  "target_name": "Ahmed Al-Rashid"
}
```

### POST /verify

Verify a candidate name against the stored target.

**Request:**
```json
{
  "candidate_name": "Ahmad Al Rashid"
}
```

**Response:**
```json
{
  "match": true,
  "confidence": 0.92,
  "reason": "High confidence match: strong token similarity (0.95), order preserved"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Property-Based Tests Only

```bash
pytest -k "property" -v
```

### Run Specific Test File

```bash
pytest tests/test_verifier.py -v
```

## Project Structure

```
app/
├── main.py                 # FastAPI application entry
├── config.py              # Configuration constants
├── security.py            # Input sanitization
├── logging_config.py      # Logging configuration
├── api/
│   ├── routes.py          # API endpoint definitions
│   ├── models.py          # Pydantic request/response models
│   └── errors.py          # Error handlers
├── generator/
│   └── service.py         # Name generation logic
├── verifier/
│   ├── service.py         # Verification orchestration
│   ├── normalizer.py      # Text normalization
│   ├── tokenizer.py       # Token splitting and merging
│   ├── matcher.py         # Matching algorithms
│   └── scorer.py          # Confidence scoring
└── store/
    └── memory.py          # In-memory name storage

tests/
├── test_generator.py
├── test_verifier.py
├── test_normalizer.py
├── test_tokenizer.py
├── test_matcher.py
├── test_scorer.py
└── test_api.py
```

## Architecture

The system consists of three primary components with strict isolation:

1. Name Generator: Creates target names using LLM (write-only to store)
2. Name Store: Maintains the current target name in memory
3. Name Verifier: Performs deterministic matching (read-only from store)

This isolation ensures:
- Deterministic verification results
- No context leakage between components
- Testable and predictable behavior

## Verification Algorithm

The verification process follows these steps:

1. Normalization: Convert to lowercase, apply Unicode NFC, remove punctuation, collapse whitespace, standardize prefixes
2. Tokenization: Split on whitespace, merge compound patterns (abdul, al, ibn, bin)
3. Matching: Compute token similarity, edit distance, phonetic encoding, nickname matches
4. Scoring: Weighted confidence score (token: 40%, nickname: 35%, phonetic: 15%, edit: 10%)
5. Decision: Match if confidence is 0.80 or higher AND token order preserved

## Configuration

Default configuration values are defined in `app/config.py`:

- Confidence threshold: 0.80
- Token similarity weight: 0.40
- Nickname weight: 0.35
- Phonetic weight: 0.15
- Edit distance weight: 0.10

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Client error (e.g., no target name in store)
- `422`: Validation error (e.g., empty input)
- `500`: Server error (e.g., generation failure)

All error responses include a human-readable message.

## Performance

- Verification: < 50ms (p95)
- Health check: < 10ms
- Generation: < 5s (depends on LLM API)

## Security

- Input sanitization to prevent injection attacks
- No code execution from user input
- Strict component isolation
- No external network calls during verification

## Development

### Adding New Nickname Mappings

Edit `app/config.py` and add entries to the `NICKNAME_MAP` dictionary:

```python
NICKNAME_MAP = {
    "elizabeth": ["liz", "beth", "betty"],
    "william": ["will", "bill"],
    # Add more mappings here
}
```

### Adjusting Confidence Threshold

Modify the `CONFIDENCE_THRESHOLD` constant in `app/config.py`:

```python
CONFIDENCE_THRESHOLD = 0.80  # Adjust as needed
```

## Troubleshooting

### "OpenAI API key required" Error

Ensure the `OPENAI_API_KEY` environment variable is set correctly.

### Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Tests Failing

Run tests with verbose output to see detailed error messages:
```bash
pytest -v
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support contact information here]
