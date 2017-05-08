# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QuyuItem(scrapy.Item):
    # 区域
    Quyu = scrapy.Field()
    # 正在出售
    SaleNow = scrapy.Field()
    # 90天成交
    Deal90Days = scrapy.Field()
    # 昨日带看
    # VisitYesterday = scrapy.Field()

class HouseItem(scrapy.Item):
    # 区域
    House_quyu = scrapy.Field()
    # 房源编号
    House_id = scrapy.Field()
    # 房屋title
    # House_title = scrapy.Field()
    # 建筑面积
    House_area = scrapy.Field()
    # 户型
    House_type = scrapy.Field()
    # 楼层
    House_floor = scrapy.Field()
    # 年代
    House_year = scrapy.Field()
    # 装修
    House_decorate = scrapy.Field()
    # 环线
    House_loopline = scrapy.Field()
    # 朝向
    House_direction = scrapy.Field()
    # 小区
    House_community = scrapy.Field()
    # 地址
    # House_address = scrapy.Field()
    # 总价
    House_total_price = scrapy.Field()
    # 单价
    House_unit_price = scrapy.Field()
    # 房源链接
    House_link = scrapy.Field()
