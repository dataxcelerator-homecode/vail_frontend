#!/usr/bin/env python3
"""
Run the web application.
"""

import os
from src.web.app import create_app
from src.utils import setup_logger

# Setup logger
logger = setup_logger('web_server')

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Starting Keyboard Visualizer web server on port {port}...")
    app = create_app()
    logger.info(f"Server running at http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)

