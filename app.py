from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load the API key from a .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create the Flask app
app = Flask(__name__)

# This route displays the homepage
@app.route('/')
def index():
    return render_template('index.html')

# This route handles the AI correction when the form is submitted
@app.route('/correct', methods=['POST'])
def correct_text():
    # Get the text the user entered from the form
    user_text = request.form['text']

    try:
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful writing assistant. Correct the grammar and spelling of the following text. Return only the corrected text, nothing else."},
                {"role": "user", "content": user_text}
            ]
        )
        # Get the corrected text from the AI's response
        corrected_text = response.choices[0].message.content
        # Send the result back to the webpage
        return jsonify({'success': True, 'corrected_text': corrected_text})

    except Exception as e:
        # If something goes wrong, send an error message
        return jsonify({'success': False, 'error': str(e)})

# This makes sure the app runs when we execute this script
if __name__ == '__main__':
    app.run(debug=True)