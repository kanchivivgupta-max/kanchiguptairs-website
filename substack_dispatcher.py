import os
import smtplib
from email.message import EmailMessage

def send_to_substack_email(subject, markdown_content, substack_inbound_email, sender_email, sender_password):
    """
    Sends an email to your Substack custom inbound email address to auto-publish a post.
    """
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = substack_inbound_email
    msg.set_content(markdown_content)
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"[+] Successfully dispatched post to Substack via email: {substack_inbound_email}")
        return True
    except Exception as e:
        print(f"[!] Substack email dispatch failed: {e}")
        return False

if __name__ == "__main__":
    # Test Substack email dispatch with your exact inbound address
    print("[*] Testing Substack Email-to-Post dispatcher...")
    subject = "Kanchi Gupta — Professional Overview and Public Revenue Frameworks"
    with open("/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/notes/article_template_kanchi_gupta.md", "r", encoding="utf-8") as f:
        content = f.read()
        
    sender = os.environ.get("SENDER_EMAIL", "kanchivivgupta@gmail.com")
    password = os.environ.get("SENDER_PASSWORD", "")
    
    if password:
        send_to_substack_email(subject, content, "kanchivivgupta@substack.com", sender, password)
    else:
        print("[!] SENDER_PASSWORD environment variable not set. Add it to test live publishing.")
