# Usage Guide

## Quick Start

### 1. Install the Package

```bash
# Install from wheel (after building)
pip install dist/crazy_email_recv_srv-0.1.0-py3-none-any.whl

# Or install in development mode
poetry install
```

### 2. Start the Server

```bash
# Using Poetry (development)
poetry run crazy-email-server

# Using installed package
crazy-email-server

# With custom settings
crazy-email-server --smtp-port 2525 --rest-port 8080 --verbose
```

### 3. Configure DNS (for production)

Add these DNS records to your domain:

```
A    mx    YOUR.SERVER.IP
MX   *     mx.yourdomain.com
```

### 4. Test the Server

```bash
# Check health
curl http://localhost:14000/health

# View web interface
open http://localhost:14000

# Get all emails
curl http://localhost:14000/all

# Get emails to specific address
curl http://localhost:14000/to/test@yourdomain.com
```

## Configuration Options

### Command Line Arguments

- `--config, -c`: Configuration file path
- `--smtp-host`: SMTP server host
- `--smtp-port`: SMTP server port (default: 25)
- `--rest-port`: REST API port (default: 14000)
- `--db-file`: SQLite database file (default: in-memory)
- `--verbose, -v`: Enable debug logging

### Environment Variables

- `SMTP_HOST`: Override SMTP host
- `SMTP_PORT`: Override SMTP port
- `REST_PORT`: Override REST API port

### Configuration File (cfg.ini)

```ini
[smtpd]
host = 127.0.0.1
port = 25

[rest]
port = 14000
```

## API Endpoints

### GET /health
Health check endpoint
```json
{"status": "healthy", "service": "crazy-email-recv-srv"}
```

### GET /all
Get all emails (last 100)
```json
[
  {
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "to0": "recipient@example.com",
    "subject": "Test Email",
    "content": "Email content...",
    "time": "2024-01-01T12:00:00"
  }
]
```

### GET /from/{email}
Get emails from specific sender

### GET /to/{email}
Get emails to specific recipient

## Development

### Running Tests

```bash
# Run all new tests
poetry run pytest tests/test_config.py tests/test_data.py -v

# Run with coverage
poetry run pytest --cov=crazy_email_recv_srv
```

### Building

```bash
# Build wheel and source distribution
poetry build

# Check build artifacts
ls dist/
```

### Code Quality

```bash
# Format code
poetry run black crazy_email_recv_srv/

# Sort imports
poetry run isort crazy_email_recv_srv/

# Type checking
poetry run mypy crazy_email_recv_srv/

# Linting
poetry run flake8 crazy_email_recv_srv/
```

## Use Cases

### 1. Batch Account Registration
```python
import requests
import time

# Register accounts
for i in range(100):
    email = f"user{i}@yourdomain.com"
    # Register account with this email
    register_account(email)
    
    # Wait a bit then check for verification email
    time.sleep(5)
    response = requests.get(f"http://localhost:14000/to/{email}")
    emails = response.json()
    
    if emails:
        # Process verification email
        verification_link = extract_link(emails[0]['content'])
        verify_account(verification_link)
```

### 2. Email Testing in CI/CD
```bash
# Start server in background
crazy-email-server --smtp-port 2525 --rest-port 8080 &

# Run your tests that send emails
python test_email_functionality.py

# Check received emails
curl http://localhost:8080/all
```

### 3. Development Mock Server
```python
from crazy_email_recv_srv import EmailServer, Config

# Create custom config
config = Config()
config.config.set('smtpd', 'port', '2525')
config.config.set('rest', 'port', '8080')

# Start server programmatically
with EmailServer(config=config) as server:
    server.start()
```

## Security Notes

- This is a development/testing tool
- Do not use in production without proper security measures
- The server accepts all emails without authentication
- Use appropriate firewall rules to restrict access
- Consider using non-standard ports for security
