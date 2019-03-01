import uuid
import hashlib
import logging
from datetime import datetime
from parsel import Selector
from com.amazon.entities import Item, ItemImage, ItemOffer
from com.amazon.amazon_api import ProductAPI
from properties import AWS_PRODUCT_API_REGION
from com.data.utils import remove_non_ansii, str_separator

amazon_api = ProductAPI(region=AWS_PRODUCT_API_REGION)


def updateItems(asins, session):

    processed_items = []
    response = amazon_api.call(Operation='ItemSearch',
                                 SearchIndex='All',
                                 Keywords='drone',
                                 ResponseGroup='Images,ItemAttributes,Offers'
                                )
    logging.info('amazon resp: ' + str(response))
    mydoc = Selector(str(response))
    for e in mydoc.xpath('//items/item'):
        asin = e.xpath('.//asin/text()').extract_first()
        try:
            with session.begin_nested():
                selected_item = session.query(Item).filter_by(seller_ref=asin).first()
                if selected_item is None:
                    selected_item = Item(id=str(uuid.uuid1()), seller_ref=asin)
                else:
                    logging.info('item exists in db: ' + asin)
                selected_item.seller_name = 'amazon'
                selected_item.category_id = category_id
                selected_item.seller_url = e.css('DetailPageURL::text').extract_first()
                if (e.css('SalesRank::text').extract_first() is not None):
                    selected_item.sales_rank = int(e.css('SalesRank::text').extract_first())
                selected_item.producer_info = remove_non_ansii(
                    str_separator.join(e.css('EditorialReviews EditorialReview Content::text').extract()))
                selected_item.modified_at = datetime.now()
                # attributes processing
                for attr in e.css("ItemAttributes"):
                    selected_item.brand = attr.css('Brand::text').extract_first()
                    selected_item.features = remove_non_ansii(str_separator.join(attr.css('Feature::text').extract()))
                    selected_item.color = attr.css('Color::text').extract_first()
                    selected_item.name = attr.css('Title::text').extract_first()
                    selected_item.producer = attr.css('Manufacturer::text').extract_first()
                    selected_item.producer_part_number = attr.css('MPN::text').extract_first()
                    selected_item.type_hint = attr.css('ProductTypeName::text').extract_first()
                    selected_item.product_group = attr.css('ProductGroup::text').extract_first()
                    selected_item.model = attr.css('Model::text').extract_first()
                    selected_item.ean_list = ';'.join(attr.css('EANList EANListElement::text').extract())
                    selected_item.size = attr.css('Size::text').extract_first()
                    selected_item.producer_max_age_months = attr.css('ManufacturerMaximumAge::text').extract_first()
                    selected_item.producer_min_age_months = attr.css('ManufacturerMinimumAge::text').extract_first()
                # image processing
                item_images = []
                image_ids = set()
                if session.query(ItemImage).filter_by(item_id=selected_item.id).first() is None:
                    image_small_url = e.css('SmallImage url::text').extract_first()
                    image_small_id = hashlib.md5(image_small_url.encode('utf-8')).hexdigest()
                    if not image_small_id in image_ids and session.query(ItemImage).filter_by(id=image_small_id,
                                                                                              item_id=selected_item.id).count() == 0:
                        image_ids.add(image_small_id)
                        image_small = ItemImage(id=image_small_id,
                                                item_id=selected_item.id,
                                                url=e.css('SmallImage url::text').extract_first(),
                                                image_type="small",
                                                category="main",
                                                size=e.css('SmallImage Width::text').extract_first() + 'x' + e.css(
                                                    'SmallImage Height::text').extract_first(),
                                                )
                        item_images.append(image_small)

                    image_medium_url = e.css('MediumImage url::text').extract_first()
                    image_medium_id = hashlib.md5(image_medium_url.encode('utf-8')).hexdigest()
                    if not image_medium_id in image_ids and session.query(ItemImage).filter_by(id=image_medium_id,
                                                                                               item_id=selected_item.id).count() == 0:
                        image_ids.add(image_medium_id)
                        image_medium = ItemImage(id=image_medium_id,
                                                 item_id=selected_item.id,
                                                 url=e.css('MediumImage url::text').extract_first(),
                                                 image_type="medium",
                                                 category="main",
                                                 size=e.css('MediumImage Width::text').extract_first() + 'x' + e.css(
                                                     'MediumImage Height::text').extract_first(),
                                                 )
                        item_images.append(image_medium)

                    image_large_url = e.css('LargeImage url::text').extract_first()
                    image_large_id = hashlib.md5(image_large_url.encode('utf-8')).hexdigest()
                    if not image_large_id in image_ids and session.query(ItemImage).filter_by(id=image_large_id,
                                                                                              item_id=selected_item.id).count() == 0:
                        image_ids.add(image_large_id)
                        image_large = ItemImage(id=image_large_id,
                                                item_id=selected_item.id,
                                                url=e.css('LargeImage url::text').extract_first(),
                                                image_type="large",
                                                category="main",
                                                size=e.css('LargeImage Width::text').extract_first() + 'x' + e.css(
                                                    'LargeImage Height::text').extract_first(),
                                                )
                        item_images.append(image_large)

                    for img in e.css('ImageSets ImageSet'):
                        image_small_url = img.css('SmallImage url::text').extract_first()
                        image_small_id = hashlib.md5(image_small_url.encode('utf-8')).hexdigest()
                        if not image_small_id in image_ids and session.query(ItemImage).filter_by(id=image_small_id,
                                                                                                  item_id=selected_item.id).count() == 0:
                            image_ids.add(image_small_id)
                            image_small = ItemImage(id=image_small_id,
                                                    item_id=selected_item.id,
                                                    url=img.css('SmallImage url::text').extract_first(),
                                                    image_type="small",
                                                    category="variant",
                                                    size=img.css(
                                                        'SmallImage Width::text').extract_first() + 'x' + e.css(
                                                        'SmallImage Height::text').extract_first(),
                                                    )
                            item_images.append(image_small)

                        image_medium_url = img.css('MediumImage url::text').extract_first()
                        image_medium_id = hashlib.md5(image_medium_url.encode('utf-8')).hexdigest()
                        if not image_medium_id in image_ids and session.query(ItemImage).filter_by(id=image_medium_id,
                                                                                                   item_id=selected_item.id).count() == 0:
                            image_ids.add(image_medium_id)
                            image_medium = ItemImage(id=image_medium_id,
                                                     item_id=selected_item.id,
                                                     url=img.css('MediumImage url::text').extract_first(),
                                                     image_type="medium",
                                                     category="variant",
                                                     size=img.css(
                                                         'MediumImage Width::text').extract_first() + 'x' + e.css(
                                                         'MediumImage Height::text').extract_first(),
                                                     )
                            item_images.append(image_medium)

                        image_large_url = img.css('LargeImage url::text').extract_first()
                        image_large_id = hashlib.md5(image_large_url.encode('utf-8')).hexdigest()
                        if not image_large_id in image_ids and session.query(ItemImage).filter_by(id=image_large_id,
                                                                                                  item_id=selected_item.id).count() == 0:
                            image_ids.add(image_large_id)
                            image_large = ItemImage(id=image_large_id,
                                                    item_id=selected_item.id,
                                                    url=img.css('LargeImage url::text').extract_first(),
                                                    image_type="large",
                                                    category="variant",
                                                    size=img.css(
                                                        'LargeImage Width::text').extract_first() + 'x' + e.css(
                                                        'LargeImage Height::text').extract_first(),
                                                    )
                            item_images.append(image_large)

                # offers processing
                offers = []
                offer_ids = set()
                for offer in e.css('Offers Offer'):
                    offer_id = offer.css('OfferListing OfferListingId::text').extract_first()
                    if not offer_id in offer_ids:
                        offer_ids.add(offer_id)
                        offer = ItemOffer(id=offer.css('OfferListing OfferListingId::text').extract_first(),
                                          item_id=selected_item.id,
                                          condition=offer.css('OfferAttributes Condition::text').extract_first(),
                                          availability=offer.css('OfferListing Availability::text').extract_first(),
                                          availability_type=offer.css(
                                              'OfferListing AvailabilityAttributes AvailabilityType::text').extract_first(),
                                          price=offer.css('OfferListing Price Amount::text').extract_first(),
                                          sale_price=offer.css('OfferListing SalePrice Amount::text').extract_first(),
                                          currency=offer.css('OfferListing Price CurrencyCode::text').extract_first(),
                                          isEligibleForSuperSaverShipping=offer.css(
                                              'OfferListing IsEligibleForSuperSaverShipping::text').extract_first(),
                                          isEligibleForPrime=offer.css(
                                              'OfferListing IsEligibleForPrime::text').extract_first()
                                          )
                        offers.append(offer)
            if len(item_images) > 0:
                session.add_all(item_images)
            if len(offers) > 0:
                session.add_all(offers)
            session.merge(selected_item)
        except Exception as e:
            logging.exception('exception in item update: ' + asin)
