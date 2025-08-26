# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-08-26

### Added
- **Creative Mode System**: Revolutionary flexibility for reference image generation
  - `creative_mode` parameter: Toggle between consistent branding and creative freedom
  - `layout_freedom` levels: "standard", "flexible", "experimental"  
  - `composition_style` options: "left", "right", "centered", "dynamic", "creative"
  
- **Enhanced Reference Generation**:
  - Dual prompt system: Rigid layouts for branding vs. creative prompts for experimentation
  - Flexible text integration: From structured overlays to artistic text placement
  - Dynamic composition: AI can experiment with positioning while preserving faces

### Technical Features
- **Smart Prompt Switching**: Automatically chooses rigid vs. creative prompts based on parameters
- **Creative Prompt Templates**: New `_create_creative_reference_prompt()` method
- **Parameter Validation**: All creative mode options properly validated in Pydantic models

### Examples & Testing
- New demo script: `demo_creative_modes.py` - shows prompt differences without API calls
- Enhanced test script: `test_creative_modes.py` - tests all creative modes with actual generation
- Updated documentation with creative mode examples and usage patterns

### Documentation
- Comprehensive creative mode documentation in README
- New examples showcasing consistent branding vs. creative freedom
- Usage patterns for different creative scenarios

## [0.2.0] - 2025-08-26

### Added
- **Reference Image Integration**: Revolutionary personal branding feature
  - Use your own photos to generate consistent thumbnails
  - Preserves facial features and appearance with high input fidelity
  - Custom style templates for established thumbnail layouts
  - Support for positioning, text placement, and color scheme consistency
  
- **New MCP Tool**: `generate_reference_thumbnail`
  - Specialized tool for personal branding thumbnails
  - Parameters: `reference_image`, `main_text`, `secondary_text`, `topic`, `style_override`
  - Optimized for YouTube creator workflows
  
- **Enhanced `generate_image` Tool**:
  - New `reference_image` parameter for all image generation
  - Automatic detection and processing of reference images
  - Fallback handling when reference processing fails

### Technical Improvements
- **OpenAI Image API Integration**: Proper use of `images.edit` endpoint for reference images
- **High Input Fidelity Support**: Advanced reference image processing
- **Specialized Prompt Templates**: Optimized prompts for reference-based generation
- **Automatic Fallback**: Seamless fallback to standard generation when reference fails

### Examples & Testing
- Added comprehensive test suite for reference functionality
- Sample superhero image for testing reference image features
- Example scripts: `superhero_thumbnail_test.py`, `test_reference_thumbnail.py`
- Updated documentation with reference image examples

### Documentation
- Updated README with reference image features and examples
- New usage patterns for personal branding workflows
- Enhanced tool documentation with reference image parameters

## [0.1.0] - 2024-12-28

### Added
- Initial release of GPT Thumbnail MCP Server
- GPT-5 integration for advanced image generation using Responses API
- Support for multiple OpenAI models (GPT-5, GPT-Image-1, DALL-E 3)
- Specialized content type generation:
  - YouTube thumbnails with engagement optimization
  - Blog header and featured images
  - Social media content for multiple platforms
- Comprehensive prompt optimization system
- Platform-specific image optimization (YouTube, Instagram, Twitter, Facebook, Blog)
- AI-powered thumbnail effectiveness analysis and scoring
- Batch image generation with concurrent processing
- Advanced image processing utilities (resize, compress, enhance contrast)
- MCP protocol compliance with tools and resources
- Comprehensive configuration system with environment variables
- Professional logging and error handling
- Development tools setup (Black, Ruff, MyPy, Pytest)

### Features
- **5 MCP Tools**:
  - `generate_image` - Generate optimized images for different platforms
  - `optimize_for_platform` - Convert existing images for specific platforms
  - `analyze_thumbnail` - AI analysis of thumbnail effectiveness
  - `generate_batch` - Concurrent batch image generation
  - `get_prompt_suggestions` - Intelligent prompt improvement suggestions

- **3 MCP Resources**:
  - Image generation templates for different content types
  - Platform-specific best practices and guidelines
  - Example prompts and use cases

- **Smart Features**:
  - Automatic size selection based on content type
  - YouTube best practices integration (0.3-second rule, high contrast, faces)
  - Brand color integration and consistency
  - Emotional tone and style customization
  - Text overlay support with readability optimization
  - Fallback model support for reliability

### Technical Details
- Python 3.11+ support with modern async/await patterns
- UV package manager for fast dependency management
- Pydantic models for robust data validation
- PIL/Pillow for advanced image processing
- AsyncOpenAI client for API interactions
- Comprehensive test suite with pytest
- Type hints throughout codebase
- Structured logging and monitoring

### Documentation
- Comprehensive README with usage examples
- API documentation with all parameters and examples
- Best practices guide for different platforms
- MCP client configuration examples
- Troubleshooting guide and common issues
- Development setup and contribution guidelines

### Configuration
- Flexible configuration via environment variables
- Support for custom OpenAI endpoints
- Rate limiting and performance tuning options
- Quality and compression settings
- Logging level configuration
- Security and content filtering options