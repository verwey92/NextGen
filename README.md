# NextGen
Discord Bot
## Command List
!fetch_messages @username will scan the server and return the number of messages the target user has sent in the server over the last 30 days.


## Re-Deploy Function Docs:

```sh
#Run all in LINODE Terminal
git pull #Pull Latest Changes from Git Hub
docker stop nextgen-discord #End the current Container Process
docker rm nextgen-discord #Remove the current Container
docker build -t nextgen . #Build udpated version of the image
docker run -d -e TOKEN=MYTOKEN --name nextgen-discord nextgen #Run container with latest image
```
## Steps to Re-Deploy

```sh
#SSH into Linode Terminal
update_nextgen
```