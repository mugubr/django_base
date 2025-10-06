# Changelog

## [Unreleased] - 2025-10-06

### Added - Portfolio Features
- **UserProfile Model**: Extended user model with OneToOne relationship
  - Fields: bio, avatar (ImageField), phone, birth_date, city, country, website, is_verified
  - Automatic timestamps (created_at, updated_at)

- **Category Model**: Hierarchical product categories
  - Self-referencing ForeignKey for parent/child relationships
  - Auto-generated slugs
  - Active/inactive status

- **Tag Model**: Flexible product labeling system
  - ManyToMany relationship with products
  - Color coding for UI display
  - Auto-generated slugs

- **Product Model Enhancements**:
  - ForeignKey to Category (SET_NULL on delete)
  - ManyToMany to Tags
  - ForeignKey to User (created_by)

- **Authentication System**:
  - Custom LoginForm with Bootstrap 5 styling
  - RegisterForm with email validation
  - UserProfileForm for profile editing
  - UserUpdateForm for basic user info

- **Templates**:
  - Base template with Bootstrap 5.3 and HTMX 1.9
  - Responsive navigation with user dropdown
  - Footer with social links
  - Alert messages system
  - CSRF token configuration for HTMX

- **Admin Interface Enhancements**:
  - UserProfileAdmin with fieldsets and filters
  - CategoryAdmin with prepopulated slugs
  - TagAdmin with color display
  - ProductAdmin updated with new relationship filters

### Changed
- **Dockerfile**: Added Pillow>=11.0.0 to both dev and prod stages for ImageField support
- **Models imports**: Added User model, validators, and translation support

### Technical Details
- Template structure: `templates/{base,auth,partials,components}/`
- All models include bilingual comments (PT/EN)
- Forms use Bootstrap 5 classes throughout
- Admin uses list_display, list_filter, search_fields for better UX

### Migration
- Created migration: `0002_tag_product_created_by_category_product_category_and_more`

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
