"""
Layer visualization module.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web compatibility
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Optional
from tqdm import tqdm
from ..utils.keycode_simplifier import simplify_keycode, get_key_color
from ..utils.logger import get_logger

logger = get_logger(__name__)


class LayerVisualizer:
    """Handles visualization of keyboard layers."""
    
    def __init__(self, layers: List[List[List[str]]], max_rows: int, max_cols: int):
        """
        Initialize the visualizer.
        
        Args:
            layers: List of all layers to visualize
            max_rows: Maximum number of rows
            max_cols: Maximum number of columns
        """
        self.layers = layers
        self.max_rows = max_rows
        self.max_cols = max_cols
        logger.info(f"Initializing visualizer for {len(layers)} layers")
    
    def plot_layer(self, layer_data: List[List[str]], layer_index: int,
                   ax: plt.Axes) -> plt.Axes:
        """
        Plot a single keyboard layer on the given axes.
        
        Args:
            layer_data: The layer to plot (list of rows)
            layer_index: Index of the layer (for title)
            ax: Matplotlib axes to plot on
            
        Returns:
            Modified axes object
        """
        # Set up the plot
        ax.set_xlim(0, self.max_cols)
        ax.set_ylim(0, self.max_rows)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')
        ax.set_title(f'Layer {layer_index}', fontsize=14, fontweight='bold', pad=10)
        
        # Key dimensions
        key_width = 0.9
        key_height = 0.9
        
        # Plot each key
        for row_idx, row in enumerate(layer_data):
            for col_idx, keycode in enumerate(row):
                # Skip empty positions
                if keycode == -1 or keycode == "-1":
                    continue
                
                # Draw key background
                x = col_idx + 0.05
                y = row_idx + 0.05
                
                # Get simplified keycode and colors
                simplified = simplify_keycode(str(keycode))
                face_color, edge_color = get_key_color(simplified)
                
                # Draw key rectangle
                rect = patches.Rectangle((x, y), key_width, key_height,
                                        linewidth=1.5, edgecolor=edge_color,
                                        facecolor=face_color)
                ax.add_patch(rect)
                
                # Add keycode text
                text_x = x + key_width / 2
                text_y = y + key_height / 2
                
                # Adjust font size based on text length
                font_size = 8 if len(simplified) <= 4 else 6 if len(simplified) <= 8 else 5
                
                ax.text(text_x, text_y, simplified,
                       ha='center', va='center',
                       fontsize=font_size, fontweight='normal',
                       wrap=True)
        
        return ax
    
    def create_visualization(self, output_file: Optional[str] = None, show_progress: bool = True) -> None:
        """
        Create a multi-panel plot showing all keyboard layers.
        
        Args:
            output_file: Optional filename to save the plot. If None, displays interactively.
            show_progress: Whether to show progress bar (disable for web/API contexts)
        """
        num_layers = len(self.layers)
        if num_layers == 0:
            logger.warning("No layers to visualize")
            return
        
        logger.info(f"Creating visualization for {num_layers} layers")
        
        # Calculate grid layout for subplots (prefer 2 columns)
        cols = 2
        rows = (num_layers + cols - 1) // cols
        
        # Create figure
        fig_width = cols * (self.max_cols * 0.7)
        fig_height = rows * (self.max_rows * 0.7)
        fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
        fig.suptitle('Keyboard Layer Visualization', fontsize=16, fontweight='bold')
        
        # Flatten axes array for easier iteration
        if num_layers == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        # Plot each layer with optional progress bar
        logger.info("Plotting layers...")
        if show_progress:
            iterator = tqdm(range(num_layers), desc="Creating plots")
        else:
            iterator = range(num_layers)
        
        for idx in iterator:
            self.plot_layer(self.layers[idx], idx, axes[idx])
        
        # Hide unused subplots
        for idx in range(num_layers, len(axes)):
            axes[idx].axis('off')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save or show
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            logger.info(f"Saved visualization to {output_file}")
        else:
            plt.show()
            logger.info("Displaying visualization")
        
        # Close figure to free memory
        plt.close(fig)
    
    @staticmethod
    def print_layer_summary(layers: List[List[List[str]]]) -> None:
        """
        Print a text summary of all layers.
        
        Args:
            layers: List of all layers
        """
        logger.info("Generating layer summary")
        
        print(f"\n{'='*60}")
        print(f"Keyboard Layout Summary")
        print(f"{'='*60}")
        print(f"Total Layers: {len(layers)}")
        
        for layer_idx, layer in enumerate(layers):
            print(f"\nLayer {layer_idx}:")
            for row_idx, row in enumerate(layer):
                # Filter out empty positions
                keys = [simplify_keycode(str(k)) for k in row if k != -1 and k != "-1"]
                print(f"  Row {row_idx}: {' | '.join(keys)}")

