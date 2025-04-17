# Project Kickoff Prompt (Flexible Version)

## How to Use This Prompt

This prompt is designed to guide an AI assistant in setting up a project based on existing code with its own folder structure. This prompt assumes you have already:

1. Created or cloned your project directory
2. Copied the template files and rule directories
3. The project has its own existing folder structure that should be preserved

To use this prompt effectively:

1. **Copy this entire prompt** to your conversation with an AI assistant
2. **Replace the placeholder** at the bottom with your specific information:
   - `[PROJECT_PURPOSE]`: A brief description of what the project will do
   - Note: The project name will be derived from the current directory name
3. **Share with the AI assistant** to guide them through setting up your project
4. **Review the AI's work** against the verification checklist

The AI will use the templates in `.cursor/templates/` to populate your project with the necessary files and configurations while preserving the existing folder structure. For more detailed information about the template system, refer to `.cursor/templates/TEMPLATE_SYSTEM.md`.

## Project Initialization Instructions

I'm working with an existing project directory that has its own folder structure. I've copied the template files and rule directories. Now I need your assistance to set up the project content according to our established standards while preserving the existing structure. Please help me create a well-structured, maintainable project that follows our quality guidelines.

**IMPORTANT**: 
- I've already created/cloned the project directory and copied the template files
- Please work within the existing folder structure and DO NOT create new directories that would conflict with the existing structure
- Focus on adding documentation and configuration files without changing the existing structure

## Standards and Templates

This project must adhere to the standards defined in the templates. Key files to reference:

1. **Template System Documentation**: `.cursor/templates/TEMPLATE_SYSTEM.md`
2. **Project Structure**: Adapt the templates in `.cursor/templates/` to work with the existing structure

## Memory Files Structure

The project should use a hierarchical knowledge base with these key files, adapted to the existing structure:

1. **Core Files (Required):**
   - Create `docs/product_requirement_docs.md` if it doesn't exist
   - Create `docs/architecture.md` if it doesn't exist
   - Create `docs/technical.md` if it doesn't exist
   - Create `tasks/tasks_plan.md` if it doesn't exist
   - Create `tasks/active_context.md` if it doesn't exist
   - Create `docs/error-documentation.md` if it doesn't exist
   - Create `docs/lessons-learned.md` if it doesn't exist

2. **Context Files (Optional):**
   - Create `docs/literature/` directory if it doesn't exist
   - Create `tasks/rfc/` directory if it doesn't exist

## Configuration Files

1. **pyproject.toml**: Add or update if appropriate for the project
2. **pre-commit hooks**: Add or update if appropriate for the project
3. **DEVELOPMENT.md**: Create if it doesn't exist, including the Project Quality Gates section
4. **GitHub Actions**: Add workflows if appropriate for the project

## Implementation Process

1. **First, analyze the existing structure**: Understand the current organization
2. **Adapt our standards**: Determine how to apply our standards to the existing structure
3. **Add documentation**: Create or update documentation files
4. **Configure development tools**: Set up linting, testing, and CI/CD as appropriate
5. **Document**: Add comprehensive documentation

## Quality Standards

1. **Code Quality**: Follow PEP 8, use type hints, and adhere to our linting standards
2. **Testing**: Implement unit tests with pytest, aiming for at least 80% coverage
3. **Documentation**: Use Google-style docstrings for all public APIs
4. **Security**: Follow secure coding practices, no hardcoded secrets

## Verification Checklist

Before considering the project setup complete, verify:

- [ ] Documentation files are created or updated
- [ ] Configuration files are added or updated as appropriate
- [ ] README.md includes setup and usage instructions
- [ ] The existing structure is preserved and respected

## Additional Instructions

- Always explain your reasoning for significant implementation choices
- If you need to deviate from standards for a specific reason, explain why
- Prioritize maintainability and readability over clever or complex solutions
- Follow the KISS, YAGNI, and DRY principles
- Adapt our standards to work with the existing structure rather than forcing the existing structure to conform to our standards

Now, please help me set up this project according to these guidelines.
The project's purpose is: [PROJECT_PURPOSE]
