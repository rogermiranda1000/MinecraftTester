# WatchWolf - Client & Clients Manager [![CodeFactor](https://www.codefactor.io/repository/github/rogermiranda1000/watchwolf-client/badge/dev)](https://www.codefactor.io/repository/github/rogermiranda1000/watchwolf-client/overview/dev)
A Python library to test Minecraft Plugins in the client side. For more information about WatchWolf check the [WatchWolf website](https://watchwolf.dev/).

## Dependencies
- [Docker](https://www.docker.com/get-started/)
- Python image: `docker pull nikolaik/python-nodejs`
- Build the image: `docker build --tag clients-manager .`

## Launch
- Run the docker container: `wsl_mode(){ echo "echo 'Hello world'" | powershell.exe >/dev/null 2>&1; return $?; } ; get_ip(){ wsl_mode; if [ $? -eq 0 ]; then echo '(Get-NetIPConfiguration |  Where-Object { $_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected" }).IPv4Address.IPAddress' | powershell.exe 2>/dev/null | tail -n2 | head -n1 | tr -d "\n" | tr -d "\r"; else hostname -I | awk '{print $1}';fi } ; sudo docker run -i --rm --name ClientsManager -p 7000-7199:7000-7199 --env MACHINE_IP=$(get_ip) --env PUBLIC_IP=$(curl ifconfig.me) clients-manager:latest`
