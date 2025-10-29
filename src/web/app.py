"""
Flask web application for keyboard visualization.
"""

import os
from pathlib import Path
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from ..core import VialLoader, KeycodeTransformer, LayerVisualizer, InteractiveVisualizer
from ..utils import setup_logger

logger = setup_logger('web_app')

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
UPLOAD_FOLDER = PROJECT_ROOT / 'data'
OUTPUT_FOLDER = PROJECT_ROOT / 'output'
ALLOWED_EXTENSIONS = {'vil', 'json'}


def allowed_file(filename: str) -> bool:
    """Check if file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__,
                template_folder='../../templates',
                static_folder='../../static')
    
    app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
    app.config['OUTPUT_FOLDER'] = str(OUTPUT_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.secret_key = 'keyboard-visualizer-secret-key-change-in-production'
    
    # Ensure folders exist
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    
    @app.route('/')
    def index():
        """Main page."""
        logger.info("Index page accessed")
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and visualization."""
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(url_for('index'))
            
            file = request.files['file']
            
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('index'))
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload a .vil or .json file', 'error')
                return redirect(url_for('index'))
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logger.info(f"File uploaded: {filename}")
            
            # Get transformation parameters
            rename_layer = request.form.get('rename_layer', type=int)
            rename_old = request.form.get('rename_old', '').strip()
            rename_new = request.form.get('rename_new', '').strip()
            
            # Load and process file
            loader = VialLoader()
            vil_data = loader.load_file(filepath)
            layers = loader.extract_layers(vil_data)
            
            # Apply transformation if requested
            if rename_layer is not None and rename_old and rename_new:
                transformer = KeycodeTransformer()
                layers = transformer.rename_keycode_in_all_layers(
                    layers, rename_layer, rename_old, rename_new
                )
                logger.info(f"Applied transformation: layer {rename_layer}, {rename_old} -> {rename_new}")
            
            # Generate visualizations (both PNG and HTML)
            max_rows, max_cols = loader.get_key_dimensions(layers)
            
            # Generate static PNG
            visualizer = LayerVisualizer(layers, max_rows, max_cols)
            png_filename = f"visualization_{os.path.splitext(filename)[0]}.png"
            png_path = os.path.join(app.config['OUTPUT_FOLDER'], png_filename)
            visualizer.create_visualization(png_path, show_progress=False)
            logger.info(f"PNG visualization created: {png_filename}")
            
            # Generate interactive HTML
            interactive_viz = InteractiveVisualizer(layers, max_rows, max_cols)
            html_filename = f"visualization_{os.path.splitext(filename)[0]}.html"
            html_path = os.path.join(app.config['OUTPUT_FOLDER'], html_filename)
            interactive_viz.generate_html(html_path, png_filename)
            logger.info(f"Interactive HTML created: {html_filename}")
            
            flash('Visualization created successfully!', 'success')
            
            return render_template('result.html',
                                 image_filename=png_filename,
                                 html_filename=html_filename,
                                 num_layers=len(layers))
            
        except Exception as e:
            logger.error(f"Error processing file: {e}", exc_info=True)
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    @app.route('/download/<filename>')
    def download_file(filename):
        """Download generated visualization."""
        try:
            filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
            logger.info(f"File download: {filename}")
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            flash('File not found', 'error')
            return redirect(url_for('index'))
    
    @app.route('/view/<filename>')
    def view_file(filename):
        """View generated visualization (PNG or HTML)."""
        try:
            filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
            
            # Determine mimetype based on file extension
            if filename.endswith('.html'):
                return send_file(filepath, mimetype='text/html')
            else:
                return send_file(filepath, mimetype='image/png')
        except Exception as e:
            logger.error(f"Error viewing file: {e}")
            return "File not found", 404
    
    @app.route('/interactive/<filename>')
    def view_interactive(filename):
        """Serve interactive HTML visualization in an iframe-friendly way."""
        try:
            filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return html_content
        except Exception as e:
            logger.error(f"Error loading interactive view: {e}")
            return "File not found", 404
    
    @app.route('/about')
    def about():
        """About page."""
        return render_template('about.html')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

