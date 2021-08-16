# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _
from lxml import etree
import collections
import logging
_logger = logging.getLogger(__name__)

try:
    from facturacion_electronica import facturacion_electronica
except Exception as e:
    _logger.warning("Problema al cargar Facturación electrónica: %s" % str(e))

class SIIXMLEnvio(models.Model):
    _inherit = 'sii.xml.envio'

    def get_cesion_send_status(self):
        datos = self._get_datos_empresa(self.company_id)
        datos.update({
            'codigo_envio':self.sii_send_ident,
            'cesion': True
        })
        res = facturacion_electronica.consulta_estado_dte(datos)
        print('F'*100)
        print(res)
        print('F' * 100)
        self.write({
            'state': res['status'],
            'sii_xml_response': res['xml_resp'],
        })
