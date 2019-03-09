import unittest
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.inspection import inspect
import uuid
from sqlalchemy.orm import joinedload
from com.data.entities import db, Item, ItemImage, ItemReview, ItemOffer, get_attributes
import properties as props


class EntitiesTest(unittest.TestCase):

    json_str = '''{"brand": "brand", "cat_index": "Index('cat_index', 'category_1', 'category_2')", "category_1": null, "category_2": null, "color": null, "country": "country", "created_at": "2019-03-09 07:48:40.174199", "customized_text": null, "ean_list": null, "features": null, "images": [{"category": null, "image_id": "c12874f9-423f-11e9-91c3-4cedfb747eca", "image_type": "thumbnail1", "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "size": "20x20px", "url": "url"}, {"category": null, "image_id": "c12874fa-423f-11e9-91c3-4cedfb747eca", "image_type": "thumbnail2", "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "size": "20x20px", "url": "url"}, {"category": null, "image_id": "c12874fb-423f-11e9-91c3-4cedfb747eca", "image_type": "thumbnail3", "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "size": "20x20px", "url": "url"}], "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "item_state": "state", "model": "model", "modified_at": "2019-03-09 07:48:40.174312", "name": "item name1", "offers": [{"availability": null, "availability_type": null, "condition": null, "country": "us", "created_at": "2019-03-09 07:48:40.181334", "currency": null, "isEligibleForPrime": null, "isEligibleForSuperSaverShipping": null, "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "modified_at": "2019-03-09 07:48:40.181356", "offer_id": "c12874fc-423f-11e9-91c3-4cedfb747eca", "price": 1.1, "price_formated": null, "sale_price": null, "url": null, "valid_till": null}, {"availability": null, "availability_type": null, "condition": null, "country": "uk", "created_at": "2019-03-09 07:48:40.181334", "currency": null, "isEligibleForPrime": null, "isEligibleForSuperSaverShipping": null, "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "modified_at": "2019-03-09 07:48:40.181356", "offer_id": "c12874fd-423f-11e9-91c3-4cedfb747eca", "price": 1.2, "price_formated": null, "sale_price": null, "url": null, "valid_till": null}], "online_seller": "item", "produced_till": null, "producer": "producer", "producer_info": null, "producer_max_age_months": null, "producer_min_age_months": null, "producer_part_number": null, "product_group": null, "product_spec": null, "real_seller": null, "reviews": [{"date": null, "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "rating": null, "review": null, "review_id": "1", "seller_ref": "sr1", "title": null}, {"date": null, "item": "<Item(id=c12874f8-423f-11e9-91c3-4cedfb747eca, name=item name1, producer=producer, brand=brand, model=model, country=country, item_state=state, category=None, type_hint=None)>", "item_id": "c12874f8-423f-11e9-91c3-4cedfb747eca", "rating": null, "review": null, "review_id": "2", "seller_ref": "sr2", "title": null}], "sales_rank": null, "seller_ref": "seller_ref", "seller_url": null, "similar_product_seller_refs": null, "size": null, "type": null, "type_hint": null}'''


    def set_attributes(self, json_str, expected_type):
        cls = globals()[expected_type]
        obj = json.loads(json_str)
        delete = [key for key in obj if isinstance(obj[key], list)]
        for key in delete: del obj[key]
        result = cls(**obj)
        return result

    def setUp(self):
        db.app.config['SQLALCHEMY_DATABASE_URI'] = props.DATABASE_TEST_URI
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_create_item(self):
        item = Item(item_id=str(uuid.uuid1()),
                    name='item name1',
                    producer='producer',
                    brand='brand',
                    model='model',
                    seller_ref='seller_ref',
                    country='country',
                    item_state='state'
                    )
        images = [ItemImage(image_id=str(uuid.uuid1()), item=item, url="url", image_type="thumbnail1", size="20x20px"),
                  ItemImage(image_id=str(uuid.uuid1()), item=item, url="url", image_type="thumbnail2", size="20x20px")]
        image = ItemImage(image_id=str(uuid.uuid1()), url="url", image_type="thumbnail3", size="20x20px")
        item.images.append(image)
        ir1 = ItemReview(review_id='1', seller_ref='sr1', item=item)
        ir2 = ItemReview(review_id='2', seller_ref='sr2', item=item)
        offers = [ItemOffer(offer_id=str(uuid.uuid1()), item_id=item.item_id, price=1.1, country="us"),
                  ItemOffer(offer_id=str(uuid.uuid1()), item_id=item.item_id, price=1.2, country="uk")]
        db.session.add(item)
        db.session.add_all(offers)
        db.session.add_all(images)
        db.session.add(item)
        db.session.add(ir1)
        db.session.add(ir2)
        db.session.commit()
        self.assertEqual(1, len(Item.query.all()))
        self.assertEqual(1, db.session.query(ItemReview).filter_by(review_id='1', seller_ref='sr1').count())
        self.assertIsNone(db.session.query(ItemReview).filter_by(review_id='x', seller_ref='x').first())
        self.assertEqual(3, len(item.images))
        # full_item = Item.query.options(joinedload('images'))
        # for item in full_item:
        #     self.assertEqual(3, len(item.images))
        #
        # print(json.dumps(item.serialize(), default=str))
        # print(json.dumps(item, cls=self.new_alchemy_encoder(), check_circular=True, default=str))
        print()
        print(json.dumps(get_attributes(item),  default=str))

    def test_create_item_fromjson(self):
        cls = self.set_attributes('{"item_id": "item_id_0"}', 'Item')
        print(cls)
        cls = self.set_attributes(self.json_str, 'Item')
        print(cls)
