#  Copyright (c) 2019.
#  Authored by: Alexandre Ryjoukhine
#  Licensed under MIT

from com.data.entities import Item, db


class AmazonItem(Item):
    """
    Specific Amazon item
    """
    sales_rank = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'amazonItem',
    }
