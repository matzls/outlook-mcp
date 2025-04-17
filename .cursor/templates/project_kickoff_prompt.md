# Project Kickoff Prompt

## How to Use This Prompt

This prompt is designed to guide an AI assistant in setting up a new Python project according to your established standards. This prompt assumes you have already:

1. Created your project directory
2. Copied the template files and rule directories
3. Set up the basic folder structure

To use this prompt effectively:

1. **Copy this entire prompt** to your conversation with an AI assistant
2. **Replace the placeholder** at the bottom with your specific information:
   - `[PROJECT_PURPOSE]`: A brief description of what the project will do
   - Note: The project name will be derived from the current directory name
3. **Share with the AI assistant** to guide them through setting up your project
4. **Review the AI's work** against the verification checklist

The AI will use the templates in `.cursor/templates/` to populate your project with the necessary files and configurations. For more detailed information about the template system, refer to `.cursor/templates/TEMPLATE_SYSTEM.md`.

## Project Initialization Instructions

I've created a new Python project directory and copied the template files. Now I need your assistance to set up the project content according to our established standards. Please help me create a well-structured, maintainable project that follows all our quality guidelines.

**IMPORTANT**: I've already created the project directory and copied the template files. Please set up the project in the current directory without creating a new subdirectory.

## Standards and Templates

This project must adhere to the standards defined in the templates. Key files to reference:

1. **Template System Documentation**: `.cursor/templates/TEMPLATE_SYSTEM.md`
2. **Project Structure**: Follow the templates in `.cursor/templates/`

## Required Project Structure

Please set up a project with the following structure:

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
│   ├── product_requirement_docs.md  # PRD defining project purpose and requirements
│   ├── architecture.md              # System architecture document
│   ├── technical.md                 # Technical specifications
│   └── literature/                  # Research papers and literature surveys
├── tasks/
│   ├── tasks_plan.md                # Task backlog and project progress
│   ├── active_context.md            # Current development focus
│   └── rfc/                         # Request for Comments for specific functionalities
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── test.yml
├── .cursor/
│   └── rules/
│       ├── error-documentation.mdc  # Reusable fixes for known issues
│       └── lessons-learned.mdc      # Project-specific learning journal
├── .gitignore
├── pyproject.toml
├── README.md
├── DEVELOPMENT.md
├── .pre-commit-config.yaml
└── [additional files as needed]
```

### Memory Files Structure

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

## Configuration Files

1. **pyproject.toml**: Use the standardized configuration from `master_cursor_rules/testing.mdc`
2. **pre-commit hooks**: Use the standardized configuration from `master_cursor_rules/testing.mdc`
3. **DEVELOPMENT.md**: Include the Project Quality Gates section with advanced testing standards set to "Not Yet Activated"
4. **GitHub Actions**: Set up workflows for linting and testing

## Implementation Process

1. **First, analyze the requirements**: Understand what the project needs to accomplish
2. **Create the basic structure**: Set up the directory structure and initial files
3. **Configure development tools**: Set up linting, testing, and CI/CD
4. **Implement core functionality**: Start with minimal viable implementation
5. **Add tests**: Create unit tests for the core functionality
6. **Document**: Add comprehensive documentation

## Quality Standards

1. **Code Quality**: Follow PEP 8, use type hints, and adhere to our linting standards
2. **Testing**: Implement unit tests with pytest, aiming for at least 80% coverage
3. **Documentation**: Use Google-style docstrings for all public APIs
4. **Security**: Follow secure coding practices, no hardcoded secrets

## Verification Checklist

Before considering the project setup complete, verify:

- [ ] Project structure follows the standard layout
- [ ] pyproject.toml includes all required configurations
- [ ] Pre-commit hooks are properly configured
- [ ] DEVELOPMENT.md includes Quality Gates section
- [ ] README.md includes setup and usage instructions
- [ ] Basic tests directory is created with conftest.py
- [ ] GitHub Actions workflows are set up

## Additional Instructions

- Always explain your reasoning for significant implementation choices
- If you need to deviate from standards for a specific reason, explain why
- Prioritize maintainability and readability over clever or complex solutions
- Follow the KISS, YAGNI, and DRY principles

Now, please help me set up this project according to these guidelines.
The project's purpose is: [PROJECT_PURPOSE]
