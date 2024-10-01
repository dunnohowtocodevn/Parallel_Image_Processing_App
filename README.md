

```markdown
# Flask Image Processing App with Redis and Locust Testing

This project is a Flask web application that allows users to upload images and perform actions (such as grayscale, rotate, etc.) on the uploaded images. The processed images are stored in an SQLite database, and the processing tasks are queued using Redis Queue (RQ) for better performance. Locust is used to simulate concurrent users sending requests to the application.

## Features
- Upload images for processing.
- Choose from actions like `grayscale`, `rotate`, etc.
- Store original and processed images in SQLite as BLOBs.
- Redis Queue is used to handle image processing asynchronously.
- Locust is used for load testing by simulating 1000 users concurrently.

## Table of Contents
1. [Installation](#installation)
2. [Virtual Environment](#virtual-environment)
3. [Cloning the Repository](#cloning-the-repository)
4. [Running the Application](#running-the-application)
5. [Testing with Locust](#testing-with-locust)
6. [Application Routes](#application-routes)
7. [Project Structure](#project-structure)
```
## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/dunnohowtocodevn/Parallel_Image_Processing_App.git
   cd your-repository
   ```

2. **Set up a virtual environment:**

   To create and activate a virtual environment, use the following commands:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```

3. **Install the required libraries:**

   After activating the virtual environment, install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Redis:**

   - On macOS: 
     ```bash
     brew install redis
     ```
   - On Ubuntu: 
     ```bash
     sudo apt-get install redis-server
     ```
   - On Windows: 
     Follow instructions [here](https://github.com/MicrosoftArchive/redis/releases) to install Redis.

## Virtual Environment

The project uses a virtual environment to manage dependencies. Make sure you have Python 3 installed. To activate the environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
  
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

To deactivate the virtual environment, simply type:

```bash
deactivate
```

## Running the Application

1. **Start Redis:**

   Redis should be running before you start the Flask app. Run the following command:

   ```bash
   redis-server
   ```

2. **Start the Flask App:**

   To start the application, use the following command in your terminal:

   ```bash
   python app.py
   ```

   The application should now be accessible at `http://localhost:5000`.

## Testing with Locust

1. **Install Locust:**

   ```bash
   pip install locust
   ```

2. **Run Locust:**

   To start load testing with Locust, use the following command:

   ```bash
   locust --host=http://localhost:5000
   ```

   Then open the Locust web interface at `http://localhost:8089` and start the test by setting the number of users and spawn rate.

## Application Routes

Here are the main routes in the application:

- `GET /`: The homepage where users can upload an image.
- `POST /upload`: Handles image upload and saves it to the SQLite database as a BLOB.
- `POST /process/<int:image_id>`: Handles image processing (grayscale, rotate, etc.) and enqueues tasks to Redis Queue.
- `GET /view/<int:image_id>`: Displays the original and processed images.
- `GET /image/<int:image_id>/<image_type>`: Retrieves original or processed images from the database.

## Project Structure

```plaintext
.
├── app.py                    # Main Flask application
├── tasks.py                  # Image processing tasks
├── worker.py                 # Redis queue worker setup
├── requirements.txt          # List of dependencies
├── static/
│   └── uploads/              # Folder for storing images temporarily
├── templates/
│   ├── index.html            # Upload page
│   ├── process.html          # Image processing page
│   └── view.html             # Display original and processed images
├── locustfile.py             # Locust script for load testing
├── test_img/                 # Folder containing images for Locust testing
└── README.md                 # Project documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
