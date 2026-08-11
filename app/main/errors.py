"""
    Error handlers for the main blueprint
"""
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    """
        Render a custom 404 error page when a page is not found
    """
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    """
        Render a custom 500 error page when the server encounters an internal error    
    """
    return render_template('500.html'), 500
