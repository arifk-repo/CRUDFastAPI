from typing import Optional, List
from Model import ItemsModel, UserModel
from fastapi import FastAPI, Depends, Query
from TestModel.TestModel import Name
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import model
from passlib.context import CryptContext
app = FastAPI()
model.Base.metadata.create_all(bind=engine)
password_context=CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password,hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/v1/users')
async def create_user(user_request:UserModel.UserModel, db: Session = Depends(get_db)):
    user = model.User()
    user.username = user_request.username
    user.hashed_password = get_password_hash(user_request.password)
    user.is_member = user_request.is_member
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"Message": "Successful Create User"}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemsModel.Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/models/{models_name}")
async def get_model(models_name:Name):
    if models_name == Name.name1:
        return {
            "Models Name": models_name,
            "Message": "You Are Using LSTM"
        }
    if models_name.value == "Alex2":
        return {
            "Models Name": models_name,
            "Message": "You Are Using CNN"
        }
    return {
        "Models Name": models_name,
        "Message": "You Are Using DBN"
    }


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip:skip+limit]


@app.get("/v1/items/{items_id}")
async def new_read_item(items_id: str,q: Optional[str]=None):
    if q:
        return {
            "item_id": items_id,
            "query": q
        }
    return {
        "item_id": items_id
    }


@app.get("/v2/items/{items_id}")
async def new_type_read_item(items_id: str, q: Optional[str]=None, is_member: Optional[bool]=False):
    item = {
        "item_id": items_id
    }
    if q:
        item.update({
            "query": q
        })
    if is_member:
        item.update({
            "Description": "Hello Member"
        })
    return item


@app.post("/v2/items/")
async def create_items(item: ItemsModel.Items):
    return item


@app.post("/v3/items/")
async def create_item2(item: ItemsModel.Items):
    item_dict=item.dict()
    if item.is_member:
        item_dict.update({
            "Status": "You are member"
        })
    return item_dict


@app.put("/v2/items/{items_id}")
async def put_item(items_id: str, item: ItemsModel.Items):
    return {"Item_id": items_id, **item.dict()}


@app.put("/v3/items/{items_id}")
async def put_item_two(items_id: str, item: ItemsModel.Items, q:Optional[str] = None):
    result = {"Item_id":items_id, **item.dict()}
    if q:
        result.update({
            "Query": q
        })
    return result


@app.get("/v4/items/")
async def crate_items_query_multi(q: List[str] = Query(None)):
    result = {"Items":[
        {"item_id":"Foo"},
        {"Item_id":"bar"}
    ]}
    if q:
        result.update({
            "query":q
        })
    return result

@app.get("/v3/items/")
async def crate_items_query(q: Optional[str] = Query("fixedquery",min_length=3,
                                                     max_length=50,
                                                     regex="^fixedquery")):
    result = {"Items":[
        {"item_id":"Foo"},
        {"Item_id":"bar"}
    ]}
    if q:
        result.update({
            "query":q
        })
    return result