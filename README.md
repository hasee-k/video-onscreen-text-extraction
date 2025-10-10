
# Project Title
A brief description of your project.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

---


## Setup and Installation



### 1. Create and activate a virtual environment

A virtual environment is recommended to keep the dependencies required by different projects separate.

#### On macOS and Linux:

```bash
# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

Your terminal prompt should now be prefixed with `(venv)`.

#### On Windows:

```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

Your terminal prompt should now be prefixed with `(venv)`.

---

### 2. Install the required packages

With your virtual environment activated, install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

### 3. Create the environment file

This project requires a `.env` file in the root directory to store environment variables.

1. Create a new file named `.env`.
2. Open the file and add your Google API Key like this:

```env
GOOGLE_API_KEY="your_api_key_here"
```

Replace `"your_api_key_here"` with your actual Google API key.

---

## Running the Application

Once you have completed the setup steps, you can run the application using the following command:

```bash
python main.py
```

---

## Deactivating the Virtual Environment

When you are finished working on the project, you can deactivate the virtual environment by simply running:

```bash
deactivate
```

