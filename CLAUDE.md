# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Liquid Vanilla is a full-stack recipe management web application built with:
- **Backend**: FastAPI (Python) with MongoDB for data storage
- **Frontend**: Vue 3 with TypeScript, Vite, Pinia for state management, and Tailwind CSS
- **Architecture**: RESTful API with separate frontend and backend codebases

## Common Development Commands

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload  # Development server on port 8000
python -m pytest                # Run tests
python -m pytest tests/test_recipe.py  # Run specific test file
python -m pytest --cov=src      # Run tests with coverage
```

### Frontend (Vue 3)
```bash
cd frontend
npm install
npm run dev         # Development server on port 5173
npm run build       # Production build
npm run type-check  # TypeScript type checking
npm run lint        # ESLint linting with auto-fix
npm run format      # Prettier formatting
npm run test:unit   # Vitest unit tests
npm run preview     # Preview production build
```

## Database Setup

- **Database**: MongoDB (local or remote)
- **Configuration**: Environment variables in `.env` file (see `.env.example`)
- **Connection**: Configured in `backend/src/config.py` and `backend/src/database.py`
- **Database Name**: `RecipeDB` (configurable via `MONGO_DATABASE` env var)

Required environment variables:
- `MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_DATABASE`

## Architecture Overview

### Backend Structure
- **Entry Point**: `backend/src/main.py` - FastAPI application setup with CORS and router registration
- **Configuration**: `backend/src/config.py` - Settings management with environment variables
- **Database**: `backend/src/database.py` - MongoDB connection and database utilities
- **API Routes**: 
  - `backend/src/recipes/routers.py` - Recipe CRUD operations
  - `backend/src/tags/routers.py` - Tag management operations
- **Models**: 
  - `backend/src/recipes/models.py` - Recipe data models with Pydantic validation
  - `backend/src/tags/models.py` - Tag data models
- **Schemas**: Request/response schemas for API validation
- **Base URL**: `/api/v1` for all API endpoints

### Frontend Structure
- **Entry Point**: `frontend/src/main.ts` - Vue app initialization with Pinia and router
- **State Management**: Pinia stores in `frontend/src/stores/`
  - `recipeStore.ts` - Recipe data, pagination, search, and filtering
  - `tagStore.ts` - Tag data management
- **Components**: Vue components in `frontend/src/components/`
  - `RecipeList.vue` - Recipe display with infinite scroll
  - `SearchBar.vue` - Search functionality
  - `NavigationBar.vue` - Navigation component
- **Services**: API communication layer
  - `recipeService.ts` - Recipe API calls
  - `tagService.ts` - Tag API calls
- **Routing**: Vue Router configuration for SPA navigation

## Key Features

### Recipe Management
- CRUD operations for recipes with rich metadata (title, rating, tags, ingredients, instructions)
- Image URL templating for different formats (crop-360x240, etc.)
- Pagination support (20 recipes per page)
- Full-text search functionality
- Tag-based filtering with multiple tag selection

### Tag System
- Tag management with CRUD operations
- Recipe filtering by tags
- Tag usage statistics and sorting by popularity

### Frontend Features
- Infinite scroll for recipe loading
- Real-time search with debouncing
- Responsive design with Tailwind CSS
- TypeScript for type safety
- Component-based architecture
- Dark/Light mode support with theme persistence

## UI/UX Design Requirements

### Dark and Light Mode Support
**CRITICAL**: All UI components and features must support both dark and light mode themes:

- **Implementation**: Use Tailwind CSS dark mode classes (e.g., `dark:bg-secondary`, `dark:text-light`)
- **Theme Switching**: Implement toggle functionality with persistent user preference
- **Color Scheme**: Follow the established color palette defined in `frontend/src/assets/main.css`:
  - Light mode: `bg-light`, `text-dark`, `bg-secondary-light`
  - Dark mode: `dark:bg-secondary`, `dark:text-light`, `dark:bg-primary`
- **Gold Theme**: Use gold accent colors (`bg-gold-light dark:bg-gold`) for interactive elements
- **Accessibility**: Ensure proper contrast ratios in both themes
- **Consistency**: All new components must have matching dark/light mode styling

### Component Styling Guidelines
- **No Rounded Edges**: Use square/straight edges for buttons and containers (avoid `rounded` classes)
- **Gold Accent**: Use gold colors for primary actions and selected states
- **Mobile-First**: Design components to be mobile-friendly and responsive
- **Hover States**: Implement proper hover feedback with `cursor-pointer` and color transitions

## Testing

### Backend Tests
- **Framework**: pytest with pytest-asyncio
- **Test Configuration**: `backend/pytest.ini` with `pythonpath = src`
- **Test Files**: Located in `backend/tests/`
- **Coverage**: Available via `pytest-cov`
- **Mocking**: Uses `mongomock` for database testing

### Frontend Tests
- **Framework**: Vitest with Vue Test Utils
- **Test Command**: `npm run test:unit`
- **Configuration**: `frontend/vitest.config.ts`

## Development Workflow

1. **Backend Development**: Start with `uvicorn src.main:app --reload` from backend directory
2. **Frontend Development**: Start with `npm run dev` from frontend directory
3. **Database**: Ensure MongoDB is running and configured
4. **Testing**: Run both backend (`pytest`) and frontend (`npm run test:unit`) tests
5. **Linting**: Use `npm run lint` for frontend code quality
6. **Type Checking**: Use `npm run type-check` for TypeScript validation

## API Endpoints

Base URL: `http://localhost:8000/api/v1`

### Recipes
- `GET /recipes` - Get recipes with pagination, search, and tag filtering
- `POST /recipes` - Create new recipe
- `GET /recipes/{id}` - Get recipe by ID
- `PUT /recipes/{id}` - Update recipe
- `DELETE /recipes/{id}` - Delete recipe

### Tags
- `GET /tags` - Get all tags (sorted by usage count)
- `POST /tags` - Create new tag
- `GET /tags/{id}` - Get tag by ID
- `PUT /tags/{id}` - Update tag
- `DELETE /tags/{id}` - Delete tag

## Code Quality and Development Practices

### Code Quality Tools
```bash
# Install and setup pre-commit hooks
pip install pre-commit
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files

# Manual tool execution
black backend/src/ backend/tests/  # Format code
isort backend/src/ backend/tests/  # Sort imports
flake8 backend/src/ backend/tests/ # Lint code
mypy backend/src/                  # Type checking
```

### Code Style Guidelines

#### Python Standards (Backend)
- Target Python 3.9+
- Adhere to PEP 8 guidelines
- Use modern type hints: `dict[K, V]`, `list[T]`, `set[T]`, `tuple[T, ...]`
- Avoid importing `Dict`, `List`, `Set`, `Tuple` from typing unless necessary
- Only use typing module for advanced types like `Union`, `Optional`, `Protocol`, etc.
- Utilize clear and descriptive variable and function names
- Add comments for complex logic or non-obvious implementations

#### Documentation Standards
Add reStructuredText (reST) format docstrings to all functions:

```python
"""
This is a reST style.

:param param1: this is a first param
:param param2: this is a second param
:returns: this is a description of what is returned
:raises keyError: raises an exception
"""
```

#### TypeScript Standards (Frontend)
- Use strict TypeScript configuration
- Prefer interfaces over types for object shapes
- Use proper type annotations for all function parameters and return values
- Utilize Vue 3 composition API with proper typing
- Follow Vue 3 and Pinia typing conventions

#### Development Principles
- Apply SOLID principles
- Ensure code modularity and maintainability
- Implement appropriate error handling
- Consider performance implications
- Prefer constants over repeating strings

## Version Management and Changelog

### CHANGELOG.md Updates

**CRITICAL**: Always check if CHANGELOG.md needs updates when making changes to the codebase.

#### When to Update CHANGELOG.md

1. **Code Changes**: Any modification to source code in `src/`
2. **New Features**: Added functionality or capabilities
3. **Bug Fixes**: Corrections to existing functionality
4. **Breaking Changes**: Modifications that affect existing APIs or behavior
5. **Documentation Updates**: Significant changes to README, CONTRIBUTING, or architecture docs
6. **Dependency Changes**: Updates to requirements or build configuration
7. **Configuration Changes**: Modifications to settings, environment variables, or deployment

#### Version Type Determination (Semantic Versioning)

Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):

**MAJOR (X.0.0)** - Breaking changes:
- API changes that break existing functionality
- Removal of deprecated features
- Architectural changes requiring user intervention
- Changes to public interfaces or method signatures

**MINOR (0.X.0)** - New features (backward compatible):
- New API endpoints or methods
- Additional configuration options
- Enhanced functionality that doesn't break existing code
- New components or features

**PATCH (0.0.X)** - Bug fixes and minor improvements:
- Bug fixes that don't change functionality
- Performance improvements
- Documentation corrections
- Dependency updates (security patches)
- Code refactoring without behavior changes

#### Changelog Update Process

1. **Check Git Status**: Determine if changes warrant a changelog entry
2. **Assess Impact**: Determine if changes are MAJOR, MINOR, or PATCH level
3. **Check Current Version**: Look at the latest version in CHANGELOG.md
4. **Check Git Tags**: Run `git tag -l` to see if current version has been released
5. **Determine Action**:
   - If version hasn't been released (no git tag exists): Add to existing version section
   - If version has been released (git tag exists): Create new version section
6. **Update package.json**: Increment version number to match changelog
7. **Categorize Changes**: Use appropriate sections (Added, Changed, Deprecated, Removed, Fixed, Security)

#### Example Changelog Entry Structure

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature descriptions
- New functionality additions

### Changed
- Modifications to existing features
- **BREAKING**: Mark breaking changes clearly

### Fixed
- Bug fixes and corrections

### Technical Details
- Implementation specifics
- Architectural improvements
```

## Commit Process

When instructed to commit changes, always follow this complete process:

1. **Review Git Diff**: Analyze all changes using `git diff` and `git status`
2. **Version Assessment**: Check if changes warrant a new version or should use current version from CHANGELOG.md
3. **Update CHANGELOG.md**: Categorize changes logically (Features, Fixes, Changes, Technical Details). Remove or simplify less important items to keep concise.
4. **Pre-commit Checks**: Run all quality checks:
   - Backend: `python -m pytest` for tests
   - Frontend: `npm run type-check` and `npm run format` 
5. **Generate Commits**: Create clean, organized commits with appropriate messages

## Commit Message Format

Follow these guidelines:
- Start with a short imperative sentence (max 50 chars) summarizing the changes
- Use present tense
- Leave a blank line after the first sentence
- Provide a more detailed explanation (max 2-3 sentences)
- Keep the entire message under 74 characters
- Be insightful but concise, avoiding overly verbose descriptions
- Do not prefix the message with anything