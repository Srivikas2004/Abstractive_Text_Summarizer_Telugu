from flask import Flask, render_template, request, redirect, url_for
from Text_summarizer import summarize_with_disambiguation
import json
import subprocess
import os

app = Flask(__name__)

# Define paths relative to the current script's directory
current_dir = os.path.dirname(__file__)
json_file_path = os.path.join(current_dir, '../input_text.json')
python_file_path = os.path.join(current_dir, '../../Text_summarizer.py')

def load_data():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {"text": ""}
    return data

def save_data(data):
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


@app.route('/')
def index():
    data = load_data()
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    input_text = request.form['inputText']
    data = load_data()
    data['text'] = input_text
    save_data(data)

    # Run the Python file as a separate process
    command = f'python {python_file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # Print the output to the console
    print("Output:", output.decode('utf-8'))
    print("Error:", error.decode('utf-8'))

    # Assume your Python file produces an output file, you can read and display it
    with open('output.txt', 'r', encoding='utf-8') as output_file:
        file_content = output_file.read()

    # Find the index of "Final Summary:" in the file content
    start_index = file_content.find("Final Summary")

    # Check if "Final Summary:" is found
    if start_index != -1:
        # Extract the content after "Final Summary:"
        summary = file_content[start_index + len("Final Summary"):].strip()
    else:
        summary = "Final summary not found."

    return render_template('index.html', input_text=input_text, summary=summary)
if __name__ == '__main__':
    app.run(debug=True)
