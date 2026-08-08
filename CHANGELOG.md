# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-08-08

### Added
- **Tags can be excluded from recommendations**, not only required. Each tag in the
  filter search offers "Nur mit" and "Ohne", and a recipe carrying an excluded tag is
  never drawn. New `exclude_tag_ids` parameter on `GET /recipes/recommendations`
- **Tag cards on the home page show an illustration** for around 180 tags. Tags without
  one get a plain tinted panel

### Changed
- **BREAKING**: removed the recipe image storage system - the `/api/v1/images`
  endpoints, and the `cachedImagePath`, `cachedImageUrl` and `imageCachedAt` recipe
  fields. The service wrote its results under different names than the API read back,
  so no stored image was ever served; recipe images have always come from the source
  site's own URL and continue to. Removing it also takes image downloads out of the
  recipe list, detail, create and recommendation request paths

### Fixed
- **Home page tag images are no longer broken.** Every tag card pointed at
  `via.placeholder.com`, a service that no longer resolves

### Technical Details
- Tag images are matched to a tag by its normalized name and ship as WebP, which holds
  the set to a third of the size the original JPEGs would have added
- Dropped the `aiohttp` and `aiofiles` dependencies along with the image service

## [1.4.1] - 2026-08-08

### Security
- **Patched a high severity advisory in `nanoid`** (GHSA-2v37-7h3g-55p8), pulled in
  through PostCSS, where a custom generator could loop indefinitely on a zero size

### Changed
- Raised the backend requirement floors for aiohttp, mongomock, pytest, pytest-asyncio
  and uvicorn to the versions already in use, and updated the frontend type packages

## [1.4.0] - 2026-08-02

### Added
- **Recipes can be filtered by source**, so recommendations can be limited to one of the
  sites recipes are collected from. New `GET /recipes/sources` endpoint lists them
- **Recommendations are drawn evenly from every source** instead of in proportion to how
  many recipes each site contributes, which kept the largest site from filling the page

### Changed
- **Recipe cards show the star average the site's own users gave.** Cards previously
  showed the internal ranking value, so a well rated recipe could render two stars below
  its actual rating. The ranking value is served separately as `score` and never displayed
- **The quality filter selects by rank rather than by stars** - "Top 20%" instead of
  "4.0★". Sites grade very differently, and a star threshold that is demanding on one site
  passes almost everything on another; a rank threshold keeps the same share of each
- **The vote filter covers the range every source reaches** (presets up to 50, previously
  up to 2000). The old presets silently excluded whole sites, and vote weight is already
  part of the ranking value
- **BREAKING**: the recommendation parameter `min_rating` is now `min_score`, and its
  default, like the vote filter's, no longer restricts anything
- Saved filters are reset once, because the stored rating value no longer means stars

### Fixed
- **Recipes with a blank image could appear among recommendations** despite the
  "only recipes with images" filter
- **Paging through the recipe list could repeat and skip recipes** - tens of thousands of
  recipes share one ranking value, leaving their order undefined between requests
- Recipes created through the API no longer write a ranking value they have no data for

## [1.3.0] - 2026-08-01

### Added
- **Hidden tags are summarised as a "+n" hint** on recipe cards, which names every tag of
  the recipe on hover

### Changed
- **Recipe cards show only the tags that fit on one line** - cards listed every tag of a
  recipe, wrapping over as many as four lines and leaving cards in the same row at wildly
  different heights. The most used tags are kept, up to three and only as many as the line
  holds, so long tag names are shown in full rather than cut off
- Removed the decorative diamond that trailed the tag list on recipe cards

## [1.2.1] - 2026-08-01

### Changed
- **Backend dependency floors raised across major versions**: `starlette` (0.41 → 1.3),
  `fastapi` (0.115 → 0.141), and `pytest` (8.3 → 9.0). FastAPI now requires Python 3.10+;
  CI and deployment already run Python 3.12

### Fixed
- **Recipe list is empty** - the recipe overview showed no recipes at all because the API served the rating in its stored form instead of a plain number, which broke rendering of every recipe card
- **Recommendations returned nothing** - the rating filter never matched any recipe, so the recommendation view stayed empty
- **Tag filtering and tag display** - recipes are filtered and shown with their tags again instead of returning no matches and empty tag lists
- Recipes without a rating are now displayed instead of breaking the list
- API errors such as an invalid tag ID now return their intended status code instead of a generic server error
- **Recipe cards showed raw tag ids** instead of tag names, because neither the recipe list nor the recommendations view resolved ids against the tag list
- **Filtering by several tags** only applied the last one selected; every selected tag is now sent to the API

### Security
- Resolved all 21 npm advisories in the frontend dependency tree, including critical
  issues in `vitest`, `tar`, and `shell-quote`, and high-severity path traversal and
  arbitrary file read issues in `vite`
- Updated vulnerable backend dependencies: `aiohttp`, `starlette`, `python-dotenv`,
  `setuptools`, and `pytest` now floor at versions with no known advisories

## [1.2.0] - 2025-07-22

### Added
- **Pull-to-refresh functionality** for mobile devices - users can pull down from top to refresh recommendations
- **Category-based tag organization** with improved tag management and display
- **Enhanced number formatting** for better readability across the application

### Changed
- Recipe recommendation filters now have improved styling with better button colors and visual feedback
- Mobile interface now uses pull-to-refresh instead of manual refresh button (hidden on screens < 768px)
- Filter buttons have individual borders for cleaner appearance
- Improved text readability for form placeholders and UI elements

### Removed
- **Time limit filters** from recipe recommendations (cooking time, preparation time, total time filters)

### Technical Details
- Touch-based pull-to-refresh with 80px threshold and smooth animations
- Mobile-only event listeners with proper cleanup on component unmount
- Responsive design improvements for better mobile experience

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