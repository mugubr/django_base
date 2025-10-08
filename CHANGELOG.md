# Changelog

All notable changes to this project will be documented in this file. Todas as
mudanças notáveis neste projeto serão documentadas neste arquivo.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
O formato é baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [Unreleased] - 2025-10-07

### Added - New Features / Novos Recursos

**Product Listing Page**:

- ✅ Beautiful products page with card grid layout
- ✅ Advanced filters: category, tags, price range (min/max)
- ✅ Pagination with query string preservation
- ✅ Responsive design with Bootstrap 5.3
- ✅ View at `/products/` with full i18n support

**Visual Health Check Page**:

- ✅ Beautiful health check page at `/health-status/`
- ✅ Real-time system status with auto-refresh (30s)
- ✅ Visual indicators for database, cache, and overall health
- ✅ System information panel (version, environment)
- ✅ Responsive design with hover effects

### Changed - UI/UX Improvements / Melhorias UI/UX

**Auto-Dismiss Alerts**:

- ✅ Fixed white line after logout issue
- ✅ Alerts auto-dismiss after 5 seconds using Bootstrap Alert API
- ✅ Smooth fade-out animation for better UX

**Hover Effects**:

- ✅ Added hover effects to nav-links (translateY with transition)
- ✅ Added hover effects to dropdown-items
- ✅ Added hover effects to cards with shadow enhancement
- ✅ Added hover effects to dashboard buttons

**Pre-commit Hooks**:

- ✅ Re-enabled YAML syntax checking (check-yaml hook)
- ✅ All 20+ hooks active and configured

### Added - New Features / Novos Recursos

**Database Seeding**:

- ✅ Management command `seed_database` to populate database with sample data
- ✅ Creates 3 sample users with profiles (alice, bob, carol)
- ✅ Creates 8 categories with hierarchical structure (Electronics, Computers,
  etc.)
- ✅ Creates 7 tags with colors (New, Popular, Sale, Featured, etc.)
- ✅ Creates 10 sample products with relationships (MacBook, iPhone, books,
  etc.)
- ✅ Supports `--clear` flag to reset data before seeding
- ✅ Command available in README with examples

**Documentation Enhancements**:

- ✅ Added detailed Grafana setup instructions in README (EN/PT-BR)
- ✅ Added dashboard import guide with 4 recommended dashboards
- ✅ Added custom dashboard tips and troubleshooting
- ✅ Documented seed_database command in Development Commands section
- ✅ Updated all metrics endpoints URLs in README

### Changed - Improvements / Melhorias

**Observability & Monitoring**:

- ✅ Changed Prometheus metrics endpoint from `/django-metrics/` to `/metrics/`
- ✅ Corrected endpoint URL: now accessible at `/metrics/metrics`
- ✅ Verified django-prometheus integration is working correctly
- ✅ Updated all README references to new metrics endpoint

### Added - i18n Support / Suporte i18n

**Internationalization (EN/PT-BR)**:

- ✅ Django i18n configured in settings (LocaleMiddleware, LANGUAGES,
  LOCALE_PATHS)
- ✅ Translation files: `locale/pt_BR/LC_MESSAGES/django.po` with 90+
  translations
- ✅ Templates: register.html, login.html, home.html, profile.html, and
  base.html fully translated with `{% trans %}`
- ✅ All feature cards and dashboard sections translated
- ✅ Dockerfile: Added `gettext` for `compilemessages` support
- ✅ locale/README.md: Documentation for translation workflow
- ✅ .env.example: Updated defaults (LANGUAGE_CODE=pt-br,
  TIME_ZONE=America/Sao_Paulo)

### Changed - API Documentation / Documentação da API

**ViewSet Docstrings (EN/PT-BR)**:

- ✅ Standardized all custom action docstrings in viewsets following consistent
  format
- ✅ ProductViewSet: 4 custom actions (recent, deactivate, activate,
  price_range)
- ✅ CategoryViewSet: tree action for hierarchical navigation
- ✅ TagViewSet: popular action with product count
- ✅ UserProfileViewSet: me action for current user profile
- ✅ All docstrings now include: method description, query params, example
  requests, return codes
- ✅ Full bilingual documentation (English first, Portuguese after separator)

### Fixed - Bug Fixes / Correções

**Template Issues**:

- ✅ Removed HTMX code from register view (AttributeError: 'WSGIRequest' object
  has no attribute 'htmx')
- ✅ Removed unused `templates/auth/partials/register_form.html`
- ✅ Form now renders correctly without HTMX dependencies

### Added - Documentation & Optimization / Documentação & Otimização

**Full Bilingual Documentation (EN/PT)**:

- ✅ All 20+ Python files documented with bilingual docstrings
- ✅ Module-level docstrings explaining purpose and features
- ✅ Class/function docstrings with Fields/Args/Returns in both languages
- ✅ Inline comments bilingual (# English / Português)

**Template System Enhancements**:

- ✅ All 7 HTML templates documented with bilingual comments
- ✅ Custom green primary color (#198754) replacing Bootstrap blue
- ✅ CSS variables for consistent theming
- ✅ HTMX configuration documented

**Project Configuration**:

- ✅ pyproject.toml: Enhanced with bilingual comments, expanded
  keywords/classifiers
- ✅ Dependencies organized by category with inline documentation
- ✅ .claude_context.md: Optimized from 362 to 134 lines (-63% tokens)
- ✅ README.md: Updated with complete feature list and all endpoints

**Code Quality**:

- ✅ models.py: Enhanced docstrings for all 4 models (Product, UserProfile,
  Category, Tag)
- ✅ views.py: Complete documentation for 5 views + error handlers
- ✅ serializers.py: 10 serializers documented via Task agent
- ✅ viewsets.py: 4 ViewSets with custom actions documented
- ✅ signals.py: UserProfile signal with bilingual error handling
- ✅ admin.py, tasks.py, urls.py, tests.py: All documented
- ✅ settings: base/dev/prod with bilingual section comments
- ✅ forms.py: 4 forms with detailed bilingual docstrings

### Changed - UI/UX Improvements / Melhorias UI/UX

**Color Scheme**:

- 🎨 Primary color: Blue (#0d6efd) → Green (#198754)
- 🎨 All btn-primary, text-primary, bg-primary now green
- 🎨 CSS variables updated in base.html
- 🎨 Navbar: Dark green theme with improved contrast

**Templates Updated**:

- base.html: Header comments + green CSS + bilingual documentation
- home.html, login.html, register.html, profile.html: Bilingual comments
- card.html, pagination.html: Component documentation

### Documentation Files

**Created/Updated**:

- FEATURES.md: Complete (734 lines, 100% bilingual)
- CHANGELOG.md: This file, comprehensive changelog
- README.md: Updated with new features and endpoints
- .claude_context.md: Optimized for token efficiency

---

## [0.1.0] - 2025-10-06

### Added - Portfolio Features

#### Models (4 total: Product, UserProfile, Category, Tag)

**UserProfile Model** - Extended user model with OneToOne relationship

- Fields: bio, avatar (ImageField), phone, birth_date, city, country, website,
  is_verified
- Automatic timestamps (created_at, updated_at)
- Signal-based auto-creation when User is created
- Custom admin with fieldsets organization

**Category Model** - Hierarchical product categories

- Self-referencing ForeignKey for parent/child relationships
- Auto-generated slugs from name
- Active/inactive status
- API endpoint for tree structure (`/api/v1/categories/tree/`)

**Tag Model** - Flexible product labeling system

- ManyToMany relationship with products
- Color coding (hex validation) for UI display
- Auto-generated slugs
- API endpoint for popular tags (`/api/v1/tags/popular/`)

**Product Model Enhancements**

- ForeignKey to Category (SET_NULL on delete)
- ManyToMany to Tags
- ForeignKey to User (created_by)

#### Authentication System (5 views, 4 forms, 4 templates)

**Forms** (`src/core/forms.py`):

- LoginForm: Username/email + password with remember_me checkbox
- RegisterForm: Full registration with email uniqueness validation
- UserProfileForm: All profile fields with Bootstrap widgets
- UserUpdateForm: Basic user info (first_name, last_name, email)

**Views** (`src/core/views.py`):

- home: Homepage with features showcase and user dashboard
- login_view: Custom login with session expiry control (2 weeks if remember_me)
- register_view: Registration with auto-login after success
- logout_view: Logout with confirmation message
- profile_view: View/edit profile with dual forms (User + Profile)

**Templates** (Bootstrap 5.3 + HTMX 1.9):

- base.html: Base template with navbar, messages, footer
- home.html: Features grid + user dashboard
- login.html: Styled login form with animations
- register.html: Multi-field registration with password requirements
- profile.html: Profile edit with sidebar and contact info

#### API Endpoints (4 ViewSets, 10 Serializers)

**Serializers** (`src/core/serializers.py`):

- CategorySerializer / CategoryListSerializer
- TagSerializer / TagListSerializer
- UserProfileSerializer / UserProfileListSerializer
- Product serializers (existing): ProductSerializer, ProductListSerializer,
  ProductCreateSerializer, ProductUpdateSerializer

**ViewSets** (`src/core/viewsets.py`):

- CategoryViewSet: CRUD + tree navigation
- TagViewSet: CRUD + popular tags endpoint
- UserProfileViewSet: CRUD + `/me/` endpoint for current user
- ProductViewSet: Enhanced with category/tag filtering

#### Template Tags & Filters (`src/core/templatetags/core_tags.py`)

**Simple Tags (7)**:

- get_settings_value, current_year, badge, icon, alert, is_active_url,
  query_string

**Filters (14)**:

- currency, percentage, truncate_chars_middle, file_size, time_ago
- class_name, get_item, multiply, divide, initials, active_badge

**Inclusion Tags (2)**:

- card (Bootstrap card component)
- render_pagination (pagination controls)

#### Utilities

**Validators** (`src/core/validators.py` - 8 validators):

- PhoneNumberValidator: International phone format
- CPFValidator: Brazilian tax ID with check digits
- validate_image_size: Max 5MB
- validate_image_dimensions: 100x100 to 4000x4000px
- validate_youtube_url: YouTube video URLs
- validate_future_date, validate_past_date: Date validation
- validate_min_age: Age verification (default 18)
- Regex validators: username_validator, slug_validator, hex_color_validator

**Decorators** (`src/core/decorators.py` - 15 decorators):

- Permission: admin_required, superuser_required, verified_required,
  anonymous_required
- Caching: cache_result(timeout, key_prefix)
- Logging: log_execution_time, log_errors, monitored_view
- Rate limiting: rate_limit(max_requests, period), SimpleRateLimiter class
- API: require_ajax, json_response

**Mixins** (`src/core/mixins.py` - 13 mixins):

- Model Mixins (4): TimeStampedModelMixin, SoftDeleteModelMixin,
  UserTrackingModelMixin, PublishableModelMixin
- View Mixins (9): AdminRequiredMixin, SuperuserRequiredMixin,
  VerifiedRequiredMixin, OwnerRequiredMixin, SetOwnerOnCreateMixin,
  MessageMixin, PaginationMixin, AjaxResponseMixin, ActiveOnlyQuerySetMixin

#### Signals (`src/core/signals.py`)

**UserProfile Auto-Creation**:

- post_save signal on User model
- Automatically creates UserProfile for new users
- Includes error handling and logging
- Fallback handler for edge cases

#### Admin Interface Enhancements

- UserProfileAdmin: Fieldsets (User Info, Contact, Location, Status), search by
  username/email/city
- CategoryAdmin: Prepopulated slugs, hierarchical display
- TagAdmin: Color display, prepopulated slugs
- ProductAdmin: Updated with category/tags filters, filter_horizontal for tags

#### Documentation

- FEATURES.md: Detailed documentation of all features with examples
  (English/Portuguese)
- .claude_context.md: Updated with complete feature reference
- Inline documentation: All code includes bilingual comments (PT/EN)

### Changed

- **Dockerfile**: Added Pillow>=11.0.0 to both dev and prod stages for
  ImageField support
- **Models imports**: Added User model, validators, and translation support

### Technical Details

- Template structure: `templates/{base,auth,partials,components}/`
- All models include bilingual comments (PT/EN)
- Forms use Bootstrap 5 classes throughout
- Admin uses list_display, list_filter, search_fields for better UX

### Migration

- Created migration:
  `0002_tag_product_created_by_category_product_category_and_more`

---

## [0.1.0] - Previous

### Features

- Django 5.2+ with DRF
- PostgreSQL 15 + Redis 7
- Docker multi-stage builds
- Modular settings (base/dev/prod)
- Prometheus + Grafana monitoring
- Pre-commit hooks (20+)
- API documentation (Swagger/ReDoc)
- Background tasks (Django Q)
- Initial Product Model
