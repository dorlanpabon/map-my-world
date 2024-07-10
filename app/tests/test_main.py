import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_root(client: AsyncClient):
    response = await client.get("../")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Map My World API"}


########################################################################################
# region Categories
########################################################################################

@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    response = await client.get("/categories/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    name = "Test Category"
    response = await client.post(
        "/categories/",
        json={"name": name}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name


@pytest.mark.asyncio
async def test_get_categories_after_create(client: AsyncClient):
    response = await client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Category"

@pytest.mark.asyncio
async def test_create_duplicate_category(client: AsyncClient):
    response = await client.post(
        "/categories/",
        json={"name": "Test Category"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Category name must be unique"}

@pytest.mark.asyncio
async def test_read_category(client: AsyncClient):
    # First, create a category to read
    create_response = await client.post(
        "/categories/",
        json={"name": "Read Test Category"}
    )
    category_id = create_response.json()["id"]

    # Now read the created category
    response = await client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Read Test Category"

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient):
    # First, create a category to delete
    create_response = await client.post(
        "/categories/",
        json={"name": "Delete Test Category"}
    )
    category_id = create_response.json()["id"]

    # Now delete the created category
    response = await client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == category_id

    # Verify the category is not in the database anymore
    get_response = await client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Category not found"}
#endregion

########################################################################################
# region Locations
########################################################################################


@pytest.mark.asyncio
async def test_create_location(client: AsyncClient):
    location_data = {"latitude": 10.0, "longitude": 20.0}
    response = await client.post("/locations/", json=location_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["latitude"] == location_data["latitude"]
    assert response_data["longitude"] == location_data["longitude"]
    assert "id" in response_data
    assert "created_at" in response_data

@pytest.mark.asyncio
async def test_read_locations(client: AsyncClient):
    response = await client.get("/locations/")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    assert len(locations) >= 0  # Puede estar vacío si no hay datos

@pytest.mark.asyncio
async def test_read_location(client: AsyncClient):
    # Primero, crea una ubicación para asegurarte de que hay algo que leer
    location_data = {"latitude": 10.0, "longitude": 20.0}
    create_response = await client.post("/locations/", json=location_data)
    location_id = create_response.json()["id"]

    # Luego, lee la ubicación por ID
    response = await client.get(f"/locations/{location_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == location_id
    assert response_data["latitude"] == location_data["latitude"]
    assert response_data["longitude"] == location_data["longitude"]

@pytest.mark.asyncio
async def test_read_nonexistent_location(client: AsyncClient):
    response = await client.get("/locations/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Location not found"}

@pytest.mark.asyncio
async def test_delete_location(client: AsyncClient):
    # Primero, crea una ubicación para poder eliminarla
    location_data = {"latitude": 10.0, "longitude": 20.0}
    create_response = await client.post("/locations/", json=location_data)
    location_id = create_response.json()["id"]

    # Luego, elimina la ubicación por ID
    delete_response = await client.delete(f"/locations/{location_id}")
    assert delete_response.status_code == 200
    response_data = delete_response.json()
    assert response_data["id"] == location_id

    # Verifica que la ubicación ya no existe
    get_response = await client.get(f"/locations/{location_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Location not found"}
#endregion

########################################################################################
# region Recommendations
########################################################################################

@pytest.mark.asyncio
async def test_get_fresh_recommendations(client: AsyncClient):
    response = await client.get("/recommendations/fresh/")
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

@pytest.mark.asyncio
async def test_get_never_reviewed_recommendations(client: AsyncClient):
    response = await client.get("/recommendations/never-reviewed/")
    assert response.status_code == 200
    recommendations = response.json()
    assert isinstance(recommendations, list)

@pytest.mark.asyncio
async def test_create_relation(client: AsyncClient):
    review_data = {"location_id": 1, "category_id": 1}
    response = await client.post("/recommendations/", json=review_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["location_id"] == review_data["location_id"]
    assert response_data["category_id"] == review_data["category_id"]
    assert "id" in response_data
    assert "last_reviewed" in response_data

@pytest.mark.asyncio
async def test_create_review(client: AsyncClient):
    # Primero, crea una relación para asegurar que hay algo que revisar
    review_data = {"location_id": 1, "category_id": 1}
    create_response = await client.post("/recommendations/", json=review_data)
    review_id = create_response.json()["id"]

    # Luego, crea una revisión para la relación
    response = await client.post(f"/recommendations/{review_id}/review")
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == review_id
    assert "last_reviewed" in response_data

@pytest.mark.asyncio
async def test_create_relation_with_review(client: AsyncClient):
    review_data = {"location_id": 1, "category_id": 1}
    response = await client.post("/recommendations/with-review/", json=review_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["location_id"] == review_data["location_id"]
    assert response_data["category_id"] == review_data["category_id"]
    assert "id" in response_data
    assert "last_reviewed" in response_data

@pytest.mark.asyncio
async def test_get_review(client: AsyncClient):
    # Primero, crea una relación para asegurar que hay algo que revisar
    review_data = {"location_id": 1, "category_id": 1}
    create_response = await client.post("/recommendations/", json=review_data)
    review_id = create_response.json()["id"]

    # Luego, obtén la revisión por ID
    response = await client.get(f"/recommendations/{review_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == review_id

@pytest.mark.asyncio
async def test_get_nonexistent_review(client: AsyncClient):
    response = await client.get("/recommendations/999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Review not found"}

@pytest.mark.asyncio
async def test_delete_review(client: AsyncClient):
    # Primero, crea una relación para poder eliminarla
    review_data = {"location_id": 1, "category_id": 1}
    create_response = await client.post("/recommendations/", json=review_data)
    review_id = create_response.json()["id"]

    # Luego, elimina la revisión por ID
    delete_response = await client.delete(f"/recommendations/{review_id}")
    assert delete_response.status_code == 200
    response_data = delete_response.json()
    assert response_data["id"] == review_id

    # Verifica que la revisión ya no existe
    get_response = await client.get(f"/recommendations/{review_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Review not found"}
# endregion


