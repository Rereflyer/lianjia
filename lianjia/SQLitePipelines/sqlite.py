#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

SQLite_Name = 'lianjia'

conn = sqlite3.connect('%s.db' % SQLite_Name)
cursor = conn.cursor()

class Sqlite:
    @classmethod
    def write_tongji_info(cls, table_name, *tongji_info):
        print "write tongji info"
        if (cursor):
            try:
                sql = "SELECT * FROM sqlite_master WHERE type='table' AND name=?;"
                cursor.execute(sql, (table_name,))
            except:
                print 'No table named %s, we need create one!' % table_name

            if (cursor.fetchone()):	# 如果已经存在该表名，就不需要创建
                pass
            else:
                sql = '''CREATE TABLE %s ('区域'		TEXT	PRIMARY KEY NOT NULL,
                        '正在出售'		INT		NOT NULL,
                        '90天成交'		INT    	NOT NULL,
                        '今日新增房源'	INT,
                        '昨日成交'       INT);''' % table_name
                cursor.execute(sql)

            sql = "INSERT INTO %s VALUES (?, ?, ?, ?, ?);" % table_name
            cursor.execute(sql, tongji_info)
            conn.commit()

    @classmethod
    def judge_quyu(cls, table_name, *quyu_name):
        try:
            sql = "SELECT EXISTS(SELECT 1 FROM %s WHERE 区域=?);" % table_name
            cursor.execute(sql, quyu_name)
        except:
            return (0,)
        else:
            return cursor.fetchone()

    @classmethod
    def get_salenow(cls, table_name, *quyu_name):
        try:
            sql = "SELECT 正在出售 FROM %s WHERE 区域=?;" % table_name
            cursor.execute(sql, quyu_name)
        except:
            return (0,)
        else:
            return cursor.fetchone()

    @classmethod
    def get_deal90days(cls, table_name, *quyu_name):
        try:
            sql = "SELECT [90天成交] FROM %s WHERE 区域=?;" % table_name
            cursor.execute(sql, quyu_name)
        except:
            return (0,)
        else:
            return cursor.fetchone()

    @classmethod
    def update_quyu_table(cls, table_name, *changed_table):
        try:
            sql = "UPDATE %s SET 正在出售=?, [90天成交]=?, 今日新增房源=?, 昨日成交=? WHERE 区域=?;" % table_name
            cursor.execute(sql, changed_table)
        except:
            print "update_quyu_table, some error occur"
        else:
            conn.commit()

    @classmethod
    def write_house_info(cls, table_name, *house_info):
        # print "write house info, table_name=%s, House_quyu=%s, House_id=%s" % (table_name, house_info[0], house_info[1])
        if (cursor):
            try:
                sql = "SELECT * FROM sqlite_master WHERE type='table' AND name=?;"
                cursor.execute(sql, (table_name,))
            except:
                print 'No table named %s, we need create one!' % table_name

            if (cursor.fetchone()):	# 如果已经存在该表名，就不需要创建
                pass
            else:
                print 'create table'
                sql = '''CREATE TABLE %s ('区域'    TEXT NOT NULL,
                        '房屋ID'		    TEXT	    PRIMARY KEY NOT NULL,
                        '建筑面积'		TEXT    	NOT NULL,
                        '户型'			TEXT    	NOT NULL,
                        '楼层'			TEXT    	NOT NULL,
                        '年代'			TEXT    	NOT NULL,
                        '装修'			TEXT    	NOT NULL,
                        '环线'    		TEXT		NOT NULL,
                        '朝向'			TEXT    	NOT NULL,
                        '小区'			TEXT    	NOT NULL,
                        '总价'			INT			NOT NULL,
                        '单价'			TEXT    	NOT NULL,
                        '房源链接'		CHAR(100)	NOT NULL);''' % table_name
                cursor.execute(sql)

            sql = "INSERT INTO %s VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table_name
            cursor.execute(sql, house_info)
            conn.commit()

    @classmethod
    def judge_house_id(cls, table_name, *house_id):
        try:
            sql = "SELECT EXISTS(SELECT 1 FROM %s WHERE 房屋ID=?);" % table_name
            cursor.execute(sql, house_id)
        except:
            return (0,)
        else:
            return cursor.fetchone()

    @classmethod
    def get_house_price(cls, table_name, *house_id):
        try:
            sql = "SELECT 总价 FROM %s WHERE 房屋ID=?;" % table_name
            cursor.execute(sql, house_id)
        except:
            return (0,)
        else:
            return cursor.fetchone()

    @classmethod
    def write_compare_info(cls, table_name, *house_info):
        # print "write compare info, table_name=%s, House_quyu=%s, House_id=%s" % (table_name, house_info[0], house_info[1])
        if (cursor):
            try:
                sql = "SELECT * FROM sqlite_master WHERE type='table' AND name=?;"
                cursor.execute(sql, (table_name,))
            except:
                print 'No table named %s, we need create one!' % table_name

            if (cursor.fetchone()):	# 如果已经存在该表名，就不需要创建
                pass
            else:
                print 'create table'
                sql = '''CREATE TABLE %s ('区域'    TEXT NOT NULL,
                        '房屋ID'		    TEXT	    PRIMARY KEY NOT NULL,
                        '建筑面积'		TEXT    	NOT NULL,
                        '户型'			TEXT    	NOT NULL,
                        '楼层'			TEXT    	NOT NULL,
                        '年代'			TEXT    	NOT NULL,
                        '装修'			TEXT    	NOT NULL,
                        '环线'    		TEXT		NOT NULL,
                        '小区'			TEXT    	NOT NULL,
                        '原价'			INT      	NOT NULL,
                        '现价'			INT			NOT NULL,
                        '差额'			INT     	NOT NULL,
                        '单价'			TEXT    	NOT NULL,
                        '房源链接'		CHAR(100)	NOT NULL);''' % table_name
                cursor.execute(sql)

            sql = "INSERT INTO %s VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);" % table_name
            cursor.execute(sql, house_info)
            conn.commit()

    @classmethod
    def update_compare_table(cls, table_name, *changed_table):
        try:
            sql = "UPDATE %s SET 现价=?, 差额=? WHERE 房屋ID=?;" % table_name
            cursor.execute(sql, changed_table)
        except:
            print "update_compare_table, some error occur"
        else:
            conn.commit()

    @classmethod
    def update_compare_info(cls, table_name, *house_info):
        ret = Sqlite.judge_house_id(table_name, house_info[1])
        # 如何house_id在表格里已经存在，则更新该表格
        if ret[0] == 1:
            house_id = house_info[1]
            house_cur_price = house_info[10]
            house_different_price = house_info[11]
            cls.update_compare_table(table_name, house_cur_price, house_different_price, house_id)
        else:
            cls.write_compare_info(table_name, *house_info)
