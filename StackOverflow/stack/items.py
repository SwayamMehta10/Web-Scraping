# Defining storage containers for the scraped data

from scrapy.item import Item, Field

class StackItem(Item):
    title = Field()
    url = Field()