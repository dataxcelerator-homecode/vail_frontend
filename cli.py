#!/usr/bin/env python3
"""
Command-line interface for keyboard visualization.
"""

import argparse
import sys
from src.core import VialLoader, KeycodeTransformer, LayerVisualizer
from src.utils import setup_logger

# Setup logger
logger = setup_logger('keyboard_visualizer')


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Visualize Vial keyboard layers from .vil backup files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic usage
  python cli.py input.vil output.png
  
  # Rename KC_TRNS to KC_NO in layer 4
  python cli.py input.vil output.png --rename-layer 4 --rename-old KC_TRNS --rename-new KC_NO
  
  # Without text summary
  python cli.py input.vil output.png --no-summary
  
  # Enable debug logging
  python cli.py input.vil output.png --debug
        '''
    )
    
    parser.add_argument('input_file', nargs='?', default='current copy.vil',
                        help='Input .vil file (default: current copy.vil)')
    parser.add_argument('output_file', nargs='?', default='output/keyboard_layers.png',
                        help='Output PNG file (default: output/keyboard_layers.png)')
    parser.add_argument('--rename-layer', type=int, metavar='N',
                        help='Layer index to apply keycode rename (e.g., 4)')
    parser.add_argument('--rename-old', metavar='KEYCODE',
                        help='Old keycode to replace (e.g., KC_TRNS)')
    parser.add_argument('--rename-new', metavar='KEYCODE',
                        help='New keycode to use (e.g., KC_NO)')
    parser.add_argument('--no-summary', action='store_true',
                        help='Skip printing text summary')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Set debug level if requested
    if args.debug:
        logger.setLevel('DEBUG')
        logger.debug("Debug logging enabled")
    
    try:
        # Load the file
        loader = VialLoader()
        vil_data = loader.load_file(args.input_file)
        
        # Extract layers
        layers = loader.extract_layers(vil_data)
        
        # Apply keycode rename if specified
        if args.rename_layer is not None and args.rename_old and args.rename_new:
            transformer = KeycodeTransformer()
            layers = transformer.rename_keycode_in_all_layers(
                layers, args.rename_layer, args.rename_old, args.rename_new
            )
        
        # Print summary if requested
        if not args.no_summary:
            LayerVisualizer.print_layer_summary(layers)
        
        # Get dimensions and create visualizer
        max_rows, max_cols = loader.get_key_dimensions(layers)
        visualizer = LayerVisualizer(layers, max_rows, max_cols)
        
        # Create visualization
        visualizer.create_visualization(args.output_file)
        
        logger.info("Visualization complete!")
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.debug)
        return 1


if __name__ == "__main__":
    sys.exit(main())

