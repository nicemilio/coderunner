import docker
import os
import json

def run_in_docker(script_path):
    client = docker.from_env()
    
    abs_path = os.path.abspath(script_path)
    container_path = "/app/user_script.py"

    volumes = {
        abs_path: {"bind": container_path, "mode": "ro"}
    }

    try:
        container = client.containers.run(
            image="test_container:latest",
            volumes=volumes,
            detach=True,
            remove=True,
            stderr=True,
        )
        logs = container.logs(stream=True)
        output = "".join([line.decode("utf-8") for line in logs])

        # Lies den JSON-Testreport aus (ggf. über shared volume)
        # Optional:
        # report = json.load(open("path_to_report.json"))
        
        return {"success": True, "output": output}

    except docker.errors.ContainerError as e:
        return {"success": False, "error": str(e)}