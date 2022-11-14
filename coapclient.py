import asyncio
from aiocoap import *

async def coapgetlampstatus(url):
    print('coapgetlampstatus on', url)
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri=url)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:', e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))
        return response.payload

async def coapsetlampstatus(url, value):
    print('coapsetlampstatus on', url, 'with value', value)
    protocol = await Context.create_client_context()
    request = Message(code=PUT, uri=url, payload=value)

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:', e)
    else:
        print('Result: %s'%(response.code))
        
async def main():
   await coapsetlampstatus('coap://lamp1c.irst.be/lamp/dimming', b'0')
   
   val = await coapgetlampstatus('coap://lamp1c.irst.be/lamp/dimming')
   print("retrieved lamp value:", val)

async def getlampstatus(lamp):
    val = await coapgetlampstatus(lamp)
    return val

async def setlampstatus(lamp,value):
    val = await coapsetlampstatus(lamp,str.encode(str(value)))

if __name__ == "__main__":
   asyncio.run(main())