# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
_json_data_dir = os.path.join(os.path.dirname(__file__), "../../json_data")
_provinces = ["北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",  "宁夏", "新疆"]

class Province(models.Model):
    _name = 'gaokao.province'

    name = fields.Char('省')
    province_id = fields.Integer('省ID')

    def reload_data(self):
        _set = self.env["gaokao.province"].search([])
        _set.unlink()


        _logger.info("import logging")
        _path = os.path.join(_json_data_dir, "province_control.json")
        with open(_path) as _file:
            _all = eval(_file.read())
            x_province = _all["data"]["province"]
            for index, id in enumerate(x_province):
                d = {}
                d["name"] = _provinces[index]
                d["province_id"] = int(id)        
                self.env["gaokao.province"].create(d) 
        return

