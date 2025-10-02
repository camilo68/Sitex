# GasFleetManager

## Overview

GasFleetManager is a Flask-based fuel management system (SiteX) designed for managing fuel tanks, employee operations, and fuel measurements. The application provides a complete solution for tracking fuel levels, recording discharge operations, managing employee access, and maintaining historical records of all fuel-related activities. It features a role-based authentication system with different access levels for administrators, supervisors, and regular users.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask Application Factory Pattern**: The application uses a factory pattern with modular blueprints for organized route management
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy for database operations and migrations
- **Authentication**: Flask-Login integrated with bcrypt for secure password hashing and session management
- **Form Handling**: WTForms with Flask-WTF for form validation and CSRF protection

### Database Design
- **Employee Management**: Comprehensive employee records with role-based access control (admin, supervisor, user)
- **Tank Management**: Fuel tank specifications including capacity, dimensions, and current fuel levels
- **Measurement Tracking**: Historical records of fuel measurements with different operation types (routine, loading, discharge)
- **Operational Records**: Detailed logging of discharge operations with safety equipment verification

### Frontend Architecture
- **Template Engine**: Jinja2 templates with a base template inheritance system
- **UI Framework**: Bootstrap 5 for responsive design and component styling
- **Navigation**: Role-based navigation with dropdown menus for different user types
- **Forms**: Dynamic form rendering with server-side validation and error display

### Security Implementation
- **CSRF Protection**: Implemented across all forms using Flask-WTF
- **Password Security**: Bcrypt hashing for password storage and verification
- **Session Management**: Flask-Login for secure user session handling
- **Role-Based Access**: Multi-tier permission system with admin, supervisor, and user roles

### Application Structure
- **Modular Blueprints**: Separate blueprints for authentication, dashboard, and measurement operations
- **Configuration Management**: Environment-based configuration with database connection pooling
- **Database Migrations**: Flask-Migrate for schema version control and updates

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework with SQLAlchemy ORM integration
- **Flask-Login**: User session management and authentication
- **Flask-Migrate**: Database migration management
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **bcrypt**: Password hashing and verification

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive UI components
- **Bootstrap Icons**: Icon library for user interface elements

### Database Requirements
- **SQLAlchemy**: Database abstraction layer with support for multiple database engines
- **Database Connection**: Configured to support PostgreSQL with connection pooling and automatic reconnection

### Development Tools
- **Python Environment**: Requires Python with Flask ecosystem packages
- **Database Migration**: Flask-Migrate for schema management and version control