import requests
import time

VM_NAME = 'testvm2'

header = {
'Content-Type': 'application/json',
'Authorization': 'Bearer '
}

body = {
	"location":"westus",
	"properties": {
    "hardwareProfile": {
      "vmSize": "Standard_D3"
    },
    "storageProfile": {
      "imageReference": {
        "sku": "18.04-LTS",
        "publisher": "Canonical",
        "version": "latest",
        "offer": "UbuntuServer"
      },
      "osDisk": {
        "caching": "ReadWrite",
        "managedDisk": {
          "storageAccountType": "Standard_LRS"
        },
        "name": "checkname",
        "createOption": "FromImage"
      }
    },
    "networkProfile": {
      "networkInterfaces": [
        {
          "id": "/subscriptions/9221ca11-b03f-45b9-adf0-15feab4b7a3d/resourceGroups/newgroup/providers/Microsoft.Network/networkInterfaces/Nic",
          "properties": {
            "primary": 'true'
          }
        }
      ]
    },
    "osProfile": {
      "adminUsername": "srini",
      "computerName": "VkkooM",
      "adminPassword": "Srini123#",
      "customData" : "I2Nsb3VkLWNvbmZpZwpwYWNrYWdlX3VwZ3JhZGU6IHRydWUKcGFja2FnZXM6CiAgLSBuZ2lueAogIC0gbm9kZWpzCiAgLSBucG0Kd3JpdGVfZmlsZXM6CiAgLSBvd25lcjogd3d3LWRhdGE6d3d3LWRhdGEKICAgIHBhdGg6IC9ldGMvbmdpbngvc2l0ZXMtYXZhaWxhYmxlL2RlZmF1bHQKICAgIGNvbnRlbnQ6IHwKICAgICAgc2VydmVyIHsKICAgICAgICBsaXN0ZW4gODA7CiAgICAgICAgbG9jYXRpb24gLyB7CiAgICAgICAgICBwcm94eV9wYXNzIGh0dHA6Ly9sb2NhbGhvc3Q6MzAwMDsKICAgICAgICAgIHByb3h5X2h0dHBfdmVyc2lvbiAxLjE7CiAgICAgICAgICBwcm94eV9zZXRfaGVhZGVyIFVwZ3JhZGUgJGh0dHBfdXBncmFkZTsKICAgICAgICAgIHByb3h5X3NldF9oZWFkZXIgQ29ubmVjdGlvbiBrZWVwLWFsaXZlOwogICAgICAgICAgcHJveHlfc2V0X2hlYWRlciBIb3N0ICRob3N0OwogICAgICAgICAgcHJveHlfY2FjaGVfYnlwYXNzICRodHRwX3VwZ3JhZGU7CiAgICAgICAgfQogICAgICB9CiAgLSBvd25lcjogYXp1cmV1c2VyOmF6dXJldXNlcgogICAgcGF0aDogL2hvbWUvYXp1cmV1c2VyL215YXBwL2luZGV4LmpzCiAgICBjb250ZW50OiB8CiAgICAgIHZhciBleHByZXNzID0gcmVxdWlyZSgnZXhwcmVzcycpCiAgICAgIHZhciBhcHAgPSBleHByZXNzKCkKICAgICAgdmFyIG9zID0gcmVxdWlyZSgnb3MnKTsKICAgICAgY29uc3QgaHR0cCA9IHJlcXVpcmUoJ2h0dHAnKTsKICAgICAgY29uc3QgZnMgPSByZXF1aXJlKCdmcycpOwogICAgICBjb25zdCBodHRwcyA9IHJlcXVpcmUoJ2h0dHBzJyk7CgogICAgICBodHRwcy5nZXQoJ2h0dHBzOi8vbmV3dGVzdGh0bWwuYmxvYi5jb3JlLndpbmRvd3MubmV0L25ld2NvbnRhaW5lci9nZW5lcmF0ZWRfcGFnZWZyb21zcGVlY2guaHRtbCcsIChyZXMpID0+IHsKICAgICAgICBjb25zb2xlLmxvZygnc3RhdHVzQ29kZTonLCByZXMuc3RhdHVzQ29kZSk7CiAgICAgICAgY29uc29sZS5sb2coJ2hlYWRlcnM6JywgcmVzLmhlYWRlcnMpOwoKICAgICAgICByZXMub24oJ2RhdGEnLCAoZCkgPT4gewogICAgICAgIGZzLndyaXRlRmlsZVN5bmMoJ2ZpbGUuaHRtbCcsIGQpOwogICAgICAgIH0pOwoKICAgICAgfSkub24oJ2Vycm9yJywgKGUpID0+IHsKICAgICAgY29uc29sZS5lcnJvcihlKTsKICAgICAgfSk7CgoKCgoKICAgICAgYXBwLmdldCgnLycsIGZ1bmN0aW9uIChyZXEsIHJlcykgewogICAgICAgIHJlcy5zZW5kRmlsZSgnZmlsZS5odG1sJywgeyByb290IDogX19kaXJuYW1lfSkKICAgICAgfSkKICAgICAgYXBwLmxpc3RlbigzMDAwLCBmdW5jdGlvbiAoKSB7CiAgICAgICAgY29uc29sZS5sb2coJ0hlbGxvIHdvcmxkIGFwcCBsaXN0ZW5pbmcgb24gcG9ydCAzMDAwIScpCiAgICAgIH0pCnJ1bmNtZDoKICAtIHNlcnZpY2UgbmdpbnggcmVzdGFydAogIC0gY2QgIi9ob21lL2F6dXJldXNlci9teWFwcCIKICAtIG5wbSBpbml0CiAgLSBucG0gaW5zdGFsbCBleHByZXNzIC15CiAgLSBub2RlanMgaW5kZXguanM="
    }
  }
}

url = 'https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/newgroup/providers/Microsoft.Compute/virtualMachines/'+VM_NAME+'?api-version=2017-12-01'

data = requests.put(url,headers=header,json=body)

print(data.text)

time.sleep(100)

data2 = requests.get('https://management.azure.com/subscriptions/9221ca11-b03f-45b9-adf0-15feab4b7a3d/resourceGroups/newgroup/providers/Microsoft.Network/publicIPAddresses/IPAddress?api-version=2019-12-01',headers=header)

# print(data2.text)

data3 = eval(str(data2.text))

print(data3['properties']['ipAddress'])




