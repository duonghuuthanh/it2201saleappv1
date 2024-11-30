from app.models import Category, Product, User, UserRole
from app import app, db
import hashlib
import cloudinary.uploader


def load_categories():
    return Category.query.order_by("id").all()


def load_products(cate_id=None, kw=None, page=1):
    query = Product.query

    if cate_id:
        query = query.filter(Product.category_id == cate_id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    query = query.slice(start, start + page_size)

    return query.all()


def count_products():
    return Product.query.count()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username),
                          User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def add_user(name, username, password, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username.strip(), password=password)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)
