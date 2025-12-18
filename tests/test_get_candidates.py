import pytest
from unittest.mock import Mock, patch
from app.entry_points.commands.get_candidates_command import GetCandidatesCommand

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_execute_prints_candidates_found(capsys):
    # Arrange
    loader = Mock()
    presenter = Mock()
    loader.fetch.return_value = ['cand1', 'cand2']
    presenter.build_lines.side_effect = ['Candidate 1 info', 'Candidate 2 info']
    cmd = GetCandidatesCommand(loader, presenter)

    # Act
    await cmd.execute([])

    # Assert
    out = capsys.readouterr().out
    assert "Retrieved 2 candidates" in out
    assert "Candidate 1 info" in out
    assert "Candidate 2 info" in out

@pytest.mark.asyncio
async def test_execute_prints_no_candidates_found(capsys):
    loader = Mock()
    presenter = Mock()
    loader.fetch.return_value = []
    cmd = GetCandidatesCommand(loader, presenter)

    await cmd.execute([])

    out = capsys.readouterr().out
    assert "No candidates were found." in out

@pytest.mark.asyncio
async def test_execute_handles_exception_and_logs(capsys):
    loader = Mock()
    presenter = Mock()
    loader.fetch.side_effect = Exception("DB error")
    cmd = GetCandidatesCommand(loader, presenter)

    with patch("app.entry_points.commands.get_candidates_command.logger") as logger_mock:
        await cmd.execute([])
        out = capsys.readouterr().out
        assert "We were unable to retrieve candidate information" in out
        assert logger_mock.exception.called