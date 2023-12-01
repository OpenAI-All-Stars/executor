
from asyncio import create_subprocess_shell, subprocess
from fastapi import FastAPI

from executor.entities import ExecuteBashRequest, ExecuteBashResponse


app = FastAPI()


@app.get('/ping')
async def ping() -> str:
    return 'OK'


@app.post('/execute-bash')
async def execute_bash(request: ExecuteBashRequest) -> ExecuteBashResponse:
    proc = await create_subprocess_shell(
        request.command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return ExecuteBashResponse(
        stdout=stdout.decode(),
        stderr=stderr.decode(),
    )
