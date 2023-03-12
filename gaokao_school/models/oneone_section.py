# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import math
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class OneoneSection(models.Model):
    _name = 'gaokao.oneone_section'

    name = fields.Char('分数')
    rank = fields.Char('分数段')

    num = fields.Integer('本段人数')
    total = fields.Integer('累计人数')

    province_name = fields.Char('招生省份')
    province_id = fields.Integer('省ID')
    year = fields.Integer('年')

    type_name = fields.Char('type_name(文理)')
    score_name = fields.Char('score_name(成绩类型)')
    
    def _load_json_file(self, path, year, provinces, types):
    
        _json_file = os.path.basename(path)
        _ss = _json_file.split(".")[0].split("_")
        _province_id = int(_ss[1])
        _type_id = int(_ss[2])
        _score_id = _ss[3]

        _province_name = provinces[_province_id]
        _type_name = types[_type_id]

        _records = []
        with open(path) as _file:
            _data = _file.read() or "{}"
            _data = _data.replace("null", "\"\"")
            _data = eval(_data)
            if not _data:
                return []

            _items = _data["data"]["search"]
            if not _items:
                return []

            for _key in _items:
                _value = _items[_key]

                _record = {
                    "year": year,
                    "province_id": _province_id,
                    "province_name": _province_name,
                    "type_name": _type_name,
                    "score_name": _score_id,
                    "name": _key,
                    "rank": _value["rank"],
                    "num": int(_value["num"]),
                    "total": int(_value["total"])}

                _records.append(_record)
        return _records

    def _load_year(self, year, provinces, types):
        _path = os.path.join(_json_data_dir, "api-oneone-section/%s" % year)
        _records = []
        for _j_path in os.walk(_path):
            _json_files = list(_j_path)[2]
            _logger.info(_json_files)
            for _json_file in _json_files:
                _records += self._load_json_file(os.path.join(_path, _json_file), year, provinces, types)
        return _records

    def reload_data(self):
        _set = self.env["gaokao.oneone_section"].search([])
        _set.unlink()

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
            _records = self._load_year(_year, _provinces_dict, _types_dict)
            _logger.info("oneone section load year: %s" % _year)
            _logger.info(_records)
            for _record in _records:
                self.env["gaokao.oneone_section"].create(_record)
        return

