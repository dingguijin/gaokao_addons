# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import math
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class SpScore(models.Model):
    _name = 'gaokao.sp_score'

    school_ref = fields.Many2one('gaokao.school', '院校REF', readonly=True)
    name = fields.Char(related='school_ref.name', store=True)

    school_id = fields.Integer(related='school_ref.school_id')
    school_province_name = fields.Char(related='school_ref.province_name', store=True)
    school_belong = fields.Char(related='school_ref.belong', store=True)
    school_is211 = fields.Boolean(related='school_ref.is_211', store=True)
    school_is985 = fields.Boolean(related='school_ref.is_985', store=True)
    school_isdual = fields.Boolean(related='school_ref.is_dual', store=True)
    school_isadmission = fields.Boolean(related='school_ref.is_admission', store=True)
    school_nature_name = fields.Char(related='school_ref.nature_name', store=True) # 公办/民办

    school_level_name = fields.Char(related='school_ref.level_name', store=True) # 普通本科/专科（高职）
    school_type_name = fields.Char(related='school_ref.type_name', store=True) # 理工 农 医学

    province_name = fields.Char('招生省份招生')
    province_id = fields.Integer('省ID')
    year = fields.Integer('年')

    zslx_id = fields.Integer('招生类型ID')
    zslx_name = fields.Char('招生类型')

    type_id = fields.Integer('type_id')
    type_name = fields.Char('考生类型')
    
    batch_name = fields.Char('录取批次')
    batch_id = fields.Integer('batch_id')
    
    min_score = fields.Integer('最低分')
    min_section = fields.Integer('最低排名')

    sp_info = fields.Char('专业信息')
    spname = fields.Char('专业名称')



    def _load_json_file(self, path, year, schools):
    
        _records = []
        with open(path) as _file:
            _data = _file.read() or "{}"
            _data = _data.replace("null", "\"\"")
            _data = eval(_data)
            if not _data:
                return []

            _logger.info(path)
            _logger.info(_data)
            if type(_data) is dict:
                return []
            for _items_data in _data:
                _logger.info(_items_data)
                _items = _items_data["data"]["item"]
                for _item in _items:
                    if _item["min"] == "-":
                        _item["min"] = 0

                    if _item["min_section"] == "-":
                        _item["min_section"] = 0

                    _record = {
                        "year": year,
                        "school_ref": schools[int(_item["school_id"])],

                        "province_name": _item["local_province_name"],
                        "type_name": _item["local_type_name"],
                        "batch_name": _item["local_batch_name"],

                        "sp_info": _item["sp_info"],
                        "spname": _item["spname"],

                        "min_score": math.floor(float(_item["min"])),
                        "min_section": int(_item["min_section"])}
                    _records.append(_record)
        return _records

    def _load_year(self, year, schools):
        _path = os.path.join(_json_data_dir, "api-sp-score/%s/api-sp-score" % year)
        _records = []
        for _j_path in os.walk(_path):
            _json_files = list(_j_path)[2]
            for _json_file in _json_files:
                _records += self._load_json_file(os.path.join(_path, _json_file), year, schools)
        return _records

    def reload_data(self):
        _set = self.env["gaokao.sp_score"].search([])
        _set.unlink()

        _schools_dict = {}
        _schools = self.env["gaokao.school"].search([])
        for _i in _schools:
            _schools_dict[_i.school_id] = _i.id

        _years = [2020, 2021, 2022]
        for _year in _years:
            _records = self._load_year(_year, _schools_dict)
            for _record in _records:
                self.env["gaokao.sp_score"].create(_record)
        return

