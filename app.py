from flask import Flask, request, jsonify, send_from_directory, render_template
from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Expanded Knowledge Base with prompt-based templates
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
        ],
        "templates": {
            "form": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        input, select, textarea {{ width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }}
        button {{ background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }}
        button:hover {{ background-color: #0056b3; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <form>
        {form_fields}
        <button type="submit">Submit</button>
    </form>
</body>
</html>""",
            "landing": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; }}
        .hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 0; text-align: center; }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.2rem; margin-bottom: 2rem; }}
        .cta-button {{ display: inline-block; background: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
        .features {{ padding: 80px 0; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }}
        .feature {{ text-align: center; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="container">
            <h1>{title}</h1>
            <p>{description}</p>
            <a href="#" class="cta-button">Get Started</a>
        </div>
    </section>
    
    <section class="features">
        <div class="container">
            <div class="features-grid">
                <div class="feature">
                    <h3>Feature 1</h3>
                    <p>Description of your first feature</p>
                </div>
                <div class="feature">
                    <h3>Feature 2</h3>
                    <p>Description of your second feature</p>
                </div>
                <div class="feature">
                    <h3>Feature 3</h3>
                    <p>Description of your third feature</p>
                </div>
            </div>
        </div>
    </section>
</body>
</html>""",
            "card": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; padding: 20px; }}
        .card-container {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; }}
        .card {{ background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; width: 300px; transition: transform 0.3s; }}
        .card:hover {{ transform: translateY(-5px); }}
        .card-header {{ background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 20px; }}
        .card-body {{ padding: 20px; }}
        .card-footer {{ padding: 15px 20px; background: #f8f9fa; }}
        .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 30px;">{title}</h1>
    <div class="card-container">
        {cards}
    </div>
</body>
</html>""",
            "dashboard": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #f5f6fa; }}
        .sidebar {{ position: fixed; left: 0; top: 0; width: 250px; height: 100vh; background: #2c3e50; color: white; padding: 20px 0; }}
        .sidebar h2 {{ text-align: center; margin-bottom: 30px; }}
        .sidebar ul {{ list-style: none; }}
        .sidebar li {{ padding: 15px 20px; cursor: pointer; transition: background 0.3s; }}
        .sidebar li:hover {{ background: #34495e; }}
        .main-content {{ margin-left: 250px; padding: 20px; }}
        .header {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 2rem; font-weight: bold; color: #3498db; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>{title}</h2>
        <ul>
            <li>Dashboard</li>
            <li>Analytics</li>
            <li>Users</li>
            <li>Settings</li>
        </ul>
    </div>
    
    <div class="main-content">
        <div class="header">
            <h1>Welcome to Dashboard</h1>
            <p>Overview of your data and metrics</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">1,234</div>
                <div>Total Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">567</div>
                <div>Active Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">89%</div>
                <div>Success Rate</div>
            </div>
        </div>
    </div>
</body>
</html>"""
        }
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
        ],
        "templates": {
            "animations": """/* CSS Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}

@keyframes bounce {
    0%, 20%, 60%, 100% { transform: translateY(0); }
    40% { transform: translateY(-20px); }
    80% { transform: translateY(-10px); }
}

.fade-in { animation: fadeIn 0.6s ease-out; }
.slide-in { animation: slideIn 0.5s ease-out; }
.bounce { animation: bounce 2s infinite; }

/* Hover Effects */
.hover-lift {
    transition: transform 0.3s ease;
}
.hover-lift:hover {
    transform: translateY(-5px);
}

.hover-glow {
    transition: box-shadow 0.3s ease;
}
.hover-glow:hover {
    box-shadow: 0 0 20px rgba(67, 97, 238, 0.5);
}""",
            "grid": """/* CSS Grid Layouts */
.grid-container {
    display: grid;
    gap: 20px;
    padding: 20px;
}

/* Responsive Grid */
.auto-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

/* Named Grid Areas */
.layout-grid {
    grid-template-areas: 
        "header header header"
        "sidebar main main"
        "footer footer footer";
    grid-template-rows: auto 1fr auto;
    grid-template-columns: 200px 1fr 1fr;
    min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Card Grid */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}""",
            "flexbox": """/* Flexbox Utilities */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }
.flex-wrap { flex-wrap: wrap; }

/* Alignment */
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }

/* Common Flex Patterns */
.flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
}

.flex-between {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.flex-grow { flex: 1; }
.flex-shrink-0 { flex-shrink: 0; }"""
        }
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
        ],
        "templates": {
            "api": """// API Integration
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }
    
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'GET',
                headers: this.headers
            });
            return await response.json();
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    }
    
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    }
}

// Usage
const api = new APIClient('https://api.example.com');
api.get('/users').then(users => console.log(users));""",
            "validation": """// Form Validation
class FormValidator {
    constructor(formId) {
        this.form = document.getElementById(formId);
        this.errors = {};
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (this.validate()) {
                this.onSuccess();
            }
        });
    }
    
    validate() {
        this.errors = {};
        const formData = new FormData(this.form);
        
        // Email validation
        const email = formData.get('email');
        if (!this.isValidEmail(email)) {
            this.errors.email = 'Please enter a valid email address';
        }
        
        // Password validation
        const password = formData.get('password');
        if (password.length < 8) {
            this.errors.password = 'Password must be at least 8 characters';
        }
        
        this.displayErrors();
        return Object.keys(this.errors).length === 0;
    }
    
    isValidEmail(email) {
        return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
    }
    
    displayErrors() {
        // Clear previous errors
        document.querySelectorAll('.error').forEach(el => el.remove());
        
        // Display new errors
        Object.keys(this.errors).forEach(field => {
            const input = this.form.querySelector(`[name="${field}"]`);
            const error = document.createElement('div');
            error.className = 'error';
            error.textContent = this.errors[field];
            input.parentNode.appendChild(error);
        });
    }
    
    onSuccess() {
        console.log('Form is valid!');
        // Submit the form or perform other actions
    }
}

// Usage
new FormValidator('myForm');""",
            "slider": """// Image Slider
class ImageSlider {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.slides = this.container.querySelectorAll('.slide');
        this.currentSlide = 0;
        this.totalSlides = this.slides.length;
        
        this.createNavigation();
        this.showSlide(0);
        this.startAutoplay();
    }
    
    createNavigation() {
        const nav = document.createElement('div');
        nav.className = 'slider-nav';
        
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '❮';
        prevBtn.onclick = () => this.prevSlide();
        
        const nextBtn = document.createElement('button');
        nextBtn.textContent = '❯';
        nextBtn.onclick = () => this.nextSlide();
        
        nav.appendChild(prevBtn);
        nav.appendChild(nextBtn);
        this.container.appendChild(nav);
    }
    
    showSlide(index) {
        this.slides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
        });
        this.currentSlide = index;
    }
    
    nextSlide() {
        const next = (this.currentSlide + 1) % this.totalSlides;
        this.showSlide(next);
    }
    
    prevSlide() {
        const prev = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.showSlide(prev);
    }
    
    startAutoplay() {
        setInterval(() => this.nextSlide(), 5000);
    }
}

// Usage
new ImageSlider('imageSlider');"""
        }
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
        ],
        "templates": {
            "api": """# Flask API
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data
users = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com'}
]

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        'id': len(users) + 1,
        'name': data.get('name'),
        'email': data.get('email')
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)""",
            "data_analysis": """# Data Analysis with Pandas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data.csv')

# Data exploration
print("Dataset shape:", df.shape)
print("\\nDataset info:")
print(df.info())
print("\\nFirst few rows:")
print(df.head())

# Data cleaning
df = df.dropna()  # Remove missing values
df = df.drop_duplicates()  # Remove duplicates

# Statistical analysis
print("\\nDescriptive statistics:")
print(df.describe())

# Visualization
plt.figure(figsize=(12, 8))

# Histogram
plt.subplot(2, 2, 1)
df['column_name'].hist(bins=20)
plt.title('Distribution of Column')

# Box plot
plt.subplot(2, 2, 2)
sns.boxplot(data=df, y='column_name')
plt.title('Box Plot')

# Correlation heatmap
plt.subplot(2, 2, 3)
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')

# Scatter plot
plt.subplot(2, 2, 4)
plt.scatter(df['x_column'], df['y_column'])
plt.xlabel('X Column')
plt.ylabel('Y Column')
plt.title('Scatter Plot')

plt.tight_layout()
plt.show()""",
            "automation": """# Automation Script
import os
import shutil
import schedule
import time
from datetime import datetime

class FileOrganizer:
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.file_types = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov'],
            'audio': ['.mp3', '.wav', '.flac', '.aac']
        }
    
    def organize_files(self):
        print(f"Starting file organization at {datetime.now()}")
        
        for filename in os.listdir(self.source_dir):
            if os.path.isfile(os.path.join(self.source_dir, filename)):
                file_ext = os.path.splitext(filename)[1].lower()
                
                # Determine file category
                category = 'others'
                for cat, extensions in self.file_types.items():
                    if file_ext in extensions:
                        category = cat
                        break
                
                # Create category directory if it doesn't exist
                category_dir = os.path.join(self.dest_dir, category)
                os.makedirs(category_dir, exist_ok=True)
                
                # Move file
                source = os.path.join(self.source_dir, filename)
                destination = os.path.join(category_dir, filename)
                
                try:
                    shutil.move(source, destination)
                    print(f"Moved {filename} to {category}")
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
    
    def schedule_organization(self):
        schedule.every().day.at("09:00").do(self.organize_files)
        schedule.every().day.at("18:00").do(self.organize_files)
        
        print("File organization scheduled for 9:00 AM and 6:00 PM daily")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Usage
organizer = FileOrganizer('/path/to/downloads', '/path/to/organized')
organizer.organize_files()  # Run once
# organizer.schedule_organization()  # Run on schedule"""
        }
    }
}

def count_words(text):
    return len(text.split())

def count_chars(text):
    return len(text)

def generate_from_prompt(language, prompt):
    """Generate code based on user prompt"""
    prompt_lower = prompt.lower()
    
    # HTML prompt patterns
    if language == 'html':
        if any(keyword in prompt_lower for keyword in ['form', 'contact', 'signup', 'login']):
            title = extract_title(prompt) or "Contact Form"
            form_fields = generate_form_fields(prompt)
            return KNOWLEDGE_BASE['html']['templates']['form'].format(
                title=title,
                form_fields=form_fields
            )
        elif any(keyword in prompt_lower for keyword in ['landing', 'homepage', 'hero']):
            title = extract_title(prompt) or "Welcome to Our Site"
            description = extract_description(prompt) or "Transform your ideas into reality"
            return KNOWLEDGE_BASE['html']['templates']['landing'].format(
                title=title,
                description=description
            )
        elif any(keyword in prompt_lower for keyword in ['card', 'product', 'showcase']):
            title = extract_title(prompt) or "Product Showcase"
            cards = generate_cards(prompt)
            return KNOWLEDGE_BASE['html']['templates']['card'].format(
                title=title,
                cards=cards
            )
        elif any(keyword in prompt_lower for keyword in ['dashboard', 'admin', 'panel']):
            title = extract_title(prompt) or "Admin Dashboard"
            return KNOWLEDGE_BASE['html']['templates']['dashboard'].format(title=title)
    
    # CSS prompt patterns
    elif language == 'css':
        if any(keyword in prompt_lower for keyword in ['animation', 'animate', 'hover']):
            return KNOWLEDGE_BASE['css']['templates']['animations']
        elif any(keyword in prompt_lower for keyword in ['grid', 'layout']):
            return KNOWLEDGE_BASE['css']['templates']['grid']
        elif any(keyword in prompt_lower for keyword in ['flex', 'flexbox']):
            return KNOWLEDGE_BASE['css']['templates']['flexbox']
    
    # JavaScript prompt patterns
    elif language == 'javascript':
        if any(keyword in prompt_lower for keyword in ['api', 'fetch', 'ajax']):
            return KNOWLEDGE_BASE['javascript']['templates']['api']
        elif any(keyword in prompt_lower for keyword in ['validation', 'form', 'validate']):
            return KNOWLEDGE_BASE['javascript']['templates']['validation']
        elif any(keyword in prompt_lower for keyword in ['slider', 'carousel', 'gallery']):
            return KNOWLEDGE_BASE['javascript']['templates']['slider']
    
    # Python prompt patterns
    elif language == 'python':
        if any(keyword in prompt_lower for keyword in ['api', 'flask', 'web']):
            return KNOWLEDGE_BASE['python']['templates']['api']
        elif any(keyword in prompt_lower for keyword in ['data', 'analysis', 'pandas']):
            return KNOWLEDGE_BASE['python']['templates']['data_analysis']
        elif any(keyword in prompt_lower for keyword in ['automation', 'script', 'organize']):
            return KNOWLEDGE_BASE['python']['templates']['automation']
    
    # Default to basic code if no specific pattern matched
    return KNOWLEDGE_BASE[language]['code']

def extract_title(prompt):
    """Extract title from prompt"""
    # Look for patterns like "create a form for..." or "make a landing page called..."
    patterns = [
        r'(?:for|called|titled|named)\s+([A-Za-z0-9\s]+)',
        r'(?:create|make|build)\s+(?:a\s+)?([A-Za-z0-9\s]+?)(?:\s+(?:page|form|site))',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, prompt, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
    return None

def extract_description(prompt):
    """Extract description from prompt"""
    # Look for description patterns
    if 'about' in prompt.lower():
        parts = prompt.lower().split('about')
        if len(parts) > 1:
            return parts[1].strip()[:100]
    return None

def generate_form_fields(prompt):
    """Generate form fields based on prompt"""
    fields = []
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['name', 'contact']):
        fields.append('''
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>''')
    
    if any(word in prompt_lower for word in ['email', 'contact']):
        fields.append('''
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>''')
    
    if any(word in prompt_lower for word in ['phone', 'contact']):
        fields.append('''
        <div class="form-group">
            <label for="phone">Phone:</label>
            <input type="tel" id="phone" name="phone">
        </div>''')
    
    if any(word in prompt_lower for word in ['message', 'comment']):
        fields.append('''
        <div class="form-group">
            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="4"></textarea>
        </div>''')
    
    if any(word in prompt_lower for word in ['password', 'login', 'signup']):
        fields.append('''
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>''')
    
    # Default fields if none specified
    if not fields:
        fields = [
            '''
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>''',
            '''
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>'''
        ]
    
    return ''.join(fields)

def generate_cards(_):
    """Generate card HTML based on prompt"""
    # Default cards
    cards = []
    for i in range(3):
        card = f'''
        <div class="card">
            <div class="card-header">
                <h3>Card {i+1}</h3>
            </div>
            <div class="card-body">
                <p>This is the content for card {i+1}. You can customize this based on your needs.</p>
            </div>
            <div class="card-footer">
                <a href="#" class="btn">Learn More</a>
            </div>
        </div>'''
        cards.append(card)
    
    return ''.join(cards)

@app.route('/api/generate', methods=['POST'])
def generate_content():
    data = request.get_json()
    topic = data.get('topic')
    content_type = data.get('content_type')
    prompt = data.get('prompt', '')
    
    # Validate input
    if topic not in KNOWLEDGE_BASE:
        return jsonify({
            "error": "Invalid topic",
            "valid_topics": list(KNOWLEDGE_BASE.keys())
        }), 400

    # Generate content based on type
    if content_type == 'tips':
        tips = KNOWLEDGE_BASE[topic]['tips']
        content = "\n".join(f"• {tip}" for tip in tips)
    elif content_type == 'code':
        if prompt:
            # Use prompt-based generation
            content = generate_from_prompt(topic, prompt)
        else:
            # Use default code
            content = KNOWLEDGE_BASE[topic]['code']
    elif content_type == 'prompt':
        # New prompt-based generation
        content = generate_from_prompt(topic, prompt)
    else:
        content = KNOWLEDGE_BASE[topic][content_type]

    # Generate metadata
    metadata = {
        "word_count": count_words(content),
        "char_count": count_chars(content),
        "timestamp": datetime.now().isoformat(),
        "language": topic,
        "content_type": content_type,
        "prompt_used": bool(prompt)
    }

    return jsonify({
        "content": content,
        "metadata": metadata
    })

@app.route('/api/preview', methods=['POST'])
def preview_html():
    """Generate HTML preview for HTML content"""
    data = request.get_json()
    html_content = data.get('content', '')
    
    # Return the HTML content for preview
    return jsonify({
        "html": html_content,
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True)
