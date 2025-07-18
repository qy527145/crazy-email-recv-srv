"""
Tests for configuration management.
"""

import os
import tempfile
import pytest
from pathlib import Path

from aemail.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()

        # After auto-detection, smtp_host should be a valid IP address
        assert config.smtp_host in ['::', '0.0.0.0', '127.0.0.1']
        assert config.smtp_port == 25
        assert config.rest_host == config.smtp_host  # rest_host returns smtp_host
        assert config.rest_port == 14000
    
    def test_config_from_file(self):
        """Test loading configuration from file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            f.write("""
[smtpd]
host = 192.168.1.100
port = 2525

[rest]
port = 8080
""")
            config_file = f.name
        
        try:
            config = Config(config_file)
            
            assert config.smtp_host == '192.168.1.100'
            assert config.smtp_port == 2525
            assert config.rest_host == '192.168.1.100'
            assert config.rest_port == 8080
        finally:
            os.unlink(config_file)
    
    def test_config_from_env(self):
        """Test loading configuration from environment variables."""
        # Set environment variables
        os.environ['SMTP_HOST'] = '10.0.0.1'
        os.environ['SMTP_PORT'] = '587'
        os.environ['REST_PORT'] = '9000'
        
        try:
            config = Config()
            
            assert config.smtp_host == '10.0.0.1'
            assert config.smtp_port == 587
            assert config.rest_host == '10.0.0.1'
            assert config.rest_port == 9000
        finally:
            # Clean up environment variables
            for key in ['SMTP_HOST', 'SMTP_PORT', 'REST_PORT']:
                if key in os.environ:
                    del os.environ[key]
    
    def test_config_save(self):
        """Test saving configuration to file."""
        config = Config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            config_file = f.name
        
        try:
            config.save(config_file)
            
            # Verify file was created and contains expected content
            assert Path(config_file).exists()
            
            # Load the saved config
            new_config = Config(config_file)
            assert new_config.smtp_host == config.smtp_host
            assert new_config.smtp_port == config.smtp_port
            assert new_config.rest_port == config.rest_port
        finally:
            if Path(config_file).exists():
                os.unlink(config_file)
