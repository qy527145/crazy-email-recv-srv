# AEmail - Simple Email Receive Server

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-dependency%20management-blue.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simple SMTP server for receiving emails with REST API access. Perfect for testing, development, and automation scenarios where you need to receive emails programmatically.

## Features

- 🚀 **Simple SMTP Server**: Receives emails on any address with your domain
- 🌐 **REST API**: Easy access to received emails via HTTP endpoints
- 💾 **Flexible Storage**: In-memory or SQLite database storage
- 🔧 **Easy Configuration**: Environment variables and config file support
- 📦 **Poetry Package**: Professional Python packaging with wheel support
- 🖥️ **Command Line Tool**: Simple CLI for starting the server
- 🎨 **Web Interface**: Modern web UI for browsing emails
- 🔍 **Search Functionality**: Find emails by sender or recipient

## Use Cases

- **Batch Registration**: Register multiple accounts and receive verification emails
- **Email Testing**: Test email functionality in development environments
- **Automation**: Programmatically access received emails for processing
- **Development**: Mock email server for local development

## Quick Start

### Installation

```bash
# Install with pip
pip install crazy-email-recv-srv

# Or install with Poetry
poetry add crazy-email-recv-srv
```

### Basic Usage

```bash
# Start the server with default settings
crazy-email-server

# Start with custom ports
crazy-email-server --smtp-port 2525 --rest-port 8080

# Start with persistent database
crazy-email-server --db-file emails.db

# Start with custom config
crazy-email-server --config my-config.ini
```

## DNS Configuration

To receive emails for your domain, configure DNS records:

### A Record
Point your mail subdomain to your server IP:
```
A    mx    YOUR.SERVER.IP.ADDRESS
```

### MX Record
Configure MX record to route emails to your server:
```
MX   *    mx.yourdomain.com
```

> The `*` wildcard means ALL subdomains will be routed to your server.
> Examples: `test@yourdomain.com`, `anything@sub.yourdomain.com`
> This gives you unlimited email addresses!

## API Endpoints

The server provides a REST API for accessing received emails:

### GET /all
Get all stored messages (last 100)
```bash
curl http://localhost:14000/all
```

### GET /from/{email}
Get messages from a specific sender
```bash
curl http://localhost:14000/from/sender@example.com
```

### GET /to/{email}
Get messages to a specific recipient
```bash
curl http://localhost:14000/to/recipient@example.com
```

### GET /health
Health check endpoint
```bash
curl http://localhost:14000/health
```

### Response Format
```json
[
  {
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "to0": "recipient@example.com",
    "subject": "Test Email",
    "content": "Email content here...",
    "time": "2024-01-01T12:00:00"
  }
]
```

## Configuration

### Config File (cfg.ini)
```ini
[smtpd]
host = 127.0.0.1
port = 25

[rest]
port = 14000
```

### Environment Variables
Override config file settings with environment variables:
- `SMTP_HOST` - SMTP server host
- `SMTP_PORT` - SMTP server port
- `REST_PORT` - REST API port

### Command Line Options
```bash
crazy-email-server --help

Options:
  --config, -c          Path to configuration file
  --smtp-host          SMTP server host
  --smtp-port          SMTP server port
  --rest-port          REST API port
  --db-file            SQLite database file path
  --verbose, -v        Enable verbose logging
  --version            Show version
```

## Development

### From Source
```bash
# Clone the repository
git clone https://github.com/lycying/crazy-email-recv-srv.git
cd crazy-email-recv-srv

# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run the server
poetry run crazy-email-server

# Run tests
poetry run pytest

# Build wheel package
poetry build
```

### Project Structure
```
crazy-email-recv-srv/
├── crazy_email_recv_srv/     # Main package
│   ├── __init__.py
│   ├── cli.py               # Command line interface
│   ├── config.py            # Configuration management
│   ├── data.py              # Data access layer
│   ├── email_handler.py     # SMTP email processing
│   ├── server.py            # Main server
│   ├── utils.py             # Utility functions
│   └── web_api.py           # REST API
├── tests/                   # Test suite
├── static/                  # Web interface files
├── pyproject.toml          # Poetry configuration
└── README.md
```

## Testing

Send a test email to any address at your domain:
```bash
# Example: Send email to test@yourdomain.com
# Then query the API:
curl http://localhost:14000/to/test@yourdomain.com
```

Or use the web interface at: http://localhost:14000

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/lycying/crazy-email-recv-srv/issues)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/lycying/crazy-email-recv-srv/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/lycying/crazy-email-recv-srv/discussions)

---

**Note**: This tool is for testing and development purposes. Use responsibly and in compliance with applicable laws and regulations.
