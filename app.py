from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Main HTML page

# INSERT THIS RIGHT AFTER
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ...then continue with the rest like:
# KNOWLEDGE_BASE = { ... }
# Knowledge base for each language and content type
KNOWLEDGE_BASE = {
    "html": {
        "paragraph": "HTML (HyperText Markup Language) is the foundational building block of the web, providing the structure and content of web pages. It uses a system of tags and attributes to define elements like headings, paragraphs, links, images, and more. HTML5, the latest version, introduced semantic elements like <header>, <footer>, <article>, and <section> that make documents more accessible and meaningful.",
        "code": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <header>
        <h1>Welcome to My Site</h1>
        <nav>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <article>
            <h2>Article Title</h2>
            <p>This is a sample article content.</p>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2023 My Site</p>
    </footer>
</body>
</html>""",
        "tips": [
            "Always include the DOCTYPE declaration at the start of your HTML documents",
            "Use semantic HTML5 elements for better accessibility and SEO",
            "Validate your HTML using the W3C Validator",
            "Keep your nesting clean and consistent with proper indentation",
            "Use alt attributes for images to improve accessibility"
        ]
    },
    "css": {
        "paragraph": "CSS (Cascading Style Sheets) is the language used to style and layout web pages. It controls the visual presentation of HTML elements, including colors, fonts, spacing, and positioning. CSS works by selecting HTML elements and applying styles to them through rulesets. Modern CSS includes powerful features like Flexbox and Grid for complex layouts, animations for interactivity, and media queries for responsive design that adapts to different screen sizes.",
        "code": """/* CSS Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Variables for theming */
:root {
    --primary-color: #4361ee;
    --secondary-color: #3f37c9;
    --text-color: #212529;
    --light-bg: #f8f9fa;
}

/* Typography */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--light-bg);
}

/* Layout with Flexbox */
.container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    background-color: var(--primary-color);
    color: white;
    padding: 1rem;
}

/* Responsive design with media queries */
@media (min-width: 768px) {
    .main-content {
        display: grid;
        grid-template-columns: 1fr 3fr;
        gap: 2rem;
    }
}""",
        "tips": [
            "Use CSS variables for consistent theming across your site",
            "Learn Flexbox and Grid for modern layout techniques",
            "Mobile-first design approach often leads to cleaner CSS",
            "Use shorthand properties where possible to reduce code",
            "Organize your CSS with logical sections and comments"
        ]
    },
    "javascript": {
        "paragraph": "JavaScript is a versatile programming language that adds interactivity to web pages. It runs in the browser and can manipulate the Document Object Model (DOM), handle events, make asynchronous requests (AJAX), and much more. Modern JavaScript (ES6+) introduced features like arrow functions, classes, modules, template literals, and promises. JavaScript has evolved beyond the browser with Node.js enabling server-side development, and frameworks like React, Angular, and Vue dominating frontend development.",
        "code": """// DOM manipulation example
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('#myButton');
    const output = document.querySelector('#output');
    
    btn.addEventListener('click', async () => {
        try {
            // Fetch data from an API
            const response = await fetch('https://api.example.com/data');
            const data = await response.json();
            
            // Process and display data
            output.innerHTML = data.map(item => 
                `<div class="item">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                </div>`
            ).join('');
        } catch (error) {
            console.error('Error:', error);
            output.textContent = 'Failed to load data';
        }
    });
});

// ES6+ Features
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
    
    greet() {
        return `Hello, my name is ${this.name} and I'm ${this.age} years old.`;
    }
}

const person = new Person('Alice', 30);
console.log(person.greet());""",
        "tips": [
            "Always use const and let instead of var for variable declarations",
            "Understand asynchronous programming with promises and async/await",
            "Learn the DOM thoroughly before jumping into frameworks",
            "Use array methods like map, filter, and reduce for data manipulation",
            "Always handle errors in asynchronous operations"
        ]
    },
    "python": {
        "paragraph": "Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python's extensive standard library and vast ecosystem of third-party packages make it ideal for web development (Django, Flask), data science (NumPy, Pandas), machine learning (TensorFlow, PyTorch), automation, and more. Python emphasizes code readability with its clean syntax and significant whitespace.",
        "code": """# Python basics
def greet(name):
    return f"Hello, {name}!"

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"My name is {self.name} and I'm {self.age} years old."

# List comprehension
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]

# File handling
try:
    with open('file.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found")

# Web request with requests library
import requests
response = requests.get('https://api.example.com/data')
data = response.json()""",
        "tips": [
            "Follow PEP 8 style guide for consistent Python code",
            "Use virtual environments for project dependencies",
            "Learn list comprehensions for concise data transformations",
            "Prefer context managers (with statement) for resource handling",
            "Write docstrings for all public modules, functions, classes, and methods"
        ]
    }
}

def count_words(text):
    return len(text.split())

def count_chars(text):
    return len(text)

@app.route('/api/generate', methods=['POST'])
def generate_content():
    data = request.get_json()
    topic = data.get('topic')
    content_type = data.get('content_type')
    
    # Validate input
    if topic not in KNOWLEDGE_BASE or content_type not in ['paragraph', 'code', 'tips']:
        return jsonify({
            "error": "Invalid topic or content type",
            "valid_topics": list(KNOWLEDGE_BASE.keys()),
            "valid_content_types": ['paragraph', 'code', 'tips']
        }), 400

    # Get the appropriate content
    if content_type == 'tips':
        tips = KNOWLEDGE_BASE[topic]['tips']
        content = "\n".join(f"• {tip}" for tip in tips)
    elif content_type == 'code':
        import html
        raw_code = KNOWLEDGE_BASE[topic]['code']
        content = html.escape(raw_code)  # Escape HTML code to show as text
    else:
        content = KNOWLEDGE_BASE[topic][content_type]

    # Generate metadata
    metadata = {
        "word_count": count_words(content),
        "char_count": count_chars(content),
        "timestamp": datetime.now().isoformat(),
        "language": topic,
        "content_type": content_type
    }

    return jsonify({
        "content": content,
        "metadata": metadata
    })

if __name__ == '__main__':
    app.run(debug=True)