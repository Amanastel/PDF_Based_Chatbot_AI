# PdfChat

## Introduction
This is a Django project that demonstrates how to create a custom user model and define related models for user profiles, PDF documents, and chat messages.
## Deplolyed App
https://deployed-site.whatever


## Features
List out the key features of your application.

- Custom user model with extended fields (phone and address).
- User profiles associated with each user.
- PDF documents uploaded and associated with users.
- Chat messages with timestamps.

## Getting Started



## design decisions or assumptions
List your design desissions & assumptions

## Installation & Getting started
Detailed instructions on how to install, configure, and get the project running.

```bash
1. Clone the repository: `git clone https://github.com/amanastel/LLMDjango.git`
2. Navigate to the project directory: `cd LLMDjango`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Apply database migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`
```

## Usage
Provide instructions and examples on how to use your project.

```bash
# Example
```

Include screenshots as necessary.

## APIs Used
1. Create a superuser to access the admin panel: `python manage.py createsuperuser`
2. Start the development server: `python manage.py runserver`
3. Access the admin panel at: `http://localhost:8000/admin/`
4. Use the admin panel to manage users, profiles, PDF documents, and chat messages.


## API Endpoints
- User Registration: `POST /api/register/`
- User Login: `POST /api/login/`
- User Profile: `GET /api/profile/`
- Upload PDF Document: `POST /api/upload-pdf/`
- List PDF Documents: `GET /api/pdf-documents/`
- Create Chat Message: `POST /api/chat/create/`
- List Chat Messages: `GET /api/chat/list/`

## Custom User Serializer

You can find the `CustomUserSerializer` in the `serializers.py` file under the `llmApp` app directory. This serializer is used for user registration and login.


## Models

- `CustomProfile`: Represents user profiles with extended fields (phone and address).
- `PDFDocument`: Represents uploaded PDF documents associated with users.
- `ChatMessage`: Represents chat messages with timestamps.


## Technology Stack
List and provide a brief overview of the technologies used in the project.

- Django
- Python
- Langchain
- MySql
- Vue



## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
