# Google-Africastalking-AI-Course

# Voice API
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

