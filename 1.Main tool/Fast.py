import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

async def fetch(session, url, business_name):
    try:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            agent_name = soup.find(id='MainContent_lblResidentAgentName')
            return business_name, agent_name.text if agent_name else "Not Found"
    except Exception as e:
        return business_name, "Error"

async def main(input_dir, output_dir, csv_file_name):
    csv_file_path = os.path.join(input_dir, csv_file_name)
    data = pd.read_csv(csv_file_path)

    if 'Business Name' not in data.columns:
        print("Error: 'Business Name' column not found.")
        return

    data['Registered Agent'] = ""

    async with aiohttp.ClientSession() as session:
        tasks = []
        for business_name in data['Business Name'][:2000].dropna():
            url = f'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSearch.aspx?SearchType=1&EntityName={business_name}'
            task = asyncio.ensure_future(fetch(session, url, business_name))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

    for business_name, agent_name in responses:
        data.loc[data['Business Name'] == business_name, 'Registered Agent'] = agent_name

    # Remove unnecessary columns
    data = data[['Business Name', 'Registered Agent']]

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_file_name = f'results_{timestamp}.csv'
    output_file_path = os.path.join(output_dir, output_file_name)
    data.to_csv(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")

if __name__ == '__main__':
    input_dir = '/path/to/your/input/directory'
    output_dir = '/path/to/your/output/directory'
    csv_file_name = 'your_csv_file_name.csv'
    asyncio.run(main(input_dir, output_dir, csv_file_name))



# pyhton3 fast.py