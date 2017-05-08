#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from sqlite import Sqlite
from lianjia.items import QuyuItem
from lianjia.items import HouseItem


class HouselinkPipeline(object):
    def process_item(self, item, spider):
        # 第一种Item
        if isinstance(item, QuyuItem):
            tj_table_name = u"全上海统计"
            tj_quyu = item['Quyu']
            tj_salenow = item['SaleNow']
            tj_deal90days = item['Deal90Days']
            tj_todaynewhouse = None
            tj_dealyesterday = None
            # tj_visityesterday = item['VisitYesterday']
            ret = Sqlite.judge_quyu(tj_table_name, tj_quyu)
            if ret[0] == 1:
                logging.log(level=logging.WARNING, msg='该区域已经存在')

                old_salenow = Sqlite.get_salenow(tj_table_name, tj_quyu)[0]
                tj_todaynewhouse = int(tj_salenow) - old_salenow

                old_deal90days = Sqlite.get_deal90days(tj_table_name, tj_quyu)[0]
                tj_dealyesterday = int(tj_deal90days) - old_deal90days

                # 更新区域表
                Sqlite.update_quyu_table(tj_table_name, tj_salenow, tj_deal90days, \
                                         tj_todaynewhouse, tj_dealyesterday, tj_quyu)
            else:
                # logging.log(level=logging.WARNING, msg='添加新的区域到数据库')
                Sqlite.write_tongji_info(tj_table_name, tj_quyu, tj_salenow, tj_deal90days,\
                                         tj_todaynewhouse, tj_dealyesterday)
        # 第二种Item
        if isinstance(item, HouseItem):
            house_table_name = u"房源信息"
            house_quyu = item['House_quyu']
            house_id = item['House_id']
            # house_title = item['House_title']
            house_area = item['House_area']
            house_type = item['House_type']
            house_floor = item['House_floor']
            house_year = item['House_year']
            house_decorate = item['House_decorate']
            house_loopline = item['House_loopline']
            house_direction = item['House_direction']
            house_community = item['House_community']
            # house_address = item['House_address']
            house_total_price = item['House_total_price']
            house_unit_price = item['House_unit_price']
            house_link = item['House_link']

            ret = Sqlite.judge_house_id(house_table_name, house_id)
            if ret[0] == 1:
                logging.log(level=logging.WARNING, msg='该房源已经存在')
                house_old_price = Sqlite.get_house_price(house_table_name, house_id)[0]
                if ((int(house_total_price) < house_old_price) and (house_old_price != 0)):
                    house_table_name = u"降价啦"
                    house_different_price = house_old_price - int(house_total_price)
                elif ((int(house_total_price) > house_old_price) and (house_old_price != 0)):
                    house_table_name = u"涨价啦"
                    house_different_price = int(house_total_price) - house_old_price
                else:
                    return item
                Sqlite.update_compare_info(house_table_name, house_quyu, house_id, house_area, \
                                        house_type, house_floor, house_year, house_decorate, house_loopline, \
                                        house_community, house_old_price, house_total_price, \
                                        house_different_price, house_unit_price, house_link)
            else:
                # logging.log(level=logging.WARNING, msg='添加新的房源到数据库')
                Sqlite.write_house_info(house_table_name, house_quyu, house_id, house_area, \
                                        house_type, house_floor, house_year, house_decorate, house_loopline, \
                                        house_direction, house_community, house_total_price, \
                                        house_unit_price, house_link)

        return item

