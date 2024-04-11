**Tool that helps you update your server with the latest in tibia.**
*things it can do*:

* get the information of the latest items added to tibia by modifying items.xml, weapons.xml and movements.xml.
* add missing outfits
* add missing mounts
1. <u>first identify whether the server uses client ID or server ID in the items.xml file.</u>
   in my case, the server I am using uses client id, therefore, I have to get which is the client depending on the server id of each of my items, since tibia fandom uses server id.
   there must be many ways to get these client ids and server ids, in my case, I used otcv8 and created this simple script that returns a json with the clientid and serverid

```lua
g_things.loadOtb('items.otb') -- path to the server otb (the one found with items.xml)

local lista = {}

for i = 1, 60000 do
    local item = Item.create(i)
    local serverId = item:getServerId()
    if serverId ~= 0 then
        rawset(lista, tostring(item:getId()), serverId)
    end
end

g_resources.writeFileContents("DumpIDS.json", json.encode(lista, 1))
```

    Estructura del archivo resultante:


```json
{
 "19035": 21352,
 "31197": 35911,
 "8335": 9251,
 "32810": 38561,
 "30701": 35415,
 "223": 7578
}
```

2. config ***path_serverIDS*** and ***path_itemsXML*** variable in *itemsConverter.py* and **run**