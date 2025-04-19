from httpx import AsyncClient, ASGITransport 
import asyncio, pytest

from src.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_get_tables():
    async with AsyncClient(transport=ASGITransport(app=app), 
    base_url="http://test") as aclient:
        response = await aclient.get(url='/tables/')
        assert response.status_code == 200
        data = response.json()
        
        assert type(data['response']) == list
        


@pytest.mark.asyncio
async def test_post_table():
    async with AsyncClient(transport=ASGITransport(app=app), 
    base_url="http://test") as aclient:
        response = await aclient.post(url='/tables/', json={
            "id":0,
            "name":'Ss',
            "seats":2,
            "location":"sdkljh",
            })
        assert response.status_code == 200
        data = response.json()
        
        assert data['response'] == "Table has been added"

@pytest.mark.asyncio
async def test_delete_table():
    async with AsyncClient(transport=ASGITransport(app=app), 
    base_url="http://test") as aclient:
        response = await aclient.delete(url='/tables/', params={"id": 1})
            
        assert response.status_code == 200
        data = response.json()
        
        assert data['response'] == "Table has been deleted"        

