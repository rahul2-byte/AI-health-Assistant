import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python")))
from components.server import TelegramBot
import json

def main(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    bot = TelegramBot(is_local=False)
    
    try:
        # Set up on AWS URL if provided
        aws_url = os.environ.get('AWS_WEBHOOK_URL')
        if aws_url:
            bot.setup_webhook(aws_url)

        # Handle the webhook request
        if event.get('body'):
            # Create Flask request context for webhook handling
            with bot.app.test_request_context(
                path='/webhook',
                method='POST',
                data=event['body'],
                headers=event.get('headers', {})
            ):
                # Process webhook and get response
                response = bot.webhook()
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps(response.get_json() if hasattr(response, 'get_json') else response)
                }
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'No body found in request'
                })
            }
    except Exception as e:
        print(f"Error in lambda handler: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }

if __name__ == "__main__":
    # Run locally
    bot = TelegramBot(is_local=True)
    bot.run_local()