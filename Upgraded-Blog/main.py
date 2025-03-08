import os
from email.mime.text import MIMEText
from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
import dotenv
from flask.cli import load_dotenv

load_dotenv()

app = Flask(__name__)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = 587  # Standard TLS port
SENDER_EMAIL = os.getenv('SMTP_EMAIL')  # Your email address
SENDER_PASSWORD = os.getenv('SMTP_PASSWORD')
RECIPIENT_EMAIL = "sneeze@demented.cc"  # Where you want to receive the messages


def get_all_posts():
    response = requests.get("https://api.npoint.io/93fc9a8f6a1cb9510fb3")
    return response.json()


def get_post(post_id):
    all_posts = get_all_posts()
    return next((post for post in all_posts if post["id"] == post_id), None)

def send_email(name, email, phone, message):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f"New Contact Form Submission from {name}"

    # Create the email body
    body = f"""
    You have received a new contact form submission:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Message:
    {message}
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create SMTP session
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            # Send email
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route('/')
@app.route('/index.html')
def index():
    all_posts = get_all_posts()
    return render_template('index.html', posts=all_posts)


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def show_post(post_id):
    requested_post = get_post(post_id)
    return render_template('post.html', post=requested_post)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Print the information for logging
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Message: {message}")

        # Try to send the email
        if send_email(name, email, phone, message):
            return "<h1>Successfully sent your message</h1>"
        else:
            return "<h1>There was an error sending your message. Please try again later.</h1>"

    return render_template('contact.html')




if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
