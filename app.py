from flask import Flask, request, jsonify
import openai
import random

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

# Initial price range for the negotiation
price_range = {'min': 50, 'max': 150}

# Helper function to generate a response from GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Endpoint to handle negotiation requests
@app.route('/negotiate', methods=['POST'])
def negotiate():
    user_message = request.json.get('message')
    
    # Example prompts
    if "desired price" in user_message.lower():
        prompt = (
            "You are a negotiation chatbot. Your job is to negotiate the price of a product. "
            "The price range for this product is between ${min} and ${max}. "
            "A customer has proposed a price of ${user_price}. You need to respond with a counteroffer or accept the price."
        ).format(min=price_range['min'], max=price_range['max'], user_price=user_message)
    else:
        prompt = (
            "You are a negotiation chatbot. Engage in a conversation with the user regarding product pricing. "
            "If the user asks for a price, provide an offer within the range of ${min} to ${max}. "
            "Respond based on the user's input, aiming to simulate a negotiation process."
        ).format(min=price_range['min'], max=price_range['max'])
    
    # Get response from GPT-3
    gpt_response = generate_response(prompt)
    
    # Determine whether to accept, reject or counteroffer
    if "accept" in gpt_response.lower():
        response = {
            'message': f"Offer accepted! The final price is ${user_message}.",
            'status': 'accepted'
        }
    elif "reject" in gpt_response.lower():
        response = {
            'message': "Sorry, your offer is too low. Please make a new offer.",
            'status': 'rejected'
        }
    else:
        # Generate a counteroffer
        counteroffer = random.randint(price_range['min'], price_range['max'])
        response = {
            'message': f"Counteroffer: ${counteroffer}.",
            'status': 'counteroffer'
        }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
