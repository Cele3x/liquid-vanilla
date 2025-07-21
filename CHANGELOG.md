# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-21

### Added
- **Image caching system** with hierarchical directory structure for recipe images
- Recipe recommendations endpoint returning recipes with images only
- Tag icon support for visual recipe categorization
- Dark mode support across the entire application
- Comprehensive test suite with 86 tests and 90% code coverage

### Changed
- **BREAKING**: Recipe model extended with cached image fields (`cachedImagePath`, `cachedImageUrl`, `imageCachedAt`)
- Image caching uses MD5-based hierarchical directories (`cache/recipe_images/XX/YY/`) for performance at scale
- Recipe retrieval prioritizes cached images over external URLs
- Updated Node.js version in deployment workflow to v24

### Fixed
- Tag filtering bug in recipe queries (corrected field name from `tags` to `tagIds`)
- Frontend image fallback when cached images unavailable

### Technical Details
- Hierarchical image caching supporting thousands of images across 65,536 directories
- Async image downloading with aiohttp and aiofiles
- Comprehensive test coverage including edge cases and error scenarios
- Enhanced development environment with improved tooling and documentation

## [1.0.0] - 2024-12-01

### Added
- Full-stack recipe management web application
- FastAPI backend with MongoDB integration
- Vue 3 frontend with TypeScript and Tailwind CSS
- Complete recipe CRUD operations with rich metadata support
- Advanced tag system with filtering and management capabilities
- Full-text search functionality for recipes
- Infinite scroll pagination (20 recipes per page)
- Real-time search with debouncing
- Tag-based filtering with multiple tag selection
- Recipe image URL templating for different formats
- Loading indicators and responsive UI design
- Comprehensive API endpoints for recipes and tags
- Complete test suites for both backend and frontend
- GitHub Actions deployment workflow
- Development environment setup with hot reloading

### Technical Details
- MongoDB database integration with proper connection management
- RESTful API design with `/api/v1` base URL
- Pinia state management for frontend data
- Component-based Vue 3 architecture
- pytest testing framework with mongomock for backend
- Vitest testing framework for frontend
- CORS configuration for cross-origin requests
- Environment-based configuration management
- Code quality tools (ESLint, Prettier, Black, isort, flake8, mypy)