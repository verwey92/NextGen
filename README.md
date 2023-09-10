# NextGen

Discord Bot

## Command List

'!usermessages @username' 

'!fetch_messages #channelname' 

'!voice_stats' Will track user join and leave events from voice chats in the server. Command will return total users who entered the voice chats and the average time spent for all users.

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