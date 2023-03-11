# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class ProvinceControl(models.Model):
    _name = 'gaokao.province_control'

    name = fields.Char('name')
    province_name = fields.Char('省')
    province_id = fields.Integer('省ID')
    year = fields.Integer('年')
    type_id = fields.Integer('type_id')
    type_name = fields.Char('type_name')
    batch_name = fields.Char('batch_name')
    batch_id = fields.Integer('batch_id')
    score = fields.Integer('score')
    major_score = fields.Integer('major_score')
    rank = fields.Integer('rank')
    diff = fields.Integer('diff')

    def _prepare(self, item):
        _record = {
            "name": item["name"],
            "province_id": int(item["province_id"]),
            "province_name": item["province"],
            "type_id": int(item["type"]),
            "type_name": item["type_name"],
            "batch_name": item["batch_name"],
            "batch_id": int(item["batch"]),
            "score": int(item["score"]),
            "rank": int(item["rank"]),
            "year": int(item["year"]),
        }
        return _record

    def reload_data(self):
        _set = self.env["gaokao.province_control"].search([])
        _set.unlink()

        _path = os.path.join(_json_data_dir, "province_control_array.json")
        with open(_path) as _file:
            _all = eval(_file.read())
            for _item in _all:
                _data = _item["data"]
                #_logger.info(_item["province_id"])
                #_item["province_id"])
                _years = _data.values()
                for _year_item in _years:
                    _type_all = _year_item.values()
                    for _type_item in _type_all:
                        for _name_item in _type_item:
                            #_logger.info(_name_item)
                            _name_item["province_id"] = _item["province_id"]
                            _new = self._prepare(_name_item)
                            self.env["gaokao.province_control"].create(_new) 
        return

