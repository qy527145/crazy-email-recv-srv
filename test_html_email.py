#!/usr/bin/env python3
"""
Test script to send HTML email and verify HTML rendering functionality.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import urllib.request
import json

def send_test_html_email():
    """Send a test HTML email to the local SMTP server."""
    
    # HTML content for testing
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test HTML Email</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .header { background-color: #4CAF50; color: white; padding: 20px; }
            .content { padding: 20px; }
            .highlight { background-color: yellow; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 HTML Email Test</h1>
        </div>
        <div class="content">
            <h2>Features to Test:</h2>
            <ul>
                <li><strong>Bold text</strong></li>
                <li><em>Italic text</em></li>
                <li><span class="highlight">Highlighted text</span></li>
                <li><a href="https://example.com">Links</a></li>
            </ul>
            
            <h3>Sample Table:</h3>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td>John Doe</td>
                    <td>john@example.com</td>
                    <td>Active</td>
                </tr>
                <tr>
                    <td>Jane Smith</td>
                    <td>jane@example.com</td>
                    <td>Pending</td>
                </tr>
            </table>
            
            <p>This email contains <code>HTML formatting</code> that should be rendered properly in the web interface.</p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = """
    HTML Email Test
    
    Features to Test:
    - Bold text
    - Italic text
    - Highlighted text
    - Links
    
    Sample Table:
    Name        Email               Status
    John Doe    john@example.com    Active
    Jane Smith  jane@example.com    Pending
    
    This email contains HTML formatting that should be rendered properly in the web interface.
    """
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "HTML Email Rendering Test"
    msg['From'] = "test@example.com"
    msg['To'] = "recipient@localhost"
    
    # Add both plain text and HTML parts
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    # Send email
    try:
        server = smtplib.SMTP('localhost', 25)
        server.send_message(msg)
        server.quit()
        print("✅ HTML test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def check_email_received():
    """Check if the email was received and can be retrieved via API."""
    try:
        # Wait a moment for email to be processed
        time.sleep(2)

        # Check via API
        with urllib.request.urlopen('http://localhost:14000/to/recipient@localhost') as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                if 'messages' in data:
                    messages = data['messages']
                else:
                    messages = data  # Fallback for old API format

                if messages:
                    print(f"✅ Found {len(messages)} message(s)")
                    latest_msg = messages[0]
                    print(f"📧 Subject: {latest_msg.get('subject', 'No subject')}")

                    content = latest_msg.get('content', '')
                    if '<!-- HTML_CONTENT -->' in content or '<html>' in content.lower():
                        print("✅ HTML content detected in email!")
                        return True
                    else:
                        print("⚠️  No HTML content marker found")
                        return False
                else:
                    print("❌ No messages found")
                    return False
            else:
                print(f"❌ API request failed: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Failed to check email: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing HTML Email Rendering...")
    print("=" * 50)
    
    print("1. Sending HTML test email...")
    if send_test_html_email():
        print("\n2. Checking if email was received...")
        if check_email_received():
            print("\n✅ HTML email test completed successfully!")
            print("\n📝 Next steps:")
            print("   1. Open http://localhost:14000 in your browser")
            print("   2. Go to 'Search Emails' tab")
            print("   3. Search for emails to 'recipient@localhost'")
            print("   4. Look for the 'HTML Email Rendering Test' message")
            print("   5. Click the 'HTML' button to see rendered HTML content")
        else:
            print("\n❌ Email was not received properly")
    else:
        print("\n❌ Failed to send test email")
        print("\n💡 Make sure the email server is running:")
        print("   poetry run aemail-server")
