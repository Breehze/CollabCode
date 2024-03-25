import docker
import json
import asyncio
from datetime import datetime, timedelta

class containerManager:
    def __init__(self,image_cont_ratio : dict):
        self.dock_instance = docker.from_env()
        self.cont_pool = {}
        with open('utils/seccomp.json','r') as out:
            seccomp_conf = json.load(out)
        for image,cont_amount in image_cont_ratio.items():
            spec_cont_pool = []
            for i in range(cont_amount):
                new_cont = self.dock_instance.containers.run(image = image,command="tail -f /dev/null", detach = True, name = f"{image[:3]}_N{i}",network_disabled = True,read_only = True, mem_limit = "100m")
                spec_cont_pool.append(new_cont)
            self.cont_pool.update({image : spec_cont_pool})
     
    async def run_code_async(self,lang,script):
        """Only python for now"""
        if len(self.cont_pool[lang]) < 1:
            return "No container available"
        event_loop = asyncio.get_event_loop()
        container = self.cont_pool[lang][0]
        self.cont_pool[lang].remove(container)
        try:
            async with asyncio.timeout(5):
                result = await event_loop.run_in_executor( None , lambda :container.exec_run(f"python -c \"{script}\""))
        except asyncio.TimeoutError: 
            ditch_process = await event_loop.run_in_executor(None, lambda : container.exec_run("sh -c 'ps x | grep [p]ython'"))
            p_to_kill = ditch_process.output.decode().split()[0]
            await event_loop.run_in_executor(None , lambda : container.exec_run(f"kill -SIGKILL {p_to_kill}"))
            self.cont_pool[lang].append(container)
            return "Process killed"
        self.cont_pool[lang].append(container)
        return result.output.decode('utf-8')

            
    def teardown(self):
        for _,cont_pool in self.cont_pool.items():
            for cont_id in cont_pool:
                cont_id.stop()
                cont_id.remove()
