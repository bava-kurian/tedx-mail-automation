import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "bavakurianvarghese2026@cs.ajce.in"
SENDER_PASSWORD = "iimt zfbj okad adjm"   # Replace with Gmail App Password
IMAGE_FOLDER = "image_forder"  # Updated image folder path

def create_email_template(recipient_email):
    subject = "Welcome to TEDxAJCE 2025!"
    
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="text-align: center;">
        <img src="cid:logo" style="max-width: 200px; margin-bottom: 20px;">
    </div>
    
    <p>Dear Valued Attendee,</p>

    <p>We're thrilled to confirm your registration for TEDxAJCE 2025! We have curated a remarkable lineup of speakers who will challenge your thinking and spark your imagination. Your ticket is attached to this email.</p>

    <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0;">
        <h3 style="color: #e62b1e; margin-top: 0;">Event Details</h3>
        <p>Date: 12th March 2025<br>
        Theme: ASCENT - Every Step Leaves a Mark<br>
        Time: 9:15am - 3:30pm<br>
        Venue: RB Auditorium, Amal Jyothi College of Engineering, Kanjirappally</p>
    </div>

    <div style="margin: 20px 0;">
        <h3 style="color: #e62b1e;">Highlights</h3>
        <ul>
            <li>Inspiring talks from innovative speakers</li>
            <li>Networking opportunities</li>
            <li>Complimentary refreshments</li>
        </ul>
    </div>

    <div style="background-color: #fff3f3; padding: 15px; margin: 20px 0;">
        <h3 style="color: #e62b1e; margin-top: 0;">Important Information</h3>
        <ul>
            <li>Please arrive at the venue by 8:30am</li>
            <li>Visit the help desk at the entrance for check-in and assistance</li>
            <li>Make sure to have an electronic copy of your ticket ready for scanning at entry</li>
        </ul>
    </div>

    <p>The TEDx experience is about engaging with new ideas and connecting with others. We look forward to seeing you at this gathering of minds!</p>

    <p>Here's our event schedule:</p>
    <img src="cid:schedule" width="600" style="margin: 20px 0;">

    <p>Warm regards,<br>
    TEDxAJCE Team</p>

    <p style="font-style: italic;">P.S. Don't forget to review the attached schedule and ticket!</p>
    </body>
    </html>
    """
    
    return subject, html_body

def send_email(recipient_email, image_path):
    msg = MIMEMultipart('related')
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    
    subject, html_body = create_email_template(recipient_email)
    msg['Subject'] = subject
    
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    
    # Attach HTML content
    html_part = MIMEText(html_body, 'html')
    msg_alternative.attach(html_part)
    
    # Attach logo image inline
    with open('logo.png', 'rb') as f:
        logo_img = MIMEImage(f.read())
        logo_img.add_header('Content-ID', '<logo>')
        msg.attach(logo_img)
    
    # Attach schedule image inline
    with open('schedule.jpg', 'rb') as f:
        schedule_img = MIMEImage(f.read())
        schedule_img.add_header('Content-ID', '<schedule>')
        msg.attach(schedule_img)
    
    # Attach personalized invitation
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data)
    image.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
    msg.attach(image)
    
    # Send email with better error handling
    try:
        print(f"Attempting to connect to {SMTP_SERVER}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)  # Enable debug output
        print("Starting TLS...")
        server.starttls()
        print("Attempting login...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except smtplib.SMTPAuthenticationError as e:
        print("Authentication failed! Please check:")
        print("1. Enable 'Less secure app access' in your Google Account")
        print("2. Generate and use App Password if 2FA is enabled")
        print(f"Error details: {str(e)}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {str(e)}")

def main():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: Image folder '{IMAGE_FOLDER}' not found")
        return
    
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            recipient_email = os.path.splitext(filename)[0]
            image_path = os.path.join(IMAGE_FOLDER, filename)
            send_email(recipient_email, image_path)

if __name__ == "__main__":
    main()
