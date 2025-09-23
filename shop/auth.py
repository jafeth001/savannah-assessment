import hashlib
import re
from django.contrib.auth.models import User
from .models import Customer


def generate_username(email):
    """
    Generate a username from email address
    """
    # Clean the email address to create a valid username
    username = re.sub(r'[^a-zA-Z0-9_@+.-]', '', email)
    # Limit to 150 characters
    username = username[:150]
    return username


def create_customer_from_claims(claims):
    """
    Create a Customer instance from OIDC claims
    """
    # Extract information from claims
    email = claims.get('email', '')
    first_name = claims.get('given_name', '')
    last_name = claims.get('family_name', '')

    # Use a placeholder for phone if not provided
    phone = claims.get('phone_number', 'N/A')

    # Check if customer already exists
    customer, created = Customer.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
        }
    )

    return customer


class OIDCCustomerBackend:
    """
    Custom OIDC Authentication Backend that links OIDC users with Customer model
    """

    def create_user(self, claims):
        """
        Create a new User and Customer from OIDC claims
        """
        # Create Django User
        user = User.objects.create_user(
            username=generate_username(claims.get('email')),
            email=claims.get('email'),
            first_name=claims.get('given_name', ''),
            last_name=claims.get('family_name', ''),
        )

        # Create Customer
        customer = create_customer_from_claims(claims)

        # Link User to Customer
        user.customer = customer
        user.save()

        return user

    def update_user(self, user, claims):
        """
        Update existing user with new claims from OIDC
        """
        user.email = claims.get('email', user.email)
        user.first_name = claims.get('given_name', user.first_name)
        user.last_name = claims.get('family_name', user.last_name)
        user.save()

        # Update customer information if exists
        if hasattr(user, 'customer'):
            customer = user.customer
            customer.email = claims.get('email', customer.email)
            customer.first_name = claims.get('given_name', customer.first_name)
            customer.last_name = claims.get('family_name', customer.last_name)
            customer.phone = claims.get('phone_number', customer.phone)
            customer.save()

        return user
