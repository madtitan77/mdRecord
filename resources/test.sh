#!/bin/bash


curl -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"madtitan.mdrecord.id","enabled":true},"id":1}' \
  http://<kodi-ip>:8080/jsonrpc
