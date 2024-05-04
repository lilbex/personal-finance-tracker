import time
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

load_dotenv()

aws_access_key_id = os.environ.get('SES_AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('SES_AWS_SECRET_ACCESS_KEY')

style = """
<style>
    button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
    }
    p {
        font-size: 16px;
        color: #000000;
        margin-bottom: 10px;
    }
    a {
        color: #0000FF;
    }
"""


class AWSEmailTemplateManager:
    def __init__(self):
        self.client = boto3.client('ses',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   #    aws_session_token=aws_session_token,
                                   region_name='us-east-1')

    def receive_email_from_client(self, subject, body, sender_email):
        send = self.client

    def create_template(self, template_name, subject_part, html_body, text_body):
        response = self.client.create_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': subject_part,
                'HtmlPart': html_body,
                'TextPart': text_body
            }
        )
        return response

    def update_template(self, template_name, subject_part=None, html_body=None, text_body=None):
        template = {
            'TemplateName': template_name
        }
        if subject_part:
            template['SubjectPart'] = subject_part
        if html_body:
            template['HtmlPart'] = html_body
        if text_body:
            template['TextPart'] = text_body

        response = self.client.update_template(
            Template=template
        )
        return response['Template']

    def verify_email(self, email_address):
        response = self.client.verify_email_identity(
            EmailAddress=email_address
        )
        return response

    def verify_email(self, email_address):
        try:
            # Initiate email verification
            self.client.verify_email_identity(EmailAddress=email_address)

            # Wait for a few seconds to allow time for the verification email to be sent
            time.sleep(5)

            # Check verification status
            response = self.client.get_identity_verification_attributes(Identities=[
                                                                        email_address])
            verification_status = response['VerificationAttributes'][email_address]['VerificationStatus']

            if verification_status == 'Success':
                print(f"Successfully verified email address: {email_address}")
                return True
            else:
                print(
                    f"Failed to verify email address: {email_address}. Status: {verification_status}")
                return False
        except Exception as e:
            print(f"Error verifying email {email_address}: {e}")
            return False

    def delete_template(self, template_name):
        response = self.client.delete_template(
            TemplateName=template_name
        )
        return response

    def get_template(self, template_name):
        response = self.client.get_template(
            TemplateName=template_name
        )
        return response['Template']

    def list_templates(self):
        response = self.client.list_templates()
        return response['TemplatesMetadata']

    def send_templated_email(self, source, destination, template_name, template_data):
        response = self.client.send_templated_email(
            Source=source,
            Destination=destination,
            Template=template_name,
            TemplateData=template_data
        )
        return response

    def send_email_with_attachment(self, source, destination, subject, body_text, attachment_data, attachment_name):
        # Encode the attachment data as base64
        # attachment_data_base64 = base64.b64encode(attachment_data).decode()

        # Create the MIME message for the email
        mime_message = MIMEMultipart()
        mime_message['Subject'] = subject
        mime_message['From'] = source
        mime_message['To'] = ', '.join(destination['ToAddresses'])

        # Add body text
        mime_message.attach(MIMEText(body_text, 'plain'))

        # Add attachment
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(attachment_data)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_name}"')
        mime_message.attach(attachment)

        # Convert the MIME message to a string
        raw_message = {'Data': mime_message.as_string()}

        try:
            response = self.client.send_raw_email(
                Source=source,
                Destinations=destination['ToAddresses'],
                RawMessage=raw_message
            )
            return response
        except ClientError as e:
            print(f"Error sending email: {e.response['Error']['Message']}")
            raise

    def receive_email_from_client(self, subject, body, sender_email, recipient_email):
        try:
            response = self.client.send_raw_email(
                Source=sender_email,
                RawMessage={
                    # Include subject in the email data
                    'Data': f"Subject: {subject}\n\n{body}",
                },
                Destinations=[
                    recipient_email,  # Replace with the recipient's email address
                ]
            )
            print("Email sent successfully:", response)
        except self.client.exceptions.MessageRejected as e:
            print("Error sending email:", e)

    def list_verified_emails(self):
        try:
            response = self.client.list_verified_email_addresses()
            verified_emails = response.get('VerifiedEmailAddresses', [])
            return verified_emails
        except Exception as e:
            print(f"Error listing verified emails: {e}")
            return None



def account_activation_template():
    template_manager = AWSEmailTemplateManager()

    template_name = "AccountActivationTemplate"
    subject_part = "Complete Your Total Health Care 360 Platform Registration"

    html_body = """
    <html>
        <body>
            <p>Dear {{name}},</p>
            <p>Thank you for registering on our platform, Total Health Care 360. To activate your account, please click 
            on the button below.</p>
            <button><a href="{{link}}">Activate My Account</a></button>
            <br>
            <p>If the activate link does not work, copy and paste the below link in your browser:</p>
            <br>
            <p>{{link}}</p>
            <p>If you have any questions, please contact us at <a href="mailto:support@totalhealthcare360.com">support@totalhealthcare360.com</a></p>
            <p>Best Regards,</p>
            <p>Total Health Care Team</p>
        </body>
    </html>
    """
    text_body = """
    Dear {{name}},
    
    Thank you for registering on our platform, Total Health Care 360. To activate your account, please click on the button below..
    
    Click the link below to activate your account.
     {{link}} 
     
    If you have any questions, please contact us at support@totalhealthcare360.com
    Best Regards,
    Total Health Care Team
    """

    try:
        template = template_manager.get_template(template_name)
        if template:
            template_manager.delete_template(template_name)

        template_manager.create_template(
            template_name, subject_part, html_body, text_body)
        print("1. Account activation template created")

    except Exception as e:
        print(f"Failed to create Account activation template: {e}")
        return None



def reset_password_template():
    template_manager = AWSEmailTemplateManager()

    template_name = "ResetPasswordTemplate"
    subject_part = "Total Health Care - Password Reset Request"
    html_body = """
    <html>
        <body>
            <p>Dear {{name}},</p>
            <p>We received a request to reset your password. Please click on the button below and follow the prompts to create a new password.</p>
             <button><a href="{{link}}">Reset My Password</a></button>
            <p>If you didn't request this, please ignore this email or contact us at<a href='mailto:support@totalhealthcare360.com'>support@totalhealthcare360.com</a></p>
            <p>Best Regards,</p>
            <p>Total Health Care Team</p>
        </body>
    </html>
    """
    text_body = """
            Dear {{name}},
            We received a request to reset your password. Please click on the button below and follow the prompts to create a new password.
            {{link}}">
            If you didn't request this, please ignore this email or contact us at support@totalhealthcare360.com
            Best Regards,
            Total Health Care Team
            """

    try:
        template = template_manager.get_template(template_name)
        if template:
            template_manager.delete_template(template_name)

        template_manager.create_template(
            template_name, subject_part, html_body, text_body)
        print("reset password template created")

    except Exception as e:
        print(
            f"Failed to create New health plan template reset password template: {e}")
        return None

# 6. Subscription expiry email template



def run_create_template():
    account_activation_template()
    reset_password_template()



