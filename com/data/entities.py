#  Copyright (c) 2019.
#  Authored by: Alexandre Ryjoukhine
#  Licensed under MIT

import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy import Index
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

    item_id = db.Column(db.String(50), primary_key=True)
    online_seller = db.Column(db.String(50), primary_key=True)
    seller_ref = db.Column(db.String(50), primary_key=True)
    seller_url = db.Column(db.Text)
    sales_rank = db.Column(db.Integer)
    ean_list = db.Column(db.String(255), index=True)
    name = db.deferred(db.Column(db.Text))
    category_1 = db.Column(db.String(50), index=True)
    category_2 = db.Column(db.String(50), index=True)
    cat_index = Index('cat_index', 'category_1', 'category_2')
    producer = db.Column(db.String(50))
    real_seller = db.Column(db.String(255))
    features = db.deferred(db.Column(db.Text))
    producer_part_number = db.Column(db.String(50))
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
    type_hint = db.Column(db.String(50))
    customized_text = db.Column(db.String(255))  # add some text to this item
    similar_product_seller_refs = db.deferred(db.Column(db.Text))
    type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': online_seller
    }

    def __repr__(self):
        return "<Item(id=%s, name=%s, producer=%s, brand=%s, model=%s, country=%s," \
               " item_state=%s, category=%s, type_hint=%s)>" % (
                   self.item_id, self.name, self.producer, self.brand, self.model, self.country,
                   self.item_state, self.category, self.type_hint)


class ItemImage(db.Model):
    """
    a table to store item image references
    """
    __tablename__ = 'item_image'
    image_id = db.Column(db.String(50), primary_key=True)
    item_id = db.Column(db.String(50), db.ForeignKey('item.item_id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('images', lazy=True))
    url = db.Column(db.String(255))
    image_type = db.Column(db.String(50))
    category = db.Column(db.String(50))
    size = db.Column(db.String(50))


class ItemReview(db.Model):
    """
    reviews of the item         
    """
    __tablename__ = 'item_review'
    review_id = db.Column(db.String(50), primary_key=True)
    item_id = db.Column(db.String(50), db.ForeignKey('item.item_id'), nullable=False)
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
    offer_id = db.Column(db.String(250), primary_key=True)  # this should be Amazon Offer Listing ID
    item_id = db.Column(db.String(50), db.ForeignKey('item.item_id'), nullable=False)
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


def get_attributes(item):
    fields = {}
    for field in [fld for fld in dir(item) if not fld.startswith('_') and fld != 'metadata' and fld != 'query'
                                              and fld != 'query_class']:
        field_val = item.__getattribute__(field)
        if isinstance(field_val, InstrumentedList):
            sub_items = []
            for it in InstrumentedList(field_val):
                sub_items.append(get_attributes(it))
            fields[field] = sub_items
        else:
            fields[field] = item.__getattribute__(field)
    return fields
