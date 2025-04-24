# Python FastAPI Boilerplate

A modern, scalable FastAPI boilerplate with support for both SQL and MongoDB databases, featuring a clean architecture and modular design.

## Project Structure

```
src/
├── auth/                 # Authentication module
├── aws/                  # AWS services integration
├── common/               # Shared utilities and base classes
│   ├── base_entity.py
│   ├── base_repository.py
│   ├── base_response.py
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── message.py
│   ├── mongo_database.py
│   ├── mongo_repository.py
│   ├── rabbitmq_client.py
│   ├── sql_database.py
│   └── sqlalchemy_repository.py
├── email/                # Email service module
├── inventory/            # Inventory management module
├── payments/             # Payment processing module
│   ├── api/             # API endpoints
│   ├── domain/          # Business logic
│   ├── dtos/            # Data Transfer Objects
│   ├── repositories/    # Data access layer
│   └── services/        # Service layer
├── sales/                # Sales module
└── main.py              # Application entry point

tests/                   # Test directory
```

## Features

- **Dual Database Support**: Built-in support for both SQL (via SQLAlchemy) and MongoDB (via Motor)
- **Clean Architecture**: Modular design following domain-driven principles
- **Common Utilities**: Shared components for logging, configuration, and messaging
- **RabbitMQ Integration**: Message queue support for async operations
- **AWS Integration**: Ready-to-use AWS services integration
- **Email Service**: Dedicated email handling module
- **Payment Processing**: Comprehensive payment module with separate layers for API, domain, and data access
- **Inventory Management**: Dedicated inventory tracking system
- **Sales Module**: Sales processing and management

## Dependencies

- python-dotenv: Environment variable management
- motor: MongoDB async driver
- SQLAlchemy: SQL toolkit and ORM

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment variables
4. Run the application:
   ```bash
   python src/main.py
   ```

## Architecture

The project follows a clean architecture pattern with clear separation of concerns:

- **API Layer**: Handles HTTP requests and responses
- **Domain Layer**: Contains business logic and entities
- **Service Layer**: Implements business operations
- **Repository Layer**: Manages data access
- **Common Layer**: Provides shared utilities and base classes

## Testing

The project includes a dedicated test directory for unit and integration tests. Run tests using your preferred testing framework.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
