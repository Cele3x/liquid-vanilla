# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-21

### Added
- **Recipe locking feature** for recommendations - users can lock specific recipes to keep them when fetching new recommendations
- **Image caching system** with hierarchical directory structure for recipe images
- **Recipe recommendations** with true randomness using MongoDB `$sample` aggregation
- Instant loading feedback with spinning wheels when fetching new recommendations
- Dark mode support across the entire application
- Comprehensive test suite with 90% code coverage

### Changed
- **BREAKING**: Recipe model extended with cached image fields (`cachedImagePath`, `cachedImageUrl`, `imageCachedAt`)
- Image caching uses MD5-based hierarchical directories (`cache/recipe_images/XX/YY/`) for performance at scale
- Recipe recommendations now support locked recipes via `locked_ids` parameter
- Recommendations button disabled when all 8 recipes are locked
- Recipe retrieval prioritizes cached images over external URLs

### Fixed
- Recipe recommendations now provide true randomness instead of returning same recipes repeatedly
- Frontend TypeScript interface alignment with API response structure (`tags` → `tagIds`)
- Recipe list display after fixing data structure mismatch
- Consistent card heights for recipe recommendations with proper loading spinners

### Technical Details
- Recipe locking system with backend parameter support and frontend state management
- Hierarchical image caching supporting thousands of images across 65,536 directories
- MongoDB aggregation pipeline with exclusion filters for locked recipes
- Enhanced UI with lock/unlock buttons, visual indicators, and loading placeholders

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