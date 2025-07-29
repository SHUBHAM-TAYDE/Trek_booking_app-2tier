# Trek Booking Application

This is a two-tier web application for booking treks, built with Flask (Python) for the backend and HTML, Tailwind CSS, and JavaScript for the frontend. It's designed to be a foundational project for practicing DevOps deployment strategies.

## Table of Contents

* [Features](#features)
* [Architecture](#architecture)
* [Prerequisites](#prerequisites)
* [Setup and Installation](#setup-and-installation)
* [Running the Application](#running-the-application)
* [DevOps Considerations](#devops-considerations)
* [Project Structure](#project-structure)

## Features

* **Home Page:** Welcoming landing page with featured treks.
* **Trek Listings:** Browse all available treks with brief details.
* **Trek Detail Pages:** Detailed information about each trek, including description, price, and offers.
* **Shopping Cart:** Add treks to a cart, update quantities, and remove items.
* **Booking/Checkout:** A simplified process to confirm bookings from the cart.
* **Offers Page:** Displays treks with special discounts or promotions.
* **About Us & Contact Us:** Essential informational pages.
* **User Authentication:** Basic user registration and login functionality.

## Architecture

This application follows a **two-tier architecture**:

1.  **Backend (Tier 1 - Server-side):**
    * **Technology:** Flask (Python)
    * **Role:** Handles all business logic, data storage (in-memory for this demo), API endpoints (for cart, booking, authentication), and serves the HTML pages.
    * **Data Storage:** For demonstration purposes, data (users, treks, cart, bookings) is stored in Python dictionaries in memory. This means data will reset every time the Flask server restarts.

2.  **Frontend (Tier 2 - Client-side):**
    * **Technology:** HTML, Tailwind CSS, JavaScript
    * **Role:** Provides the user interface, handles user interactions, and communicates with the backend via RESTful API calls to fetch and send data.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
* **pip**: Python's package installer (usually comes with Python).

## Setup and Installation

Follow these steps to get the application running on your local machine:

1.  **Clone or Download the Project:**
    If you have the project files, ensure they are organized as described in the "Project Structure" section below.

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

3.  **Create a Virtual Environment:**
    It is highly recommended to use a Python virtual environment to manage dependencies and avoid conflicts with your system's Python installation.
    Open your terminal or command prompt and navigate to the root directory of your project (`trek_booking_app/`).

    ```bash
    python3 -m venv venv
    ```

4.  **Activate the Virtual Environment:**
    * **On Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows (Command Prompt):**
        ```cmd
        venv\Scripts\activate.bat
        ```
    * **On Windows (PowerShell):**
        ```powershell
        venv\Scripts\Activate.ps1
        ```
    Your terminal prompt should change to indicate the virtual environment is active (e.g., `(venv) your_username@your_machine:~/trek_booking_app$`).

5.  **Install Dependencies:**
    With the virtual environment activated, install the required Python packages:

    ```bash
    pip install Flask Flask-Cors
    ```

## Running the Application

1.  **Start the Flask Backend:**
    Ensure your virtual environment is activated (step 3 above). Then, from the `trek_booking_app/` directory, run:

    ```bash
    python app.py
    ```
    You will see output indicating that the Flask development server is running, typically on `http://127.0.0.1:5000/`.

2.  **Access the Application:**
    Open your web browser and navigate to the address provided by the Flask server (e.g., `http://127.0.0.1:5000/`).

    You can now interact with the application:
    * Browse treks.
    * Add treks to your cart.
    * Register a new user and log in.
    * Proceed to booking.

    **Note:** Since the data is in-memory, any registered users, cart items, or bookings will be lost when you stop and restart the `app.py` server.
