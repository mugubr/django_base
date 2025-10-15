"""
Context Processors - Core Application
Processadores de Contexto - Aplicação Core

Context processors add variables to the template context for all templates.
This makes configuration and common data easily accessible in templates without
passing them explicitly from every view.

Processadores de contexto adicionam variáveis ao contexto de template para todos os templates.
Isso torna configurações e dados comuns facilmente acessíveis em templates sem
precisar passá-los explicitamente de cada view.
"""

from decouple import config


def portfolio_settings(request):
    """
    Add portfolio configuration to template context.
    These settings come from environment variables and allow
    easy customization of the portfolio without code changes.

    Adiciona configuração do portfolio ao contexto do template.
    Essas configurações vêm de variáveis de ambiente e permitem
    fácil customização do portfolio sem alterações de código.

    Returns:
        dict: Portfolio configuration variables
    """
    return {
        "PORTFOLIO_NAME": config("PORTFOLIO_NAME", default="Your Name"),
        "PORTFOLIO_TITLE": config("PORTFOLIO_TITLE", default="Full Stack Developer"),
        "GITHUB_USERNAME": config("GITHUB_USERNAME", default=""),
        "LINKEDIN_USERNAME": config("LINKEDIN_USERNAME", default=""),
        "PORTFOLIO_EMAIL": config("PORTFOLIO_EMAIL", default=""),
        "PORTFOLIO_BIO": config(
            "PORTFOLIO_BIO",
            default="Passionate about creating scalable web applications and solving complex problems.",
        ),
    }
