# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-05

### Added
- **Categories system** for organizing and grouping tags with hierarchy support
- **Tag image support** with 180+ tag images stored in frontend public directory
- **Tag exclusion filtering** in recipe recommendations via `exclude_tags` parameter
- **Category-based tag organization** in frontend with collapsible sections

### Changed
- **BREAKING**: Removed permanent image storage system and related endpoints
- **BREAKING**: Recipe model rating structure changed from flat fields to nested `rating` object with `rating` and `numVotes` properties
- Recipe recommendations filtering now supports both inclusion (`tags`) and exclusion (`exclude_tags`) of tags
- Tag store now fetches and manages tag images from public directory
- Enhanced recommendation filters UI with category-based tag grouping
- Frontend components refactored for better state management and performance

### Removed
- Image storage service and hierarchical directory system
- `/api/v1/images` endpoints
- Recipe image storage fields (`storedImagePath`, `storedImageUrl`, `imageStoredAt`)

### Technical Details
- Categories API endpoint at `/api/v1/categories` for retrieving tag categories
- Tag images served from `frontend/public/tag-images/` directory
- Improved TypeScript typing across frontend services and stores
- Simplified recipe model by removing image storage complexity

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