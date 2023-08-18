from os import getenv
import requests
import aiohttp
from fastapi import HTTPException

ALPHAVANTAGE_APIKEY= getenv("ALPHAVANTAGE_APIKEY")

def sync_converter(from_currency: str, to_currency: str, price: float):
    url=f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}"

    try: 
        response = requests.get(url=url)
    except Exception as error: 
        raise HTTPException(status_code=400, detail=error)
    
    data = response.json()

    if "Realtime Currency Exchange Rate" not in data:
         raise HTTPException(status_code=404, detail=f"Realtime Currency Exchange Rate not in data!{data}")
    
    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    
    return price * exchange_rate
  

async def async_converter(from_currency: str, to_currency: str, price: float):
    url=f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}"

    try: 
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                 print("Response status:", response.status)
                 data = await response.json()
                 print("Response data:", data)

    except Exception as error: 
        raise HTTPException(status_code=400, detail=error)
    
    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(status_code=404, detail=f"Realtime Currency Exchange Rate not in data!{data}")
    
    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    
    return {to_currency: price * exchange_rate}