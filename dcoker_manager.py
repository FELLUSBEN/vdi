import docker

client = docker.from_env()
print(client.login(username="shovelmasterben", email="", password=""))
print(client.containers.list(all=True))

class manager:
    def __init__(self):
        pass
    def stop(self, pc):
        client.api.stop(client.containers.get("cont-" + str(pc.id)).id)
    def create(self, pc):
        try:
            client.containers.run("lscr.io/linuxserver/webtop:ubuntu-mate", name="cont-" + str(pc), shm_size="1g", hostname="terminalserver", ports={3000: int(pc)+8080})
        except Exception as e:
            client.api.start("cont-" + str(pc))

