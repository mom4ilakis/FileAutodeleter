from unittest.mock import patch
from click.testing import CliRunner
from script import delete_old_files_command


def test_delete_old_files_by_date():
    runner = CliRunner()
    with patch('os.remove') as p:
        result = runner.invoke(delete_old_files_command, '--date 28.3.2022')
        assert result
        assert p
