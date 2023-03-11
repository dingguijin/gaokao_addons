# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class SpScore(models.Model):
    _name = 'gaokao.sp_score'
    '''
    {
        "school_id": "1871",
        "province_id": "62",
        "type": "1",
        "batch": "119",
        "zslx": "0",
        "xclevel": "0",
        "max": "-",
        "min_section": "112687",
        "min": "160",
        "average": "-",
        "filing": "160",
        "first_km": "0",
        "local_batch_name": "高职（专科）批R段",
        "zslx_name": "普通类",
        "proscore": "160",
        "year": "2022"
      }
      '''
    name = fields.Char('name')
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


    def _prepare(self, item):
        _record = {
        }
        return _record

    def _load_year(self, year, schools, provinces, province_control):
        _path = os.path.join(_json_data_dir, "api-school-score/%s" % year)
        for _j_path in os.walk(_path):
            _json_files = list(_j_path)[2]
            for _json_file in _json_files:
                print(_json_file)
        return

    def reload_data(self):
        _set = self.env["gaokao.school_score"].search([])
        _set.unlink()

        _schools = self.env["gaokao.school"].search([])
        _provinces = self.env["gaokao.province"].search([])
        _province_control = self.env["gaokao.province_control"].search([])

        _years = [2020, 2021, 2022]
        for _year in _years:
            self._load_year(_year, _schools, _provinces, _province_control)
        return

