import datetime
from flask_sqlalchemy import SQLAlchemy
from com.web.web_app import app
import properties as props

app.config['SQLALCHEMY_DATABASE_URI'] = props.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    """
    The item that can be sold. It may have a producer, brand, model, size, weight, country of origin
    item_state field reflects the item data condition: INIT_UPLOAD, DETAILS_LOADED, USER_REVIEWS_ADDED
    """
    __tablename__ = 'item'

    id = db.Column(db.String(50), primary_key=True)
    seller_name = db.Column(db.String(50))
    seller_ref = db.Column(db.String(50), index=True)
    seller_url = db.Column(db.Text)
    sales_rank = db.Column(db.Integer)
    ean_list = db.Column(db.String(255), index=True)
    name = db.deferred(db.Column(db.Text))
    category_id = db.Column(db.String(50), index=True)
    producer = db.Column(db.String(255))
    features = db.deferred(db.Column(db.Text))
    producer_part_number = db.Column(db.String(50), index=True)
    producer_info = db.deferred(db.Column(db.Text))
    product_spec = db.deferred(db.Column(db.Text))
    product_group = db.Column(db.String(50), index=True)
    producer_max_age_months = db.Column(db.Integer)
    producer_min_age_months = db.Column(db.Integer)
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    country = db.Column(db.String(50))
    produced_till = db.Column(db.DateTime)
    item_state = db.Column(db.String(50))
    category = db.Column(db.String(50), index=True)
    type_hint = db.Column(db.String(50), index=True)
    customized_text = db.Column(db.String(255))  # add some text to this item
    similar_product_seller_refs = db.deferred(db.Column(db.Text))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return "<Item(id=%s, name=%s, producer=%s, brand=%s, model=%s, country=%s," \
               " item_state=%s, category=%s, type_hint=%s)>" % (
                self.id, self.name, self.producer, self.brand, self.model, self.country,
                self.item_state, self.category, self.type_hint)


class ItemImage(db.Model):
    """
    a table to store item image references
    """
    __tablename__ = 'item_image'
    id = db.Column(db.String(50), primary_key=True)
    item_id = db.Column(db.String(50), db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item',  backref=db.backref('images', lazy=True))
    url = db.Column(db.String(255))
    image_type = db.Column(db.String(50))
    category = db.Column(db.String(50))
    size = db.Column(db.String(50))


class ItemReview(db.Model):
    """
    reviews of the item         
    """
    __tablename__ = 'item_review'
    id = db.Column(db.String(50), primary_key=True)
    item_id = db.Column(db.String(50), db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('reviews', lazy=True))
    seller_ref = db.Column(db.String(50), primary_key=True)
    title = db.deferred(db.Column(db.Text))
    review = db.deferred(db.Column(db.Text))
    rating = db.Column(db.Numeric(3, 2))
    date = db.Column(db.DateTime)


class ItemOffer(db.Model):
    """
    item offer by a merchant   
    """
    __tablename__ = 'item_offer'
    id = db.Column(db.String(250), primary_key=True)  # this should be Amazon Offer Listing ID
    item_id = db.Column(db.String(50), db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('offers', lazy=True))
    url = db.Column(db.Text)
    price = db.Column(db.Integer)  # expressing the price as int to avoid sqlight possible conversion losses
    price_formated = db.Column(db.String(50))
    currency = db.Column(db.String(50))
    condition = db.Column(db.String(50))
    availability = db.Column(db.String(250))
    availability_type = db.Column(db.String(250))
    isEligibleForSuperSaverShipping = db.Column(db.Boolean)
    isEligibleForPrime = db.Column(db.Boolean)
    sale_price = db.Column(db.Integer)
    country = db.Column(db.String(50))
    valid_till = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
