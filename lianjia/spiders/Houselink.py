#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging

from urlparse import urljoin
import scrapy                           # 导入scrapy包
from scrapy.http import Request         # 一个单独的request的模块，需要跟进URL的时候，需要用它
from lianjia.items import QuyuItem
from lianjia.items import HouseItem

# 把TIMEOUT设小，多并发，多重试
from scrapy.conf import settings
settings.set('DOWNLOAD_TIMEOUT', 5)
settings.set('CONCURRENT_REQUESTS', 16)
settings.set('DOWNLOAD_DELAY', 0.1)

# 设置编码格式
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['http://sh.lianjia.com/']
    base_url = 'http://sh.lianjia.com/ershoufang/'
    base_link = 'http://sh.lianjia.com/'
    count_dict = {}
    quyu_dict = {
        'all_quyu':['NULL'],  # 统计全上海二手房的数量
        'pudongxinqu':['beicai','biyun','caolu','chuansha','datuanzhen','gaodong','gaohang','huamu','huinan','geqing', \
                       'hangtou','jinqiao','jinyang','kangqiao','lingangxincheng','laogangzhen','lujiazui','lianyang', \
                       'nichengzhen','nanmatou','shibo','sanlin','shuyuanzhen','tangqiao','tangzhen','weifang', \
                       'waigaoqiao','wanxiangzhen','xinchang','xuanqiao','yangdong','yangjing','yuqiao1','yuanshen', \
                       'zhangjiang','zhoupu','zhuqiao'],
        'minhang':['chunshen','gumei','huacao','hanghua','jinganxincheng','jinhui','jinhongqiao','longbai','laominhang', \
                   'meilong','maqiao','pujiang1','qibao','wujing','shenzhuang','zhuanqiao'],
        'baoshan':['dachangzhen','dahua','gucun','gongfu','gaojing','gongkang','luodian','luojing','songbao','shangda', \
                   'songnan','tonghe','yanghang','yuepu','zhangmiao'],
        'xuhui':['caohejing','changqiao','huadongligong','huajing','hengshanlu','jianguoxilu','kangjian','longhua', \
                 'shanghainanzhan','tianlin','wantiguan','xuhuibinjiang','xujiahui','xietulu','zhiwuyuan'],
        'putuo':['changfeng1','changshoulu','caoyang','changzheng','ganquanyichuan','guangxin','taopu','wanli','wuning', \
                 'zhenguang','zhenru','zhongyuanliangwancheng'],
        'yangpu':['anshan','dongwaitan','huangxinggongyuan','kongjianglu','wujiaochang','xinjiangwancheng','zhoujiazuilu', \
                  'zhongyuan1'],
        'changning':['beixinjing','gubei','hongqiao1','tianshan','xinhualu','xijiao','xianxia','zhenninglu', \
                     'zhongshangongyuan'],
        'songjiang':['chedun','jiuting','maogang','shihudang','sijing','songjiangdaxuecheng','songjianglaocheng', \
                     'songjiangxincheng','sheshan','xinbang','xiaokunshan','shenminbieshu','xinqiao','yexie'],
        'jiading':['anting','fengzhuang','huating','jiadinglaocheng','jiadingxincheng','jiangqiao','juyuanxinqu', \
                   'malu','nanxiang','waigang','xinchenglu1','xuxing'],
        'huangpu':['dongjiadu','dapuqiao','huaihaizhonglu','huangpubinjiang','laoximen','nanjingdonglu','penglaigongyuan', \
                   'renminguangchang','shibobinjiang','wuliqiao','xintiandi','yuyuan'],
        'jingan':['caojiadu','jingansi','jiangninglu','nanjingxilu'],
        'zhabei':['buyecheng','daning','pengpu','xizangbeilu','yangcheng','yonghe','zhabeigongyuan'],
        'hongkou':['beiwaitan','jiangwanzhen','liangcheng','linpinglu','luxungongyuan','quyang','sichuanbeilu'],
        'qingpu':['baihe','chonggu','huaxin','jinze','liantang1','xianghuaqiao','xujing','xiayang','yingpu','zhujiajiao', \
                  'zhaoxiang'],
        'fengxian':['fengcheng','fengxianjinhui','haiwan','nanqiao','qingcun','situan','xidu','zhuanghang','zhelin'],
        'jinshan':['caojing','fengjing','jinshan1','langxia','luxiang','shihua','shanyang','tinglin','zhujing','zhangyan'],
        'chongming':['baozhen','chenjiazhen','chongmingqita','chongmingxincheng','changxingdao21211','hengshadao'],
        'shanghaizhoubian':['haimen','jiaxing','kunshan1','qidong1','shanghaizhoubian2','suzhou','taicang212']
    }

    # 首先按照上海的行政区域进行爬取
    def start_requests(self):
        for quyu_key in sorted(self.quyu_dict.keys()):
            if (quyu_key == "all_quyu"):
                url = self.base_url
            else:
                url = self.base_url + quyu_key
            self.log('Quyu url: %s' % url, level=logging.WARNING)
            yield Request(url, self.parse, meta={'key':quyu_key})

    # 获取行政区域的相关信息，然后再按照子区域进行爬取
    def parse(self, response):
        item = QuyuItem()
        # 区域，从网页信息中读出，中文表示，这里把quyu_key单独拎出来的目的是把quyu_key传到下一层函数中
        quyu_key = response.xpath('//div[@class="side-header clearfix"]/span[@class="header-text"]/text()').extract()[0]
        if (response.meta['key'] == "all_quyu"):
            item['Quyu'] = u"上海全部房源"
        else:
            item['Quyu'] = quyu_key
        # 正在出售
        item['SaleNow'] = response.xpath('//ul[@class="content"]/li[1]/div[2]/span[@class="num strong-num"]/text()').extract()[0]
        # 90天成交
        item['Deal90Days'] = response.xpath('//div[@class="value"]/span[@class="num strong-num"]/text()').extract()[0]
        # 昨日带看
        # item['VisitYesterday'] = response.xpath('//li[@class="last-item"]/div[2]/span[@class="num strong-num"]/text()').extract()[0]

        yield item

        # 字典中的key从上一个函数start_requests中传递下来
        for sub_quyu_value in self.quyu_dict[response.meta['key']]:
            # self.count_dict[sub_quyu_value] = 0
            if (sub_quyu_value == 'NULL'):
                pass
            else:
                url = urljoin(self.base_url, sub_quyu_value)
                # 如果拼接后的地址就是base_url，则不执行
                if (url == self.base_url):
                    # print response.meta['key']
                    # print sub_quyu_value
                    pass
                else:
                    print url
                    yield Request(url, callback=self.get_houselink, dont_filter=True, \
                                  meta={'key':quyu_key, 'sub_key':sub_quyu_value})
                    """yieid Request，请求新的URL，后面跟的是回调函数，你需要哪一个函数来处理这个返回值，
                        就调用那一个函数，返回值会以参数的形式传递给你所调用的函数。
                    """

    # 页面分析器
    def get_houselink(self, response):
        # 拿到页面上的链接，给内容解析页使用，如果有下一页，则调用本身get_houselink()
        # self.log("===========================| %s |" % response.url, level=logging.WARNING)
        if (response.url == self.base_url):
            raise ValueError("error url")
        house_list = response.xpath('//div[@class="info"]/div[@class="prop-title"]/a/@href').extract()
        for house in house_list:
            # self.count_dict[response.meta['sub_key']] += 1
            url = urljoin(self.base_link, house)
            self.log('house_url: %s' % url)
            # 将得到的页面地址传送给单个页面处理函数进行处理 -> parse_houselink()
            yield Request(url, callback=self.parse_houselink, dont_filter=True, \
                          meta={'key':response.meta['key'], 'sub_key':response.meta['sub_key']})

        # 是否还有下一页，如果有的话，则继续
        next_pages = response.xpath('//a[@gahref="results_next_page"]')

        if next_pages:
            next_page = urljoin(self.base_link, next_pages.xpath('@href').extract()[0])
            self.log('page_url: %s' % next_page)
            ## 将「下一页」的链接传递给自身，并重新分析
            yield scrapy.Request(next_page, callback=self.get_houselink, dont_filter=True, \
                                 meta={'key':response.meta['key'], 'sub_key':response.meta['sub_key']})

    # 单页分析器
    def parse_houselink(self, response):
        # 将得到的单个作品的页进行分析取值
        self.log('house_detail_url: %s' % response.url, level=logging.WARNING)
        # self.log('sub_key is %s, and the number is %d' % \
        #          (response.meta['sub_key'], self.count_dict[response.meta['sub_key']]), \
        #          level=logging.WARNING)

        item = HouseItem()
        item['House_quyu'] = response.meta['key']
        item['House_id'] = response.xpath("//span[contains(.//text(), 'sh')]/text()").extract()[0].split('：')[1]
        # item['House_title'] = response.xpath("//div[@class='title']/h1[@class='main']/text()").extract()[0]
        item['House_area'] = response.xpath("//div[@class='content']/ul/li[3]/text()").extract()[0]
        item['House_type'] = response.xpath("//div[@class='content']/ul/li[1]/text()").extract()[0]
        item['House_floor'] = response.xpath("//div[@class='content']/ul/li[2]/text()").extract()[0]
        item['House_year'] = response.xpath("//tr[2]/td[2]/text()").extract()[1].strip("\n\t ")
        item['House_decorate'] = response.xpath("//tr[4]/td[1]/text()").extract()[1].strip("\n\t ")
        if (self.is_loopline_exist(response)):
            item['House_loopline'] = response.xpath("//tr[4]/td[2]/text()").extract()[1].strip("\n\t ")
        else:
            item['House_loopline'] = u"暂无数据"
        item['House_direction'] = response.xpath("//tr[3]/td[2]/text()").extract()[1].strip("\n\t ")
        item['House_community'] = response.xpath("//tr[5]/td/a[@class='propertyEllipsis ml_5']/text()").extract()[0]
        # item['House_address'] = response.xpath("//tr[6]/td/p[@class='addrEllipsis fl ml_5']/text()").extract()[0]
        item['House_total_price'] = response.xpath("//div[@class='mainInfo bold']/text()").extract()[0]
        item['House_unit_price'] = response.xpath("//tr[1]/td[1]/text()").extract()[1].strip("\n\t ")
        item['House_link'] = response.url

        yield item
        # print item

    @staticmethod
    def is_loopline_exist(response):
        result_list = response.xpath('//tr[4]/td').extract()
        if (len(result_list) == 2):
            return True
        else:
            return False
