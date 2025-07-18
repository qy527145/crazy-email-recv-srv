"""
Tests for data access layer.
"""

import pytest
import tempfile
from pathlib import Path

from aemail.data import EmailData


class TestEmailData:
    """Test email data access layer."""
    
    def test_in_memory_database(self):
        """Test in-memory database initialization."""
        data = EmailData()
        
        # Should be able to store and retrieve messages
        message = {
            'from': 'test@example.com',
            'to': ['recipient@example.com'],
            'subject': 'Test Subject',
            'content': 'Test content'
        }
        
        data.store_message(message)
        messages = data.get_all_messages()
        
        assert len(messages) == 1
        assert messages[0]['from'] == 'test@example.com'
        assert messages[0]['subject'] == 'Test Subject'
        
        data.close()
    
    def test_file_database(self):
        """Test file-based database."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / 'test.db'
            
            data = EmailData(str(db_path))
            
            message = {
                'from': 'sender@example.com',
                'to': ['receiver@example.com'],
                'subject': 'File DB Test',
                'content': 'Testing file database'
            }
            
            data.store_message(message)
            data.close()
            
            # Verify database file was created
            assert db_path.exists()
            
            # Reopen database and verify data persists
            data2 = EmailData(str(db_path))
            messages = data2.get_all_messages()
            
            assert len(messages) == 1
            assert messages[0]['from'] == 'sender@example.com'
            
            data2.close()
    
    def test_message_queries(self):
        """Test different message query methods."""
        data = EmailData()
        
        # Store multiple messages
        messages = [
            {
                'from': 'alice@example.com',
                'to': ['bob@example.com'],
                'subject': 'Hello Bob',
                'content': 'Hi there!'
            },
            {
                'from': 'charlie@example.com',
                'to': ['bob@example.com'],
                'subject': 'Another message',
                'content': 'More content'
            },
            {
                'from': 'alice@example.com',
                'to': ['dave@example.com'],
                'subject': 'Hello Dave',
                'content': 'Different recipient'
            }
        ]
        
        for msg in messages:
            data.store_message(msg)
        
        # Test get_all_messages with pagination
        all_msgs = data.get_all_messages(limit=2)
        assert len(all_msgs) == 2

        all_msgs_page2 = data.get_all_messages(limit=2, offset=2)
        assert len(all_msgs_page2) == 1

        # Test get_messages_from with pagination
        alice_msgs = data.get_messages_from('alice@example.com')
        assert len(alice_msgs) == 2
        assert all(msg['from'] == 'alice@example.com' for msg in alice_msgs)

        # Test get_messages_to with pagination
        bob_msgs = data.get_messages_to('bob@example.com')
        assert len(bob_msgs) == 2
        assert all('bob@example.com' in msg['to'] for msg in bob_msgs)

        # Test message count
        assert data.get_message_count() == 3
        assert data.get_message_count(sender='alice@example.com') == 2
        assert data.get_message_count(recipient='bob@example.com') == 2
        
        data.close()
    
    def test_empty_queries(self):
        """Test queries with no results."""
        data = EmailData()
        
        # Test empty database
        assert data.get_all_messages() == []
        assert data.get_messages_from('nonexistent@example.com') == []
        assert data.get_messages_to('nonexistent@example.com') == []
        
        data.close()
    
    def test_message_limit(self):
        """Test message limit functionality."""
        data = EmailData()
        
        # Store more than default limit
        for i in range(150):
            message = {
                'from': f'sender{i}@example.com',
                'to': ['recipient@example.com'],
                'subject': f'Message {i}',
                'content': f'Content {i}'
            }
            data.store_message(message)
        
        # Should return only 20 messages (new default limit)
        all_msgs = data.get_all_messages()
        assert len(all_msgs) == 20
        
        # Test custom limit
        limited_msgs = data.get_all_messages(limit=50)
        assert len(limited_msgs) == 50
        
        data.close()
