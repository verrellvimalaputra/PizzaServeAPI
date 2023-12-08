import pytest

import app.api.v1.endpoints.user.crud as user_crud
import app.api.v1.endpoints.order.crud as order_crud
import app.api.v1.endpoints.pizza_type.crud as pizza_crud
import app.api.v1.endpoints.beverage.crud as beverage_crud
import app.api.v1.endpoints.dough.crud as dough_crud
from app.api.v1.endpoints.dough.schemas import DoughCreateSchema
from app.api.v1.endpoints.user.schemas import UserCreateSchema
from app.api.v1.endpoints.order.schemas import OrderCreateSchema
from app.api.v1.endpoints.order.address.schemas import AddressCreateSchema
from app.api.v1.endpoints.pizza_type.schemas import PizzaTypeCreateSchema
from app.api.v1.endpoints.beverage.schemas import BeverageCreateSchema
from app.api.v1.endpoints.order.schemas import OrderBeverageQuantityCreateSchema
from app.database.connection import SessionLocal


@pytest.fixture(scope='module')
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_order_create_read_delete(db):
    new_street = 'street'
    new_post_code = '123456'
    new_house_number = 1
    new_country = 'country'
    new_town = 'town'
    new_first_name = 'first'
    new_last_name = 'last'
    new_user_name = 'test'

    new_dough_name = 'dough_test'
    new_dough_price = 1.0
    new_dough_description = 'new dough'
    new_dough_stock = 20

    new_pizza_type_name = 'pizza_test'
    new_pizza_type_price = 8
    new_pizza_type_description = 'Pepsi'

    new_beverage_name = 'beverage_test'
    new_beverage_price = 8
    new_beverage_description = 'Pepsi'
    new_beverage_stock = 10

    number_of_users_before = len(user_crud.get_all_users(db))
    number_of_orders_before = len(order_crud.get_all_orders(db))

    user = UserCreateSchema(username=new_user_name)
    db_user = user_crud.create_user(user, db)
    created_user_id = db_user.id

    order = OrderCreateSchema(address=AddressCreateSchema(street=new_street, post_code=new_post_code,
                                                          house_number=new_house_number, country=new_country,
                                                          town=new_town,
                                                          first_name=new_first_name, last_name=new_last_name),
                              user_id=created_user_id)

    dough = DoughCreateSchema(name=new_dough_name, price=new_dough_price,
                              description=new_dough_description, stock=new_dough_stock)
    db_dough = dough_crud.create_dough(dough, db)
    created_dough_id = db_dough.id

    pizza_type = PizzaTypeCreateSchema(name=new_pizza_type_name, price=new_pizza_type_price,
                                       description=new_pizza_type_description, dough_id=created_dough_id)
    db_pizza_type = pizza_crud.create_pizza_type(pizza_type, db)
    created_pizza_type_id = db_pizza_type.id

    beverage = BeverageCreateSchema(name=new_beverage_name, price=new_beverage_price,
                                    description=new_beverage_description, stock=new_beverage_stock)
    db_beverage = beverage_crud.create_beverage(beverage, db)
    created_beverage_id = db_beverage.id

    # Act: Add order to database
    db_order = order_crud.create_order(order, db)
    created_order_id = db_order.id

    # Assert: One more order and one more user in database
    orders = order_crud.get_all_orders(db)
    users = user_crud.get_all_users(db)
    assert len(orders) == number_of_orders_before + 1
    assert len(users) == number_of_users_before + 1

    # Act: Re-read order from database
    read_order = order_crud.get_order_by_id(created_order_id, db)

    # Assert: Correct order was stored in database
    assert read_order.id == created_order_id

    # Act: Add pizza to order
    pizza_order = order_crud.add_pizza_to_order(db_order, db_pizza_type, db)

    # Assert: Correct pizza was added to order
    pizza_order_id = pizza_order.id
    assert pizza_order == order_crud.get_pizza_by_id(pizza_order_id, db)
    assert len(order_crud.get_all_pizzas_of_order(db_order, db)) == 1

    # Act: Add beverage to order
    beverage_order = order_crud.create_beverage_quantity(
        db_order, OrderBeverageQuantityCreateSchema(quantity=6, beverage_id=created_beverage_id), db)

    # Assert: Correct beverage was added to order
    beverage_order_id = beverage_order.beverage_id
    assert beverage_order == order_crud.get_beverage_quantity_by_id(created_order_id, beverage_order_id, db)
    assert order_crud.get_beverage_quantity_by_id(created_order_id, beverage_order_id, db) == beverage_order

    # Act: Update beverage quantity from order
    order_crud.update_beverage_quantity_of_order(created_order_id, beverage_order_id, 10, db)

    # Assert: Correct quantity of beverage from order was updated
    assert beverage_order.quantity == 10

    # Act: Delete beverage from order
    order_crud.delete_beverage_from_order(created_order_id, beverage_order_id, db)

    # Assert: Correct beverage was deleted from order
    assert order_crud.get_beverage_quantity_by_id(created_order_id, beverage_order_id, db) is None

    # Act: Delete pizza from order
    order_crud.delete_pizza_from_order(db_order, pizza_order_id, db)

    # Assert: Correct pizza was deleted from order
    deleted_pizza_order = order_crud.get_pizza_by_id(pizza_order_id, db)
    assert deleted_pizza_order is None

    # Act: Delete beverage from database
    beverage_crud.delete_beverage_by_id(created_beverage_id, db)

    # Assert: Correct beverage was deleted from database
    deleted_beverage = beverage_crud.get_beverage_by_id(created_beverage_id, db)
    assert deleted_beverage is None

    # Act: Delete pizza from database
    pizza_crud.delete_pizza_type_by_id(created_pizza_type_id, db)

    # Assert: Correct pizza was deleted from database
    deleted_pizza = pizza_crud.get_pizza_type_by_id(created_pizza_type_id, db)
    assert deleted_pizza is None

    # Act: Delete dough from database
    dough_crud.delete_dough_by_id(created_dough_id, db)

    # Assert: Correct dough was deleted from database
    deleted_dough = dough_crud.get_dough_by_id(created_dough_id, db)
    assert deleted_dough is None

    # Act: Delete order
    order_crud.delete_order_by_id(created_order_id, db)

    # Assert: Correct number of orders in database after deletion
    orders = order_crud.get_all_orders(db)
    assert len(orders) == number_of_orders_before

    # Assert: Correct order was deleted from database
    deleted_order = order_crud.get_order_by_id(created_order_id, db)
    assert deleted_order is None
