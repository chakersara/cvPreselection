# CV Preselection (ReScan)

ReScan is a Flask-based web application designed to automate the initial stages of recruitment by preselecting candidates based on recruiter-defined criteria. This application provides a platform to quickly analyze and filter CVs, making the preselection process more efficient and streamlined.

## Features

- **Automated CV Filtering**: Easily filter candidates by skills, language, experience, and keywords.
- **Data Analysis**: Analyze candidate profiles.
- **User-Friendly Web Interface**: An accessible and intuitive web interface powered by Flask.

## Folder Structure

- **`app/`**: Main application folder containing the core application logic:
  - **`admin/`**: Contains admin-related logic and views.
  - **`api_resume/`**: Handles API endpoints for resume data.
  - **`api_skills/`**: Handles API endpoints for skills data.
  - **`database/`**: Database-related files and configuration.
  - **`models/`**: Data models for storing candidate information.
    - **`adminEntity.py`**: Defines the admin entity model.
    - **`resumeEntity.py`**: Defines the resume entity model.
  - **`static/`**: CSS, JavaScript, and images for the frontend.
  - **`templates/`**: HTML templates for rendering web pages, powered by the Jinja2 template engine.
- **`tests/`**: Contains test cases for the application.
- **`config.py`**: Configuration file for application settings.
- **`main.py`**: Entry point for running the Flask application.
- **`service.py`**: Contains service-related logic.
- **`venv/`**: Virtual environment for managing dependencies.
- **`requirements.txt`**: Lists all the dependencies needed for the project.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chakersara/cvPreselection.git
   cd cvPreselection
   ```

2. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

To run the tests, navigate to the `app` folder and run the following command:

```bash
cd app
pytest
```

## Usage

1. **Start the Flask Application**

   To run the application using Flask, use the command:

   ```bash
   flask run
   ```

   Make sure that the `FLASK_APP` environment variable is set to the correct entry point. You can set it with the following command:

   ```bash
   export FLASK_APP=app/main.py   # On Windows use `set FLASK_APP=app\main.py`
   ```

   Optionally, you can enable debug mode for easier development:

   ```bash
   export FLASK_ENV=development   # On Windows use `set FLASK_ENV=development`
   ```

   After running `flask run`, this will start a local server. You can access the application by navigating to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

2. **Configuration**

   Adjust any configuration settings in `config.py` to set up parameters such as preselection criteria, database settings, or API keys if needed.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:

   ```bash
   git checkout -b feature-name
   ```

3. **Make your changes and commit them**:

   ```bash
   git commit -m 'Add new feature'
   ```

4. **Push to the branch**:

   ```bash
   git push origin feature-name
   ```

5. **Open a pull request**.

