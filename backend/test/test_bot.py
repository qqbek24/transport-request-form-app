import pytest
import os
import sys
from pathlib import Path
from freezegun import freeze_time
from main import Task
from rpa_bot.log import lte, log
from rpa_bot.utils import task_kill
# # For debug console issue while launching GUI apps
# import faulthandler 
# faulthandler.disable()

pytest.bot = None

@pytest.fixture
def bot():
    pytest.bot = Task(sysargs=['bot_mode=dev', 'log_debug=True'])
    return pytest.bot

def test_process(bot: Task):
    with bot:
        bot.process()

def error():
    raise Exception("Expected error message")
def test_expected_error(bot: Task):
    with pytest.raises(Exception) as exc_info:
        error()
    assert exc_info.value.args[0] == "Expected error message"

def test_clear():
    """Ending of test - close all windows opened by prevoius tests"""
    task_kill("excel.exe")
