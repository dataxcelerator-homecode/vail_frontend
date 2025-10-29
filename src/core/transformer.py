"""
Keycode transformation module.
"""

from typing import List
from ..utils.logger import get_logger

logger = get_logger(__name__)


class KeycodeTransformer:
    """Handles transformation operations on keyboard layers."""
    
    @staticmethod
    def rename_keycode_in_layer(layer: List[List[str]], old_keycode: str,
                                new_keycode: str) -> List[List[str]]:
        """
        Replace all instances of a specific keycode with a new keycode in a layer.
        
        Args:
            layer: The layer to modify (list of rows)
            old_keycode: The keycode to replace
            new_keycode: The new keycode to use as replacement
            
        Returns:
            Modified layer with replaced keycodes
        """
        modified_layer = []
        replacement_count = 0
        
        for row in layer:
            modified_row = []
            for keycode in row:
                if str(keycode) == old_keycode:
                    modified_row.append(new_keycode)
                    replacement_count += 1
                else:
                    modified_row.append(keycode)
            modified_layer.append(modified_row)
        
        logger.debug(f"Replaced {replacement_count} instances of '{old_keycode}' with '{new_keycode}'")
        return modified_layer
    
    @staticmethod
    def rename_keycode_in_all_layers(layers: List[List[List[str]]], layer_index: int,
                                     old_keycode: str, new_keycode: str) -> List[List[List[str]]]:
        """
        Replace all instances of a keycode in a specific layer.
        
        Args:
            layers: List of all layers
            layer_index: Index of the layer to modify
            old_keycode: The keycode to replace
            new_keycode: The new keycode to use
            
        Returns:
            Modified layers list with the specified layer updated
        """
        if layer_index < 0 or layer_index >= len(layers):
            logger.warning(f"Layer index {layer_index} out of range (0-{len(layers)-1})")
            return layers
        
        logger.info(f"Renaming '{old_keycode}' to '{new_keycode}' in layer {layer_index}")
        
        modified_layers = []
        for idx, layer in enumerate(layers):
            if idx == layer_index:
                modified_layer = KeycodeTransformer.rename_keycode_in_layer(
                    layer, old_keycode, new_keycode
                )
                modified_layers.append(modified_layer)
            else:
                modified_layers.append(layer)
        
        return modified_layers

