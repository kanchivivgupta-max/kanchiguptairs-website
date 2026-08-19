import os
import requests
import smtplib
from email.message import EmailMessage

def publish_to_medium(title, markdown_content, tags=None, publish_status="public"):
    """
    Publishes an article to Medium via their official REST API.
    Requires environment variables: MEDIUM_TOKEN, MEDIUM_USER_ID
    """
    token = os.environ.get("MEDIUM_TOKEN")
    user_id = os.environ.get("MEDIUM_USER_ID")
    
    if not token or not user_id:
        print("[!] Medium credentials (MEDIUM_TOKEN, MEDIUM_USER_ID) not found in environment.")
        return None
        
    url = f"https://api.medium.com/v1/users/{user_id}/posts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": markdown_content,
        "publishStatus": publish_status
    }
    
    if tags:
        payload["tags"] = tags
        
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        data = response.json().get("data", {})
        print(f"[+] Successfully published to Medium! URL: {data.get('url')}")
        return data.get("url")
    else:
        print(f"[!] Failed to publish to Medium: {response.status_code} - {response.text}")
        return None

def publish_to_substack_via_email(subject, markdown_content, recipient_email):
    """
    Publishes an article to Substack by sending an email to your Substack's unique inbound address.
    Requires environment variables: SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
    """
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        print("[!] Sender email credentials (SENDER_EMAIL, SENDER_PASSWORD) not found in environment.")
        return False
        
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # Set the body as plain text/markdown (Substack email-to-post parser handles text nicely)
    msg.set_content(markdown_content)
    
    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                
        print(f"[+] Successfully dispatched article to Substack via email: {recipient_email}")
        return True
    except Exception as e:
        print(f"[!] Failed to send Substack email: {e}")
        return False

def publish_to_linkedin(text_content, article_url=None):
    """
    Publishes a post or share to LinkedIn via their official REST API (UGC Posts / Shares).
    Requires environment variables: LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN (e.g. urn:li:person:abcdef)
    """
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.environ.get("LINKEDIN_PERSON_URN")
    
    if not access_token or not person_urn:
        print("[!] LinkedIn credentials (LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN) not found in environment.")
        return None
        
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    # Construct share content payload
    share_content = {
        "shareCommentary": {
            "text": text_content
        },
        "shareMediaCategory": "NONE"
    }
    
    if article_url:
        share_content["shareMediaCategory"] = "ARTICLE"
        share_content["media"] = [{
            "status": "READY",
            "originalUrl": article_url,
            "title": {"text": "Professional Update — Kanchi Gupta"}
        }]

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": share_content
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        print("[+] Successfully published post to LinkedIn!")
        return response.json()
    else:
        print(f"[!] Failed to publish to LinkedIn: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    # Example usage / automated dispatch check using markdown template
    template_path = os.path.join(os.path.dirname(__file__), "notes", "article_template_kanchi_gupta.md")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        title = "Kanchi Gupta — Public Revenue, Tax Administration, and Digital Workflows"
        
        print("[*] Testing automated syndication payload...")
        # 1. Try Medium if configured
        if os.environ.get("MEDIUM_TOKEN") and os.environ.get("MEDIUM_USER_ID"):
            publish_to_medium(title, content, tags=["Kanchi Gupta", "Tax Policy", "Public Administration"])
            
        # 2. Try Substack if configured
        if os.environ.get("SENDER_EMAIL") and os.environ.get("SUBSTACK_EMAIL"):
            publish_to_substack_via_email(title, content, os.environ.get("SUBSTACK_EMAIL"))
            
        # 3. Try LinkedIn if configured
        if os.environ.get("LINKEDIN_ACCESS_TOKEN") and os.environ.get("LINKEDIN_PERSON_URN"):
            linkedin_text = f"Exploring public revenue administration, indirect taxation, and digital workflows as Joint Commissioner, Chennai CGST Audit. Read more at https://kanchiguptairs.com"
            publish_to_linkedin(linkedin_text, article_url="https://kanchiguptairs.com")
    else:
        print("Defensive Cross-Platform Publishing Script Loaded Successfully.")
