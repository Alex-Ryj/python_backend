import unittest
import uuid
from sqlalchemy.orm import joinedload
from com.data.entities import db, Item, ItemImage, ItemReview, ItemOffer
import properties as props


class EntitiesTest(unittest.TestCase):

    def setUp(self):
        db.app.config['SQLALCHEMY_DATABASE_URI'] = props.DATABASE_TEST_URI
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_create_item(self):
        item = Item(id=str(uuid.uuid1()),
                    name='item name1',
                    producer='producer',
                    brand='brand',
                    model='model',
                    seller_ref='seller_ref',
                    country='country',
                    item_state='state'
                    )
        images = [ItemImage(id=str(uuid.uuid1()), item=item, url="url", image_type="thumbnail", size="20x20px"),
                  ItemImage(id=str(uuid.uuid1()), item=item, url="url", image_type="thumbnail", size="20x20px")]
        image = ItemImage(id=str(uuid.uuid1()), url="url", image_type="thumbnail", size="20x20px")
        item.images.append(image)
        ir1 = ItemReview(id='1', seller_ref='sr1', item=item)
        ir2 = ItemReview(id='2', seller_ref='sr2', item=item)
        offers = [ItemOffer(id=str(uuid.uuid1()), item_id=item.id, price=1.1, country="us"),
                  ItemOffer(id=str(uuid.uuid1()), item_id=item.id, price=1.2, country="uk")]
        db.session.add(item)
        db.session.add_all(offers)
        db.session.add_all(images)
        db.session.add(item)
        db.session.add(ir1)
        db.session.add(ir2)
        db.session.commit()
        self.assertEqual(1, len(Item.query.all()))
        self.assertEqual(1, db.session.query(ItemReview).filter_by(id='1', seller_ref='sr1').count())
        self.assertIsNone(db.session.query(ItemReview).filter_by(id='x', seller_ref='x').first())
        self.assertEqual(3, len(item.images))
        full_item = Item.query.options(joinedload('images'))
        for item in full_item:
            self.assertEqual(3, len(item.images))
