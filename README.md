# Savannah Shop - E-commerce Platform

[![Django CI/CD with Kubernetes](https://github.com/jafeth001/savannah-assessment/actions/workflows/django-k8s.yml/badge.svg)](https://github.com/jafeth001/savannah-assessment/actions/workflows/django-k8s.yml)

Savannah Shop is a Django-based e-commerce platform with OpenID Connect authentication, RESTful APIs, and integration with Africa's Talking for SMS notifications.

## Features

- **Customer Management**: Create and manage customer profiles
- **Product Catalog**: Organize products in categories with hierarchical structure
- **Order Processing**: Handle customer orders with detailed tracking
- **OpenID Connect Authentication**: Secure authentication via Auth0
- **SMS Notifications**: Automatic SMS notifications via Africa's Talking
- **Email Notifications**: HTML email templates for order updates
- **RESTful API**: Comprehensive API for all e-commerce operations
- **Docker Support**: Containerized deployment for easy scaling
- **Kubernetes Deployment**: Production-ready Kubernetes manifests
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## Technology Stack

- **Backend**: Django 5.2.6 with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: OpenID Connect (Auth0 integration)
- **SMS**: Africa's Talking API
- **Containerization**: Docker & Kubernetes
- **CI/CD**: GitHub Actions
- **WSGI Server**: Gunicorn

## Prerequisites

- Python 3.13
- pipenv
- Docker (for containerization)
- Kubernetes cluster (for production deployment)
- PostgreSQL (can be run locally or via Docker)

## Installation

### Local Development Setup

1. Clone the repository:
   git clone https://github.com/jafeth001/savannah-assessment.git cd savannah-assessment

2. Install dependencies using pipenv:
   pipenv install

3. Activate the virtual environment:
    pipenv shell

4. Set up the database:
    python manage.py migrate

5. Start the development server:
   python manage.py runserver


### Environment Variables

Create a `.env` file based on `.env.example` and configure the following variables:
- Database credentials
- Auth0 OIDC settings
- Africa's Talking API credentials
- Email configuration

## API Endpoints

### Customer Management
- `POST /shop/customer/` - Create a new customer
- `GET /shop/customer/` - List all customers
- `GET /shop/customer/{id}/` - Get customer details
- `PUT /shop/customer/{id}/` - Update customer information
- `DELETE /shop/customer/{id}/` - Delete a customer

### Product Management
- `POST /shop/product/` - Create a new product
- `GET /shop/product/` - List all products
- `GET /shop/product/{id}/` - Get product details
- `PUT /shop/product/{id}/` - Update product information
- `DELETE /shop/product/{id}/` - Delete a product

### Category Management
- `POST /shop/category/` - Create a new category
- `GET /shop/category/` - List all categories
- `GET /shop/category/{id}/` - Get category details
- `PUT /shop/category/{id}/` - Update category information
- `DELETE /shop/category/{id}/` - Delete a category

### Order Management
- `POST /shop/order/` - Create a new order
- `GET /shop/order/` - List all orders
- `GET /shop/order/{id}/` - Get order details
- `PUT /shop/order/{id}/` - Update order information
- `DELETE /shop/order/{id}/` - Delete an order

## Authentication

The API uses OpenID Connect for authentication with Auth0. To access protected endpoints:

1. Visit `/oidc/authenticate/` to initiate the authentication flow
2. Log in with your Auth0 credentials
3. After successful authentication, you can access protected endpoints

For API testing with tools like Postman:
1. Complete the authentication flow in a browser
2. Copy the session cookie
3. Use the cookie in your API requests

## Docker Deployment

1. Build the Docker image:
   docker build -t savannah-shop .

2. Run with Docker Compose:
   docker-compose up --build

## Kubernetes Deployment

1. Apply Kubernetes manifests:
   kubectl apply -f k8s

2. Update with new image:
   kubectl set image deployment/savannah-app savannah-app=<your-image>

## Testing

Run the test suite:
python manage.py test

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **Test Job**: Runs on every push/PR to main and develop branches
  - Sets up Python 3.13 environment
  - Installs dependencies
  - Runs unit tests with PostgreSQL service
  - Performs code quality checks with flake8

- **Build and Push Job**: Runs only on main branch
  - Builds Docker image
  - Pushes to DockerHub

- **Deploy Job**: Runs only on main branch after successful build
  - Configures AWS credentials
  - Updates kubeconfig for EKS cluster
  - Deploys to Kubernetes cluster

## Configuration

Key environment variables:
- [OIDC_RP_CLIENT_ID](file://C:\Users\jafeth\Desktop\savannah-assessment\savannah\settings.py#L154-L154) - OIDC client ID from Auth0
- [OIDC_RP_CLIENT_SECRET](file://C:\Users\jafeth\Desktop\savannah-assessment\savannah\settings.py#L155-L155) - OIDC client secret from Auth0
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` - Database credentials
- [AFRICASTALKING_API_KEY](file://C:\Users\jafeth\Desktop\savannah-assessment\savannah\settings.py#L169-L169) - Africa's Talking API key

See `.env.example` for a complete list of configuration options.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on the GitHub repository.




