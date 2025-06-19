# Content App

This project is a Flask web application that serves educational content based on various programming topics. It provides an API to generate content in different formats, including paragraphs, code snippets, and tips.

## Project Structure

- **app.py**: The main application file that sets up the Flask web server and handles API requests.
- **requirements.txt**: Lists the dependencies required for the project.
- **venv/**: Contains the virtual environment for isolating project dependencies.
- **templates/index.html**: The main HTML template for the application.
- **static/style.css**: Contains the CSS styles for the application.

## Setup Instructions# 🧠 content.app – Flask Code Template Generator

[![Live Site](https://img.shields.io/badge/Live%20Site-pikelela.pythonanywhere.com-green)](https://pikelela.pythonanywhere.com)
[![Built with Flask](https://img.shields.io/badge/Built%20With-Flask-blue)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

**content.app** is a web-based code template generator built with Flask. It allows users to input prompts and generates code snippets in HTML, CSS, JavaScript, or Python. This project demonstrates full-stack web development, version control with Git, and deployment to a cloud platform (PythonAnywhere).

🌐 **Live Demo:**  
🔗 [https://pikelela.pythonanywhere.com](https://pikelela.pythonanywhere.com)

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Version Control:** Git, GitHub
- **Hosting:** PythonAnywhere
- **Others:** Virtualenv, Bash

---

## 🛠 Local Flask Setup & Testing

1. Clone the repository:
   ```bash
   git clone https://github.com/pikelelalikho/content.app.git
   cd content.app
Create and activate a virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app locally:

bash
Copy
Edit
python app.py
Then open http://localhost:5000 in your browser.

💾 Git Versioning & GitHub Sync
Initialized Git:

bash
Copy
Edit
git init
Committed changes:

bash
Copy
Edit
git add .
git commit -m "Initial commit"
Connected and pushed to GitHub:

bash
Copy
Edit
git remote add origin https://github.com/pikelelalikho/content.app.git
git push -u origin main
☁️ Deployment on PythonAnywhere
Signed up at PythonAnywhere

Opened a Bash console and cloned the repo:

bash
Copy
Edit
git clone https://github.com/pikelelalikho/content.app.git
Set up virtual environment and installed dependencies:

bash
Copy
Edit
cd content.app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Created a new web app (manual config):

Source code: /home/pikelela/content.app

Virtualenv: /home/pikelela/content.app/venv

⚙️ WSGI Configuration
Edited the WSGI file (pikelela.pythonanywhere.com_wsgi.py):

python
Copy
Edit
import sys
path = '/home/pikelela/content.app'
if path not in sys.path:
    sys.path.append(path)
from app import app as application
Reloaded the app from the Web tab to reflect changes.

🔁 Updating the Live App
To reflect GitHub changes on the live site:

Commit and push updates to GitHub.

On PythonAnywhere:

bash
Copy
Edit
cd content.app
git pull
Reload the web app from the Web tab.

🚀 Live Site
🟢 https://pikelela.pythonanywhere.com

🔮 Future Improvements
Add user authentication

Save generated outputs to a database

Add syntax highlighting to code output

Enable file download for generated code

📄 License
MIT License – use freely with attribution.

👤 Author
Likho Pikelela
💼 LinkedIn | 🌍 Portfolio

yaml
Copy
Edit

---

Let me know if you'd like me to:

- Add your **real LinkedIn or portfolio links**.
- Add **badges** for Flask, PythonAnywhere, or GitHub stats.
- Include an **animated demo GIF or screenshot** to the top.

Ready to upload or edit it for you!

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd content-app
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```
   python app.py
   ```

6. **Access the application**: Open your web browser and go to `pikelela.pythonanywhere.com`.

## API Endpoints

- **POST /api/generate**: Generates content based on the provided topic and content type. The request body should include:
  - `topic`: The programming topic (e.g., "html", "css", "javascript", "python").
  - `content_type`: The type of content to generate (e.g., "paragraph", "code", "tips"). 

## License

This project is licensed under the MIT License.
