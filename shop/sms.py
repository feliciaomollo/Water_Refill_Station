import africastalking
from decouple import config

def send_sms(phone_number, message):
    africastalking.initialize(
        username=config('AT_USERNAME'),
        api_key=config('AT_API_KEY')
    )

    sms = africastalking.SMS

    try:
        response = sms.send(message, [phone_number])
        return {'success': True, 'response': response}
    except Exception as e:
        return {'success': False, 'error': str(e)}