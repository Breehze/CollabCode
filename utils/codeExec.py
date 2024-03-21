import docker
import asyncio 


async def run_python(script : str) -> str:
    event_loop = asyncio.get_event_loop()
    client = docker.from_env() 
    container = await event_loop.run_in_executor (None, lambda :client.containers.run(
        image="python:3.11-slim",
        command=f"python -c \"{script}\"",
        detach=True,      
        mem_limit="50m",  
        network_disabled=True,     
    ))   
    result = await event_loop.run_in_executor(None,container.wait)
    output = await event_loop.run_in_executor(None,container.logs) 
    container.remove()
    decoded = output.decode()
    
    return decoded[:len(decoded)-1]



