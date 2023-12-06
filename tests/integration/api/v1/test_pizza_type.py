import pytest

import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_pizza_type_create_read_delete(db):
    new_pizza_type_name = 'test'
    new_pizza_type_price = 8
    new_pizza_type_description = 'Pepsi'
    number_of_pizza_types_before = len(pizza_type_crud.get_all_pizza_types(db))
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))

    # Arrange: Instantiate a new dough and pizza_type object
    dough = DoughCreateSchema(name='test_dough', price=1.5, description='new dough', stock=20)
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    pizza_type = PizzaTypeCreateSchema(name=new_pizza_type_name, price=new_pizza_type_price,
                                       description=new_pizza_type_description,
                                       dough_id=created_dough_id)

    # # Act: Add pizza_type to database
    db_pizza_type = pizza_type_crud.create_pizza_type(pizza_type, db)
    created_pizza_type_id = db_pizza_type.id

    # Assert: One more pizza_type in database
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before + 1

    # Act: Re-read pizza_type from database
    read_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct pizza_type was stored in database
    assert read_pizza_type.id == created_pizza_type_id
    assert read_pizza_type.name == new_pizza_type_name

    # Act: Delete pizza_type
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct number of pizza_types in database after deletion
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before

    # Assert: Correct pizza_type was deleted from database
    deleted_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)
    assert deleted_pizza_type is None

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None
