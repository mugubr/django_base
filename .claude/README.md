# Claude Code Configuration for django_base

This directory contains optimized Claude Code configuration for maximum
productivity and token efficiency.

## 📁 Structure

```
.claude/
├── README.md                    # This file
├── context.md                   # Project context (bilingual, token-optimized)
├── settings.local.json          # Claude Code settings with permissions
├── agents/                      # Specialized agents for different tasks
│   ├── django-expert.md        # Django/DRF expert
│   ├── code-reviewer.md        # Code quality and security reviewer
│   ├── backend-architect.md    # System architecture expert
│   └── python-pro.md           # Python optimization specialist
├── scripts/
│   └── context-monitor.py      # Status line script (token counter)
└── skills/
    └── mcp-builder/            # MCP server builder skill
```

## 🎯 Core Philosophy

### 1. Maximum Token Economy ⚡

- **Edit over Rewrite**: Use `Edit` tool for modifications
- **Agents for Complex Tasks**: Use specialized agents via `Task` tool
- **Concise Responses**: 1-4 lines when possible, no fluff
- **Smart Caching**: Leverage context caching for frequent reads

### 2. Bilingual Documentation 🌍

- **All docstrings**: English first line, Portuguese second
- **Inline comments**: `# EN / PT-BR`
- **Templates**: Use `{% trans %}` for i18n
- **Code is globally accessible**: EN/PT-BR by default

### 3. Quality Assurance 🛡️

- **Pre-commit hooks**: 20+ quality checks
- **Ruff formatting**: Auto-format on save
- **Security scanning**: Bandit integration
- **Test coverage**: Maintain >80%

## 🤖 Specialized Agents

### Django Expert (`django-expert`)

**When to use**: Django models, views, forms, serializers, DRF tasks

```bash
# Example usage in conversation:
"Use the django-expert agent to create a new API endpoint for orders"
```

**Expertise**:

- Models with proper mixins (Timestamped, SoftDelete, UserTracking)
- DRF ViewSets with filters, search, pagination
- Forms with Bootstrap 5 widgets
- Custom validators and decorators
- Bilingual docstrings

### Code Reviewer (`code-reviewer`)

**When to use**: After implementing features, before commits

```bash
# Example usage:
"Use the code-reviewer agent to review my changes"
```

**Review checklist**:

- Code quality (Ruff, unused imports, type hints)
- Django best practices (ORM, queries, migrations)
- Security (no hardcoded secrets, CSRF, XSS, SQL injection)
- Project standards (bilingual docs, i18n, mixins)
- Performance (N+1 queries, caching)
- Testing (coverage, edge cases)

### Backend Architect (`backend-architect`)

**When to use**: Architectural decisions, database design, scalability

```bash
# Example usage:
"Use the backend-architect agent to design the notification system"
```

**Expertise**:

- System architecture and API design
- Database schema and relationships
- Scalability planning
- Performance optimization
- Integration patterns

### Python Pro (`python-pro`)

**When to use**: Refactoring, optimization, advanced Python features

```bash
# Example usage:
"Use the python-pro agent to optimize the data processing pipeline"
```

**Expertise**:

- Python best practices and patterns
- Performance optimization
- Async/await, generators, decorators
- Type hints and static analysis
- Code refactoring

## 🧠 Memory MCP Server

The project is configured with Memory MCP server for persistent context across
sessions.

**Configuration**: See `.mcp.json` in project root

**Usage**:

```typescript
// Memory MCP automatically persists:
- Important project decisions
- Architecture patterns
- User preferences
- Conversation context
```

**Benefits**:

- Continuity across sessions
- Reduced context repetition
- Better long-term understanding
- Faster startup with cached knowledge

## ⚙️ Settings Explained

### Permissions (`settings.local.json`)

**Simplified wildcard permissions** for common tools:

- `docker-compose:*`, `docker:*` - Docker operations
- `git:*` - All git operations
- `kubectl:*`, `kubectl.exe:*` - Kubernetes operations
- `python:*`, `ruff:*` - Python and linting
- `pre-commit:*` - Code quality hooks

**Denied operations** (safety):

- `rm -rf /` - System deletion
- `dd:*` - Disk operations
- Fork bombs and destructive commands

### Status Line

Shows real-time token usage via `context-monitor.py`:

```
Tokens: 45k/200k | Files: 12 | Context: 15%
```

## 📖 Context File (`context.md`)

Optimized project documentation with:

- **Mission and critical rules** (token economy, bilingual, workflow)
- **Architecture and tech stack** (table format for quick reference)
- **Design principles** (security, DX, performance, soft delete)
- **Core files reference** (models, views, forms, APIs, utils)
- **Common workflows** (how to create endpoints, pages, etc.)
- **Quick commands** (Docker, database, testing)
- **Critical info** (credentials, URLs, ports)
- **Code patterns** (docstrings, forms, templates)

## 🚀 Best Practices

### When Starting a Task

1. **Check context**: Read `.claude/context.md` if unfamiliar
2. **Plan complex tasks**: Use `TodoWrite` for 3+ steps
3. **Choose the right agent**: Use specialized agents for efficiency
4. **Verify state**: Run `git status` before modifications

### During Development

1. **Edit, don't rewrite**: Use `Edit` tool for changes
2. **Bilingual everything**: Docstrings and comments EN/PT-BR
3. **Test immediately**: Write tests with new features
4. **Commit often**: Small, focused commits with bilingual messages

### Before Committing

1. **Review code**: Use `code-reviewer` agent
2. **Run tests**: Ensure >80% coverage
3. **Check quality**: Pre-commit hooks run automatically
4. **Update docs**: If public API changed

## 💡 Token Optimization Tips

### For Users

1. **Be specific**: "Add user authentication" vs "Add JWT authentication with
   refresh tokens"
2. **Use agents**: Complex tasks → specialized agents
3. **Reference files**: "Edit line 42 in models.py" vs explaining the whole
   context
4. **Batch requests**: Multiple related changes in one message

### For Claude

1. **Prefer Edit**: Modify existing code, don't rewrite
2. **Concise responses**: Skip pleasantries, get to the point
3. **Use memory**: Store recurring patterns, user preferences
4. **Smart tool selection**: Grep before Read for large files

## 📚 Quick Reference

### File Paths

- **Context**: `.claude/context.md`
- **Settings**: `.claude/settings.local.json`
- **Agents**: `.claude/agents/*.md`
- **MCP Config**: `.mcp.json` (root)

### Agent Invocation

```bash
# In conversation with Claude:
"Use <agent-name> to <task>"

# Examples:
"Use django-expert to create a Product model"
"Use code-reviewer to check my changes"
"Use backend-architect to design the API"
"Use python-pro to optimize this function"
```

### Common Commands

```bash
# Check token usage
cat .claude/scripts/context-monitor.py

# View context
cat .claude/context.md

# List agents
ls .claude/agents/

# Check MCP config
cat .mcp.json
```

## 🔧 Maintenance

### Updating Context

When project evolves significantly:

1. Edit `.claude/context.md`
2. Keep it concise (token-optimized)
3. Update file counts, model lists, etc.
4. Maintain bilingual standard

### Adding New Agents

1. Create `.claude/agents/new-agent.md`
2. Define expertise and usage
3. List available tools
4. Add usage examples
5. Document in this README

### Reviewing Permissions

Periodically check `.claude/settings.local.json`:

- Remove unused permissions
- Add new common operations
- Verify deny list is complete

## 📊 Metrics

Track these for optimization:

- **Token usage per session**: Aim for <50k for standard tasks
- **Agent usage**: Which agents are most effective?
- **Edit vs Rewrite ratio**: Higher is better
- **Response length**: Shorter is better (when appropriate)

## 🎓 Learning Resources

- [Claude Code Docs](https://docs.claude.com/claude-code)
- [MCP Documentation](https://modelcontextprotocol.io)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)
- [DRF Best Practices](https://www.django-rest-framework.org/topics/best-practices/)

---

**Last Updated**: 2025-10-20 **Version**: 1.0.0 **Status**: ✅ Production Ready
