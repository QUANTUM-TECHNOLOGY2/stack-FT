import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from deepseek_python_20260708_1a153f import get_user_profile, generate_file_preview


def test_generate_file_preview_handles_text():
    preview = generate_file_preview(b'hello world', 'text/plain')
    assert preview['text'] == 'hello world'


def test_get_user_profile_returns_none_for_missing_user():
    assert get_user_profile('missing-user') is None
