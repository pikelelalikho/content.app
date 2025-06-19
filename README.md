# Content App

This project is a Flask web application that serves educational content based on various programming topics. It provides an API to generate content in different formats, including paragraphs, code snippets, and tips.

## Project Structure

- **app.py**: The main application file that sets up the Flask web server and handles API requests.
- **requirements.txt**: Lists the dependencies required for the project.
- **venv/**: Contains the virtual environment for isolating project dependencies.
- **templates/index.html**: The main HTML template for the application.
- **static/style.css**: Contains the CSS styles for the application.

## Setup Instructions

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

6. **Access the application**: Open your web browser and go to `http://127.0.0.1:5000`.

## API Endpoints

- **POST /api/generate**: Generates content based on the provided topic and content type. The request body should include:
  - `topic`: The programming topic (e.g., "html", "css", "javascript", "python").
  - `content_type`: The type of content to generate (e.g., "paragraph", "code", "tips"). 

## License

This project is licensed under the MIT License.