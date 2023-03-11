# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import math
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class SchoolScore(models.Model):
    _name = 'gaokao.school_score'
    name = fields.Char('name')
    school_id = fields.Integer('院校ID')
    school_name = fields.Char('院校名称')

    province_name = fields.Char('省')
    province_id = fields.Integer('省ID')
    year = fields.Integer('年')

    zslx_id = fields.Integer('招生类型ID')
    zslx_name = fields.Char('招生类型(普通)')

    type_id = fields.Integer('type_id')
    type_name = fields.Char('type_name(文理)')
    
    batch_name = fields.Char('batch_name(录取批次)')
    batch_id = fields.Integer('batch_id')
    
    min_score = fields.Integer('最低分')
    min_section = fields.Integer('最低排名')

    def _load_json_file(self, path, year, schools, provinces, types):
    
        _records = []
        with open(path) as _file:
            _data = _file.read() or "{}"
            _data = _data.replace("null", "\"\"")
            _data = eval(_data)
            if not _data:
                return []

            _items = _data["data"]["item"]
            if not _items:
                return []

            for _item in _items:
                if _item["min"] == "-":
                    _item["min"] = 0

                _record = {
                    "year": year,
                    "school_id": int(_item["school_id"]),
                    "school_name": schools[int(_item["school_id"])],
                    "name": schools[int(_item["school_id"])],

                    "province_id": int(_item["province_id"]),
                    "province_name": provinces[int(_item["province_id"])],

                    "type_id": int(_item["type"]),
                    "type_name": types[int(_item["type"])],

                    "batch_id": int(_item["batch"]),
                    "batch_name": _item["local_batch_name"],

                    "zslx_id": int(_item["zslx"]),
                    "zslx_name": _item["zslx_name"],

                    "min_score": math.floor(float(_item["min"])),
                    "min_section": int(_item["min_section"])}
                _records.append(_record)
        return _records

    def _load_year(self, year, schools, provinces, types):
        _path = os.path.join(_json_data_dir, "api-school-score/%s" % year)
        _records = []
        for _j_path in os.walk(_path):
            _json_files = list(_j_path)[2]
            for _json_file in _json_files:
                _records += self._load_json_file(os.path.join(_path, _json_file), year, schools, provinces, types)
        return _records

    def reload_data(self):
        _set = self.env["gaokao.school_score"].search([])
        _set.unlink()

        _schools_dict = {}
        _schools = self.env["gaokao.school"].search([])
        for _i in _schools:
            _schools_dict[_i.school_id] = _i.name

        _provinces_dict = {}
        _provinces = self.env["gaokao.province"].search([])
        for _i in _provinces:
            _provinces_dict[_i.province_id] = _i.name

        _types_dict = {}
        _province_control = self.env["gaokao.province_control"].search([])
        for _i in _province_control:
            _types_dict[_i.type_id] = _i.type_name


        _years = [2020, 2021, 2022]
        for _year in _years:
            _records = self._load_year(_year, _schools_dict, _provinces_dict, _types_dict)
            for _record in _records:
                self.env["gaokao.school_score"].create(_record)
        return

