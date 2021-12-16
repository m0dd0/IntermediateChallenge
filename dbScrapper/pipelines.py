# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DbscrapperPipeline:

    def process_item(self, item, spider):
        print(item)
        if item['train'] is None:
            raise DropItem()
        else:
            for key in item:
                if isinstance(item[key], str):

                    # remove multiple whitespace in the result and sequences like \n
                    trimmed = " ".join(item[key].split())

                    # replace Unicode characters like ä
                    #trimmed = trimmed.decode('unicode-escape')

                    item[key] = trimmed

            return item
