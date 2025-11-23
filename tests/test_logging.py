"""
Tests for logging functionality across the codebase.

This module tests:
1. Loguru logger configuration and usage
2. Standard logging configuration
3. Log level filtering
4. Log output capture
"""

import logging
import sys
from io import StringIO
from pathlib import Path

import pytest
from loguru import logger


class TestLoguruLogging:
    """Test loguru logger configuration and functionality."""

    def setup_method(self):
        """Setup for each test - configure loguru to capture logs."""
        # Remove default handlers
        logger.remove()

        # Store log messages for testing
        self.log_messages = []

        def log_sink(message):
            self.log_messages.append(message)

        # Add a sink that captures logs
        self.handler_id = logger.add(
            log_sink,
            format="{level} | {message}",
            level="DEBUG"
        )

    def teardown_method(self):
        """Cleanup after each test."""
        logger.remove(self.handler_id)

    def test_logger_info_level(self):
        """Test that info level logs are captured."""
        test_message = "Test info message"
        logger.info(test_message)

        assert len(self.log_messages) == 1
        assert "INFO" in self.log_messages[0]
        assert test_message in self.log_messages[0]

    def test_logger_debug_level(self):
        """Test that debug level logs are captured."""
        test_message = "Test debug message"
        logger.debug(test_message)

        assert len(self.log_messages) == 1
        assert "DEBUG" in self.log_messages[0]
        assert test_message in self.log_messages[0]

    def test_logger_warning_level(self):
        """Test that warning level logs are captured."""
        test_message = "Test warning message"
        logger.warning(test_message)

        assert len(self.log_messages) == 1
        assert "WARNING" in self.log_messages[0]
        assert test_message in self.log_messages[0]

    def test_logger_error_level(self):
        """Test that error level logs are captured."""
        test_message = "Test error message"
        logger.error(test_message)

        assert len(self.log_messages) == 1
        assert "ERROR" in self.log_messages[0]
        assert test_message in self.log_messages[0]

    def test_logger_success_level(self):
        """Test that success level logs are captured (loguru-specific)."""
        test_message = "Test success message"
        logger.success(test_message)

        assert len(self.log_messages) == 1
        assert "SUCCESS" in self.log_messages[0]
        assert test_message in self.log_messages[0]

    def test_logger_with_format_strings(self):
        """Test logger with formatted strings."""
        name = "TestUser"
        count = 42
        logger.info(f"User {name} has {count} items")

        assert len(self.log_messages) == 1
        assert "TestUser" in self.log_messages[0]
        assert "42" in self.log_messages[0]

    def test_logger_multiple_messages(self):
        """Test that multiple log messages are all captured."""
        logger.info("Message 1")
        logger.debug("Message 2")
        logger.warning("Message 3")

        assert len(self.log_messages) == 3
        assert "Message 1" in self.log_messages[0]
        assert "Message 2" in self.log_messages[1]
        assert "Message 3" in self.log_messages[2]

    def test_logger_level_filtering(self):
        """Test that log level filtering works."""
        # Remove previous handler and add one with INFO level
        logger.remove(self.handler_id)
        self.log_messages = []

        def log_sink(message):
            self.log_messages.append(message)

        self.handler_id = logger.add(
            log_sink,
            format="{level} | {message}",
            level="INFO"
        )

        # Debug should be filtered out
        logger.debug("Debug message")
        assert len(self.log_messages) == 0

        # Info should be captured
        logger.info("Info message")
        assert len(self.log_messages) == 1

    def test_logger_with_exception(self):
        """Test logger with exception information."""
        try:
            raise ValueError("Test exception")
        except ValueError:
            logger.exception("An error occurred")

        assert len(self.log_messages) == 1
        assert "ERROR" in self.log_messages[0]
        assert "An error occurred" in self.log_messages[0]


class TestStandardLogging:
    """Test standard Python logging configuration."""

    def setup_method(self):
        """Setup for each test."""
        # Create a string buffer to capture log output
        self.log_buffer = StringIO()
        self.handler = logging.StreamHandler(self.log_buffer)
        self.handler.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        self.handler.setFormatter(formatter)

        # Create a test logger
        self.test_logger = logging.getLogger('test_logger')
        self.test_logger.setLevel(logging.DEBUG)
        self.test_logger.addHandler(self.handler)

    def teardown_method(self):
        """Cleanup after each test."""
        self.test_logger.removeHandler(self.handler)
        self.handler.close()

    def test_standard_logger_info(self):
        """Test standard logger info level."""
        self.test_logger.info("Test info message")
        log_output = self.log_buffer.getvalue()

        assert "INFO" in log_output
        assert "Test info message" in log_output
        assert "test_logger" in log_output

    def test_standard_logger_debug(self):
        """Test standard logger debug level."""
        self.test_logger.debug("Test debug message")
        log_output = self.log_buffer.getvalue()

        assert "DEBUG" in log_output
        assert "Test debug message" in log_output

    def test_standard_logger_warning(self):
        """Test standard logger warning level."""
        self.test_logger.warning("Test warning message")
        log_output = self.log_buffer.getvalue()

        assert "WARNING" in log_output
        assert "Test warning message" in log_output

    def test_standard_logger_error(self):
        """Test standard logger error level."""
        self.test_logger.error("Test error message")
        log_output = self.log_buffer.getvalue()

        assert "ERROR" in log_output
        assert "Test error message" in log_output

    def test_standard_logger_critical(self):
        """Test standard logger critical level."""
        self.test_logger.critical("Test critical message")
        log_output = self.log_buffer.getvalue()

        assert "CRITICAL" in log_output
        assert "Test critical message" in log_output

    def test_standard_logger_with_exception(self):
        """Test standard logger with exception."""
        try:
            raise RuntimeError("Test exception")
        except RuntimeError:
            self.test_logger.exception("Exception occurred")

        log_output = self.log_buffer.getvalue()
        assert "ERROR" in log_output
        assert "Exception occurred" in log_output
        assert "RuntimeError" in log_output

    def test_standard_logger_level_filtering(self):
        """Test that log level filtering works for standard logger."""
        # Set level to WARNING
        self.test_logger.setLevel(logging.WARNING)

        # Info and debug should be filtered
        self.test_logger.info("Info message")
        self.test_logger.debug("Debug message")
        log_output = self.log_buffer.getvalue()
        assert log_output == ""

        # Warning should pass through
        self.test_logger.warning("Warning message")
        log_output = self.log_buffer.getvalue()
        assert "WARNING" in log_output
        assert "Warning message" in log_output

    def test_logger_name_hierarchy(self):
        """Test logger name hierarchy."""
        parent_logger = logging.getLogger('parent')
        child_logger = logging.getLogger('parent.child')

        # Add handler to parent
        parent_buffer = StringIO()
        parent_handler = logging.StreamHandler(parent_buffer)
        parent_logger.addHandler(parent_handler)
        parent_logger.setLevel(logging.DEBUG)

        # Log to child
        child_logger.setLevel(logging.DEBUG)
        child_logger.info("Child message")

        # Should propagate to parent
        parent_output = parent_buffer.getvalue()
        assert "Child message" in parent_output

        # Cleanup
        parent_logger.removeHandler(parent_handler)


class TestModuleLoggingIntegration:
    """Test logging integration in actual modules."""

    def test_gpu_manager_uses_standard_logging(self):
        """Test that gpu_manager uses standard logging."""
        # Import the module
        from src.utils import gpu_manager

        # Check that it has a logger
        assert hasattr(gpu_manager, 'logger')
        assert isinstance(gpu_manager.logger, logging.Logger)

    def test_parallel_executor_uses_standard_logging(self):
        """Test that parallel_executor uses standard logging."""
        # Import the module
        from src.utils import parallel_executor

        # Check that it has a logger
        assert hasattr(parallel_executor, 'logger')
        assert isinstance(parallel_executor.logger, logging.Logger)

    def test_strategy_modules_use_loguru(self):
        """Test that strategy modules use loguru."""
        from src.strategies import semantic, hybrid, multisignal

        # These modules import logger from loguru
        # We can verify by checking if they have the logger
        assert hasattr(semantic, 'logger')
        assert hasattr(hybrid, 'logger')
        assert hasattr(multisignal, 'logger')

    def test_model_modules_use_loguru(self):
        """Test that model modules use loguru."""
        from src.models import embedders, rerankers, bm25

        # These modules import logger from loguru
        assert hasattr(embedders, 'logger')
        assert hasattr(rerankers, 'logger')
        assert hasattr(bm25, 'logger')


class TestLoggerConfiguration:
    """Test logger configuration scenarios."""

    def test_multiple_handlers_configuration(self):
        """Test configuring multiple log handlers."""
        # Remove default handlers
        logger.remove()

        # Add multiple sinks
        messages_info = []
        messages_error = []

        def info_sink(message):
            messages_info.append(message)

        def error_sink(message):
            messages_error.append(message)

        logger.add(info_sink, level="INFO", format="{message}")
        logger.add(error_sink, level="ERROR", format="{message}")

        # Log different levels
        logger.info("Info message")
        logger.error("Error message")

        # Info sink should have both
        assert len(messages_info) == 2

        # Error sink should only have error
        assert len(messages_error) == 1
        assert "Error message" in messages_error[0]

    def test_file_logging_configuration(self, tmp_path):
        """Test logging to a file."""
        # Remove default handlers
        logger.remove()

        # Add file handler
        log_file = tmp_path / "test.log"
        logger.add(str(log_file), level="DEBUG", format="{level} | {message}")

        # Log some messages
        logger.info("Test file log")
        logger.debug("Debug file log")

        # Read the file
        log_content = log_file.read_text()

        assert "Test file log" in log_content
        assert "Debug file log" in log_content
        assert "INFO" in log_content
        assert "DEBUG" in log_content

    def test_logger_context_binding(self):
        """Test logger context binding."""
        # Remove default handlers
        logger.remove()

        messages = []

        def sink(message):
            messages.append(str(message))

        logger.add(sink, format="{extra[user]} | {message}")

        # Bind context
        user_logger = logger.bind(user="Alice")
        user_logger.info("Logged in")

        assert len(messages) == 1
        assert "Alice" in messages[0]
        assert "Logged in" in messages[0]
