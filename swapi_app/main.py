from work_db import paste_to_db
from math import ceil
import asyncio
import aiohttp


URL = 'https://swapi.dev/api/people/'


async def get_json(client, *args, **kwargs):
    response = await client.get(*args, **kwargs)
    json_data = await response.json()
    return json_data


async def get_page_meta():
    async with aiohttp.ClientSession() as client:
        info = await get_json(client, URL)
        character_on_page = len(info['results'])
        all_character = info['count']
        max_page = ceil(all_character / character_on_page)
        return max_page, character_on_page


MAX_PAGE_COUNT, CHARACTER_ON_PAGE = asyncio.run(get_page_meta())


async def get_listed_data(client, field, *links):
    if not links:
        return
    coroutines = [get_json(client, link) for link in links]
    json_data = await asyncio.gather(*coroutines)
    data = ', '.join(json_field[field] for json_field in json_data)
    return data


async def get_character_data(client, character, character_id):
    data = await asyncio.gather(get_listed_data(client, 'name', character['homeworld']),
                                get_listed_data(client, 'title', character['films']),
                                get_listed_data(client, 'name', character['species']),
                                get_listed_data(client, 'name', character['starships']),
                                get_listed_data(client, 'name', character['vehicles']))

    character_data = dict(id=character_id,
                          birth_year=character['birth_year'],
                          eye_color=character['eye_color'],
                          gender=character['gender'],
                          hair_color=character['hair_color'],
                          height=character['height'],
                          mass=character['mass'],
                          name=character['name'],
                          skin_color=character['skin_color'],
                          homeworld=data[0],
                          films=data[1],
                          species=data[2],
                          starship=data[3],
                          vehicles=data[4]
                          )

    return character_data


async def get_character(client, page):
    params = {'page': page}
    start_position = (page * CHARACTER_ON_PAGE) - (CHARACTER_ON_PAGE - 1)
    response = await get_json(client, URL, params=params)
    characters = [await get_character_data(client, character, id_) for id_, character in enumerate(response['results'],
                                                                                                   start=start_position)]
    return characters


async def main():
    async with aiohttp.ClientSession() as client:
        for page in range(1, MAX_PAGE_COUNT + 1):
            character_coro = get_character(client, page)
            paste_to_db_coroutine = paste_to_db(character_coro)
            asyncio.create_task(paste_to_db_coroutine)

    tasks = asyncio.all_tasks() - {asyncio.current_task(), }
    for task in tasks:
        await task


if __name__ == '__main__':
    asyncio.run(main())

