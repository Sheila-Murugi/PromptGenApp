from flask import Flask, request, render_template
import openai
#
app = Flask(__name__)
def generate_prompts(user_question, num_prompts=3):
    # Adjust the prompt to instruct the model to generate prompts instead of answers
    instruction = f"Generate {num_prompts} different prompts based on the following user question: '{user_question}'"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": instruction}
        ],
        max_tokens=150,
        n=num_prompts,
        temperature=0.7
    )
    prompts = [choice['message']['content'].strip() for choice in response['choices']]
    return prompts
    # Example usage
user_question = "Places to eat in Kenya"
generated_prompts = generate_prompts(user_question, num_prompts=5)
for i, prompt in enumerate(generated_prompts, start=1):
    print(f"Prompt {i}: {prompt}")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_question = request.form['user_question']
    generated_prompts = generate_prompts(user_question, num_prompts=5)
    return render_template('result.html', user_question=user_question, generated_prompts=generated_prompts)

if __name__ == '__main__':
    app.run(debug=True)