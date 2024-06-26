import pytest

import app.api.v1.endpoints.dough.crud as dough_crud
import app.api.v1.endpoints.sauce.crud as sauce_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_type_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.sauce.schemas import SauceCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
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

    update_pizza_type_name = 'test'
    update_pizza_type_price = 8
    update_pizza_type_description = 'new pizza'

    number_of_pizza_types_before = len(pizza_type_crud.get_all_pizza_types(db))
    number_of_doughs_before = len(dough_crud.get_all_doughs(db))
    number_of_sauces_before = len(sauce_crud.get_all_sauces(db))

    # Arrange: Instantiate a new dough, a new sauce and pizza_type object
    dough = DoughCreateSchema(name='test_dough', price=1.5, description='new dough', stock=20)
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    sauce = SauceCreateSchema(name='tomato', price=1.0, description='tomato', stock=30)
    db_sauce = sauce_crud.create_sauce(sauce, db)
    created_sauce_id = db_sauce.id

    pizza_type = PizzaTypeCreateSchema(name=new_pizza_type_name, price=new_pizza_type_price,
                                       description=new_pizza_type_description, dough_id=created_dough_id,
                                       sauce_id=created_sauce_id)

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

    # Act: Update pizza_type in database
    update_pizza = pizza_type_crud.update_pizza_type(read_pizza_type,
                                                     PizzaTypeCreateSchema(name=update_pizza_type_name,
                                                                           price=update_pizza_type_price,
                                                                           description=update_pizza_type_description,
                                                                           dough_id=created_dough_id,
                                                                           sauce_id=created_sauce_id),
                                                     db)

    # Assert: Old pizza_type was updated
    assert update_pizza.name == update_pizza_type_name
    assert update_pizza.price == update_pizza_type_price
    assert update_pizza.description == update_pizza_type_description

    # Act: Delete pizza_type from database
    pizza_type_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct number of pizza_types in database after deletion
    pizza_types = pizza_type_crud.get_all_pizza_types(db)
    assert len(pizza_types) == number_of_pizza_types_before

    # Assert: Correct pizza_type was deleted from database
    deleted_pizza_type = pizza_type_crud.get_pizza_type_by_id(created_pizza_type_id, db)
    assert deleted_pizza_type is None

    # Act: Delete sauce
    sauce_crud.delete_sauce_by_id(created_sauce_id, db)

    # Assert: Correct number of sauces in database after deletion
    sauces = sauce_crud.get_all_sauces(db)
    assert len(sauces) == number_of_sauces_before

    # Assert: Correct sauce was deleted from database
    deleted_sauce = sauce_crud.get_sauce_by_id(created_sauce_id, db)
    assert deleted_sauce is None

    # Act: Delete dough
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct number of doughs in database after deletion
    doughs = dough_crud.get_all_doughs(db)
    assert len(doughs) == number_of_doughs_before

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None
