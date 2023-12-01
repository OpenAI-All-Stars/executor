import pytest


@pytest.mark.parametrize(
    'command, expected',
    [
        ('pwd', {'stderr': '', 'stdout': '/app\n'}),
        ('echo a > b && cat b', {'stderr': '', 'stdout': 'a\n'}),
        ('sudo kill 1', {'stdout': '', 'stderr': '/bin/sh: 1: sudo: not found\n'}),
        ('kill 1 -9', {'stdout': '', 'stderr': '/bin/sh: 1: kill: No such process\n\n'}),
    ],
)
def test_success(http, command, expected):
    resp = http.post(
        '/execute-bash',
        json={
            'command': command,
        },
    )

    assert resp.status_code == 200
    assert resp.json() == expected
