"""
Vial file loader module.
"""

import json
from typing import Dict, List, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VialLoader:
    """Handles loading and parsing of .vil files."""
    
    @staticmethod
    def load_file(filepath: str) -> Dict[str, Any]:
        """
        Load and parse a .vil JSON file.
        
        Args:
            filepath: Path to the .vil file
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file is not valid JSON
        """
        logger.info(f"Loading file: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Successfully loaded file with {len(data.get('layout', []))} layers")
            return data
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {filepath}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading file {filepath}: {e}")
            raise
    
    @staticmethod
    def extract_layers(vil_data: Dict[str, Any]) -> List[List[List[str]]]:
        """
        Extract layer data from vil JSON structure.
        
        Args:
            vil_data: Parsed .vil file data
            
        Returns:
            List of layers, where each layer is a list of rows,
            and each row is a list of keycodes
        """
        layers = vil_data.get('layout', [])
        logger.debug(f"Extracted {len(layers)} layers from data")
        return layers
    
    @staticmethod
    def get_key_dimensions(layers: List[List[List[str]]]) -> tuple:
        """
        Determine the maximum dimensions of the keyboard.
        
        Args:
            layers: List of all layers
            
        Returns:
            Tuple of (max_rows, max_cols)
        """
        if not layers:
            logger.warning("No layers found in data")
            return 0, 0
        
        max_rows = max(len(layer) for layer in layers)
        max_cols = max(len(row) for layer in layers for row in layer)
        
        logger.debug(f"Keyboard dimensions: {max_rows} rows x {max_cols} cols")
        return max_rows, max_cols

