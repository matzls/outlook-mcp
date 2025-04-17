# Project Templates System

This document provides comprehensive guidance on using our Python project templates system.

## Overview

This templates system helps set up standardized Python projects with consistent structure, configuration, and quality standards. It's designed for both AI assistants and human developers.

## Available Templates

- `pyproject.toml`: Project configuration with standardized settings
- `pre-commit-config.yaml`: Pre-commit hooks configuration
- `DEVELOPMENT.md`: Development guide with Project Quality Gates
- `README.md`: Project overview template
- `main.py`: Template for the main module
- `conftest.py`: Template for pytest fixtures
- `test_main.py`: Template for main module tests
- `init.py`: Template for package __init__.py
- `gitignore`: Template for .gitignore
- `github_workflows_lint.yml`: GitHub Actions linting workflow
- `github_workflows_test.yml`: GitHub Actions testing workflow

## Project Setup Methods

### Method 1: Using AI Assistant (Recommended)

1. **Copy the project_kickoff_prompt.md** to your conversation with an AI assistant
2. **Replace the placeholders** at the bottom with your specific information:
   - `[PROJECT_NAME]`: The name of your new project (e.g., "data_analyzer")
   - `[PROJECT_PURPOSE]`: A brief description of what the project will do
3. The AI will set up your project structure and files according to our standards

### Method 2: Manual Setup

1. Follow the step-by-step instructions below to create your project structure
2. Copy templates from this directory to your new project
3. Replace placeholders with your project-specific values

## Project Structure

```
project_name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       └── [additional modules as needed]
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── [test files as needed]
├── docs/
│   ├── product_requirement_docs.md
│   ├── architecture.md
│   ├── technical.md
│   └── literature/
├── tasks/
│   ├── tasks_plan.md
│   ├── active_context.md
│   └── rfc/
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── test.yml
├── .cursor/
│   └── rules/
│       ├── error-documentation.mdc
│       └── lessons-learned.mdc
├── .gitignore
├── pyproject.toml
├── README.md
├── DEVELOPMENT.md
└── .pre-commit-config.yaml
```

## Placeholders

The following placeholders are used in the templates:

- `{{project_name}}`: The name of your project
- `{{project_description}}`: A brief description of your project
- `{{author_name}}`: Your name
- `{{author_email}}`: Your email
- `{{github_username}}`: Your GitHub username

## Quality Standards

These templates enforce the following standards:

1. **Code Quality**: PEP 8, type hints, and comprehensive linting
2. **Testing**: Unit tests with pytest, aiming for at least 85% coverage
3. **Documentation**: Google-style docstrings for all public APIs
4. **Security**: Secure coding practices, no hardcoded secrets
5. **Project Structure**: Consistent directory structure and file organization

## Project Quality Gates

The templates include a Project Quality Gates section in the `DEVELOPMENT.md` file. This section indicates whether advanced testing standards are activated for the project.

By default, advanced testing standards are set to "Not Yet Activated". When the project reaches an appropriate stage, this can be changed to "ACTIVATED" to enforce stricter testing standards.

## Memory Files Structure

The project uses a hierarchical knowledge base with these key files:

1. **Core Files (Required):**
   - `docs/product_requirement_docs.md`: Defines project purpose, problems, requirements, and goals
   - `docs/architecture.md`: Outlines system design and component relationships
   - `docs/technical.md`: Details development environment and technical decisions
   - `tasks/tasks_plan.md`: Tracks project progress and known issues
   - `tasks/active_context.md`: Captures current development focus
   - `.cursor/rules/error-documentation.mdc`: Documents reusable fixes
   - `.cursor/rules/lessons-learned.mdc`: Project-specific learning journal

2. **Context Files (Optional):**
   - `docs/literature/`: Research papers and literature surveys
   - `tasks/rfc/`: Detailed specifications for specific functionalities

## Step-by-Step Manual Setup Guide

### 1. Project Structure Creation

Create the directory structure as shown above.

### 2. Configuration Files

#### 2.1 pyproject.toml

Create a `pyproject.toml` file in the project root using the template.
Replace all placeholders with your project-specific values.

#### 2.2 Pre-commit Configuration

Create a `.pre-commit-config.yaml` file in the project root using the template.

#### 2.3 Git Configuration

Create a `.gitignore` file in the project root using the template.

#### 2.4 GitHub Actions

Create the workflow files in `.github/workflows/` using the templates.

### 3. Documentation Files

#### 3.1 README.md

Create a `README.md` file in the project root using the template.
Replace all placeholders with your project-specific values.

#### 3.2 DEVELOPMENT.md

Create a `DEVELOPMENT.md` file in the project root using the template.
Replace all placeholders with your project-specific values.

### 4. Source Code

#### 4.1 Main Module

Create a `src/project_name/main.py` file using the template.
Replace `{{project_name}}` with your project name.

#### 4.2 Package Initialization

Create a `src/project_name/__init__.py` file with the template content.

### 5. Tests

#### 5.1 Test Configuration

Create a `tests/conftest.py` file using the template.

#### 5.2 Test Files

Create a `tests/test_main.py` file using the template.

### 6. Development Environment Setup

1. Create a virtual environment
2. Install the package in development mode
3. Set up pre-commit hooks

### 7. Verification

Verify your project setup by running linting checks and tests.
