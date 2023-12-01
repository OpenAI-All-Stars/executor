import os
from pathlib import Path
import socket
import docker
import httpx
import pytest


@pytest.fixture(scope='session')
def app_url(repo_root_path, get_free_port, healthcheck) -> str:
    app_name = os.environ.get('DOCKER_TAG', 'executor')
    client = docker.from_env()
    img, _ = client.images.build(path=repo_root_path, tag=app_name)
    ports = {}
    for part in img.attrs['Config']['ExposedPorts']:
        port = get_free_port()
        ports[part] = port
    url = f'http://{socket.gethostname()}:{port}'
    container = client.containers.run(
        app_name,
        'executor server',
        detach=True,
        remove=True,
        auto_remove=True,
        publish_all_ports=True,
        ports=ports,
    )
    try:
        if not healthcheck(f'{url}/ping', 10):
            raise Exception('ping failed')
        yield url
    finally:
        print(container.logs().decode())
        container.stop()


@pytest.fixture(scope='session')
def repo_root_path() -> str:
    return str(Path(__file__).parent.parent.absolute())


@pytest.fixture(scope='session')
def http(app_url):
    with httpx.Client(base_url=app_url) as client:
        yield client


@pytest.fixture(scope='session')
def get_free_port():
    def _get() -> int:
        sock = socket.socket()
        sock.bind(('', 0))
        return sock.getsockname()[1]
    return _get


@pytest.fixture(scope='session')
def healthcheck() -> bool:
    def _check(ping_url: str, retries: int):
        import time
        with httpx.Client() as client:
            for _ in range(retries):
                try:
                    resp = client.get(ping_url, timeout=1)
                    if resp.status_code == 200:
                        return True
                except httpx.HTTPError:
                    pass
                time.sleep(1)
        return False
    return _check
