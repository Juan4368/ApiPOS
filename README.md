# WhatsApp Webhook Clean Architecture

This project implements a webhook integration with WhatsApp using Clean Architecture principles. The structure is designed to separate concerns and promote maintainability and testability.

## Project Structure

```
whatsapp-webhook-clean-arch
├── src
│   └── whatsapp_webhook
│       ├── app
│       │   ├── __init__.py
│       │   └── main.py
│       ├── model
│       │   ├── __init__.py
│       │   └── dto.py
│       ├── domain
│       │   ├── __init__.py
│       │   ├── entities.py
│       │   └── repositories.py
│       ├── service
│       │   ├── __init__.py
│       │   └── webhook_service.py
│       └── infrastructure
│           ├── __init__.py
│           ├── whatsapp_client.py
│           ├── repository_impl.py
│           └── web
│               ├── __init__.py
│               └── webhook_controller.py
├── tests
│   ├── conftest.py
│   └── test_webhook.py
├── requirements.txt
├── pyproject.toml
├── setup.cfg
├── .gitignore
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd whatsapp-webhook-clean-arch
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python -m src.whatsapp_webhook.app.main
   ```

## Usage

The application listens for incoming webhook requests from WhatsApp. Ensure that your WhatsApp API is configured to send messages to the correct endpoint.

## Testing

To run the tests, use the following command:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.# BotPedidos
# ProyectoBasePOS
