# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")

class School(models.Model):
    _name = 'gaokao.school'

    name = fields.Char('学校名称')
    school_id =  fields.Integer('学校ID')

    belong = fields.Char('归属')
    province_name = fields.Char('省')
    province_id = fields.Integer('省ID')

    city_id = fields.Integer('城市ID')
    city_name = fields.Char('市')

    county_id = fields.Integer('区ID')
    county_name = fields.Char('区')

    nature_id = fields.Integer('办学性质ID')
    nature_name = fields.Char('办学性质') # 公办/民办

    level_id = fields.Integer('办学范围ID')
    level_name = fields.Char('办学范围') # 普通本科/专科（高职）
    school_type = fields.Integer('学校类型') # 6000/6001

    type_id = fields.Integer('学校分类ID') # 理工 农 医学
    type_name = fields.Char('学校分类') # 理工 农 医学

    is_211 = fields.Boolean('211')
    is_985 = fields.Boolean('985')
    is_dual = fields.Boolean('双一流')
    is_admission = fields.Boolean('强基计划')


    def _prepare_school(self, school):
        _record = {
            "name": school["name"],
            "school_id": school["school_id"],
            "belong": school["belong"],
            "province_name": school["province_name"],
            "province_id": int(school["province_id"]),

            "city_id": int(school["city_id"]),
            "city_name": school["city_name"],

            "county_name": school["county_name"],
            "county_id": int(school["county_id"]),
            
            "nature_id": int(school["nature"]),
            "nature_name": school["nature_name"],

            "level_id": int(school["level"]),
            "level_name": school["level_name"],

            "school_type": int(school["school_type"]),

            "type_id": int(school["type"]),
            "type_name": school["type_name"],

            "is_211": bool(int(school["f211"]) == 1),
            "is_985": bool(int(school["f985"]) == 1),
            "is_dual": bool(school["dual_class"] == "38000"),
            "is_admission": bool(int(school["admissions"]) == 1)

        }
        return _record

    def reload_school_data(self):
        _set = self.env["gaokao.school"].search([])
        _set.unlink()

        _logger.info("import logging")
        _schools_path = os.path.join(_json_data_dir, "all_schools.json")
        with open(_schools_path) as _file:
            #_logger.info(_file.read())
            _all_schools = eval(_file.read())
            for _school in _all_schools:
                _new = self._prepare_school(_school)
                self.env["gaokao.school"].create(_new) 
        return

