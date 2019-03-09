from com.data.entities import Item, db


class EbayItem(Item):
    """
    Ebay specific item
    """

    __mapper_args__ = {
        'polymorphic_identity': 'ebayItem',
    }