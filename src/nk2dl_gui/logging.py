# nk2dl-gui/src/nk2dl_gui/logging.py
import logging
from typing import Optional

def get_gui_logger(name: str) -> logging.Logger:
    """Get a logger configured for GUI operations"""
    from nk2dl.logging import setup_logging
    return setup_logging(f'nk2dl_gui.{name}')

class QtLogger:
    """Qt-specific logger that wraps standard logger with UI formatting"""
    
    def __init__(self, name: str):
        from nk2dl.logging import setup_logging
        self._logger = setup_logging(name)
        self._ui_operation_mode = False
    
    def set_ui_operation_mode(self, enabled: bool):
        """Enable/disable UI operation mode for emoji formatting"""
        self._ui_operation_mode = enabled
    
    def _format_message(self, message: str, level: str) -> str:
        """Format message with emojis if UI operation mode is enabled"""
        if not self._ui_operation_mode:
            return message
            
        if level == 'debug':
            return f"🖥️ {message}"
        elif level == 'error':
            return f"❌ {message}"
        elif level == 'warning':
            return f"⚠️ {message}"
        elif level == 'info':
            return f"ℹ️ {message}"
        return message
    
    def debug(self, message: str):
        """Log debug message with optional UI formatting"""
        self._logger.debug(self._format_message(message, 'debug'))
    
    def info(self, message: str):
        """Log info message with optional UI formatting"""
        self._logger.info(self._format_message(message, 'info'))
    
    def warning(self, message: str):
        """Log warning message with optional UI formatting"""
        self._logger.warning(self._format_message(message, 'warning'))
    
    def error(self, message: str):
        """Log error message with optional UI formatting"""
        self._logger.error(self._format_message(message, 'error'))
    
    def critical(self, message: str):
        """Log critical message with optional UI formatting"""
        self._logger.critical(self._format_message(message, 'critical'))

# Create a singleton qt_logger for import - follows same pattern as regular logger
qt_logger = QtLogger('nk2dl_gui.qt')
