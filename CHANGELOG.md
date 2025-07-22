# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-21

### Added
- **Recipe locking feature** - users can lock specific recipes to keep them when fetching new recommendations
- **Permanent image storage system** with hierarchical directory structure for recipe images
- **Dark mode support** across the entire application with theme persistence
- **Comprehensive recipe filtering system** for recommendations with advanced tag support

### Changed
- Recipe model extended with permanent image storage fields (`storedImagePath`, `storedImageUrl`, `imageStoredAt`)
- Recipe recommendations now use MongoDB `$sample` aggregation for true randomness across entire database
- Image storage uses MD5-based hierarchical directories for performance at scale
- Enhanced UI with loading indicators and visual feedback

### Fixed
- Recipe recommendations now provide genuine variety instead of repeating same subset

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