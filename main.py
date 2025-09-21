from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os, shutil

DATABASE_URL = "sqlite:///./petshop.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String) 

    orders = relationship("Order", back_populates="user")


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    image_url = Column(String)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    city = Column(String)
    pincode = Column(String)
    state = Column(String)
    country = Column(String)

    user = relationship("User", back_populates="orders")


Base.metadata.create_all(bind=engine)

def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(username="admin", email="admin@example.com", password="123admin", role="admin")
        db.add(admin)
        db.commit()
    db.close()

create_admin()


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    pets = db.query(Pet).all()
    return templates.TemplateResponse("petshop.html", {"request": request, "pets": pets})

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    pets = db.query(Pet).all()
    user = request.session.get("user")
    user = request.session.get("admin")   
    return templates.TemplateResponse(
        "petshop.html",
        {"request": request, "pets": pets, "user": user},
        status_code=200
    )

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = User(username=username, email=email, password=password, role="user")
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        request.session["user"] = {"id": user.id, "username": user.username, "role": user.role}
        if user.role == "admin":
            return RedirectResponse("/admin_dashboard", status_code=303)
        else:
            return RedirectResponse("/user_dashboard", status_code=303)
    return RedirectResponse("/login", status_code=303)

@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == username,
        User.password == password,
        User.role == "admin"
    ).first()

    if user:
        request.session["user"] = {"id": user.id, "username": user.username, "role": "admin"}
        return RedirectResponse("/admin_dashboard", status_code=303)
    return RedirectResponse("/admin/login", status_code=303)

@app.get("/user_dashboard", response_class=HTMLResponse)
def user_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user["role"] != "user":
        return RedirectResponse("/login", status_code=303)
    orders = db.query(Order).filter(Order.user_id == user["id"]).all()
    return templates.TemplateResponse("user_dashboard.html", {"request": request, "user": user, "orders": orders})

@app.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get("user")
    if not user or user["role"] != "admin":
        return RedirectResponse("/login", status_code=303)
    users = db.query(User).all()
    orders = db.query(Order).all()
    pets = db.query(Pet).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user, "users": users, "orders": orders, "pets": pets})

UPLOAD_DIR = "static/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/add-pet", response_class=HTMLResponse)
def add_pet_page(request: Request):
    return templates.TemplateResponse("add_pet.html", {"request": request})

@app.post("/add-pet")
async def add_pet(
    name: str = Form(...),
    category: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await image.read()
    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb") as f:
        f.write(contents)

    pet = Pet(name=name, category=category, price=price, image_url=f"/{file_location}")
    db.add(pet)
    db.commit()

    return RedirectResponse("/admin_dashboard", status_code=303)

    
@app.post("/admin/delete_pet/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if pet:
        db.delete(pet)
        db.commit()
    return RedirectResponse("/admin_dashboard", status_code=303)

@app.get("/order", response_class=HTMLResponse)
def order_page(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})

@app.post("/place_order")
def place_order(
    request: Request,
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),    
    city: str = Form(...),
    pincode: str = Form(...),
    state: str = Form(...),
    country: str = Form(...),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)

    order = Order(
        user_id=user["id"],
        full_name=full_name,
        phone=phone,
        email=email,
        address=address,   
        city=city,
        pincode=pincode,
        state=state,
        country=country
    )

    db.add(order)
    db.commit()

    return templates.TemplateResponse(
    "order_success.html",
    {"request": request, "order": order},
    status_code=200  
)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
