# Arcade Sessions Visualization
![Video Project 1 (1)](https://github.com/user-attachments/assets/bfcbbca7-e6fc-454f-9b18-3db8b4993de8)

## Overview

This Flask web application allows users to visualize, filter, and analyze data from arcade sessions. It features interactive charts, an advanced filtering system, and export options for CSV and Excel files. Users can log in to save their preferences and settings, ensuring a personalized experience every time they visit.

## Features

- **Interactive Data Visualization**: View session data through various interactive charts (line, bar, scatter, etc.).
- **Advanced Filtering**: Filter sessions by date, duration, and goals.
- **Data Export**: Export filtered data to CSV or Excel.
- **Responsive Design**: Accessible on both desktop and mobile devices.
- **User Authentication**: Log in and save personalized settings.
- **Interactive Data Table**: Search, sort, and filter session data in a dynamic table.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Pandas
- Plotly
- Flask-Login
- Datatables (JavaScript library)

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/arcade-sessions-visualization.git
    cd arcade-sessions-visualization
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the project root with the following content:
      ```env
      FLASK_APP=app.py
      FLASK_ENV=development
      API_TOKEN=your_slack_api_token
      USER_ID=your_slack_user_id
      ```

5. **Run the application**:
    ```bash
    flask run
    ```

6. **Access the application**:
    - Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

### Data Import
1. Ensure your session data is in `arcade_sessions.csv`.
2. The CSV file should have the following columns: `Created At`, `Time`, `Elapsed`, `Goal`, `Ended`, and `Work`.

### Logging In
1. Visit the `/login` route to log in using your email.
2. Upon logging in, you can access the profile page to manage your settings.

### Data Visualization
1. Explore various charts on the homepage, showing trends and distributions of session data.
2. Use the filtering options to customize which data is shown.

### Exporting Data
1. Click on the "Export as CSV" or "Export as Excel" buttons to download the filtered session data.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **Pandas**: Python data analysis library used for data manipulation.
- **Plotly**: A graphing library to create interactive charts.
- **Flask-Login**: User session management for Flask.
- **JavaScript Libraries**: Datatables for interactive table features.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any changes.

## License

This project is licensed under the MIT License.

---
