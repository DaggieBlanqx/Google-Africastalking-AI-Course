# Google-Africastalking-AI-Course

This repository contains code examples and instructions for integrating Africa's Talking APIs with AI models, specifically focusing on SMS, Airtime, Sim Swap, and Voice functionalities. It also includes guidance on setting up webhooks and callbacks to handle asynchronous events.


## Prerequisites
- Python 3.8+
- Africa's Talking account (https://account.africastalking.com/) and API keys, production voice number
- Local server setup (e.g., Flask)
- Tunneling tool (e.g., Ngrok, Cloudflare Tunnel, Localhost.run)
- Google Cloud account for Gemini and Vertex AI (https://cloud.google.com/) and API keys.


## Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/DaggieBlanqx/Google-Africastalking-AI-Course
    cd Google-Africastalking-AI-Course
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
    ```

3. Install the required packages:
    ```bash
    make install
    ```
4. Create a `.env` file in the root directory and add your Africa's Talking and Google Cloud credentials:
    ```
    AT_USERNAME=your_at_username
    AT_API_KEY=your_at_api_key
    AT_VOICE_NUMBER=your_voice_enabled_phone_number
    AT_SHORTCODE=8995
    PROJECT_ID=your_gcp_project_id
    GEMINI_API_KEY=your_gemini_api_key
    VERTEX_API_KEY=your_vertex_api_key
    ```

5. Set up Ngrok or any tunneling tool to expose your local server to the internet:
    ```bash
    ngrok authtoken YOUR_NGROK_AUTH_TOKEN
    ngrok http 5000
    ```
6. Update your Africa's Talking app settings to point to your public Ngrok URL for webhooks:
    - SMS Delivery Report URL: `https://your-ngrok-url/api/sms/delivery
    - Voice Call Instructions URL: `https://your-ngrok-url/api/voice/instruct`
    - Voice Event Notification URL: `https://your-ngrok-url/api/voice/events`

7. Run the Flask application:
    ```bash
    make dev
    ```
8. Test the endpoints using tools like Postman or curl or your web browser.

# SMS API
- You require an Africastalking app with SMS product enabled, or alternatively, you can use the sandbox.

- If you don't have one, create one at https://account.africastalking.com then create a team and inside the team create an app, then make a product request for SMS (For production) or use the sandbox credentials.

- Once you have the app, get the API key and set the callback URL to your server endpoint:
  - Delivery report URL: `https://yourdomain.com/api/sms/delivery`
  - Two-way SMS URL: `https://yourdomain.com/api/sms/twoway`

- In your `.env` file, set the following variables:
```
AT_USERNAME=your_at_username
AT_API_KEY=your_at_api_key
AT_SHORTCODE=your_shortcode (if you are doing two-way SMS)
```

- With the above setup, you can now send bulk SMS, handle delivery reports and send two-way SMS.

## Endpoints
- **GET /api/sms/**: Check the status of the SMS service.
- **GET /api/sms/invoke-bulk-sms?phone=2547XXXXXXX&message=Hell World**: Invoke a bulk SMS to the specified phone number with the given message.
- **GET /api/sms/invoke-two-way-sms?phone=2547XXXXXXX&message=Hello World**: Invoke a two-way SMS to the specified phone number with the given message.
- **POST /api/sms/delivery**: Webhook endpoint to receive SMS delivery reports.
- **POST /api/sms/twoway**: Webhook endpoint to receive incoming two-way SMS messages.

# Voice API (Must be production not sandbox)
- You require a voice-enabled Africastalking app. If you don't have one, create one at https://account.africastalking.com then create a team and inside the team create an app, then make a product request for voice.

- Once you have the voice-enabled app, get the phone number issued to you and set callback URLs to your server endpoints:
  - Call instructions URL: `https://yourdomain.com/api/voice/instruct`
  - Event notification URL: `https://yourdomain.com/api/voice/events`

- In your `.env` file, set the following variables:
```
AT_USERNAME=your_at_username
AT_API_KEY=your_at_api_key
AT_VOICE_NUMBER=your_voice_enabled_phone_number
```
- With the above setup, you can now make and receive voice calls.

## Endpoints
- **GET /api/voice/**: Check the status of the voice service.
- **GET /api/voice/invoke-call?phone=2547XXXXXXX**: Invoke a voice call to the specified phone number.
- **POST /api/voice/instruct**: Webhook endpoint to provide call instructions in XML format.
- **POST /api/voice/events**: Webhook endpoint to receive call event notifications (e.g., answered, completed).

## How to use Gemini API
- Go to https://aistudio.google.com/api-keys
- Create an API key 
- Add the API key to your .env file as GEMINI_API_KEY
- Then go to https://ai.google.dev/gemini-api/docs/quickstart
- Install the sdk for your language e.g Python

```bash
pip install -q -U google-genai
```

