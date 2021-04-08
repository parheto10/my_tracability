# yourapp/lookups.py
from ajax_select import register, LookupChannel
from .models import Parcelle, Producteur, Planting
from django.db.models import Q
from django.utils.html import escape

import ajax_select
from ajax_select import LookupChannel


class ProducteurLookup(LookupChannel):
    model = Producteur

    def get_query(self, q, request):
        return Producteur.objects.filter(Q(nom__icontains=q) |Q(prenoms__icontains=q)).order_by('nom')

    def get_result(self, obj):
        """ result is the simple text that is the completion of what the person typed """
        return obj.nom

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return f"{escape(obj.nom)}<div><i>{escape(obj.prenoms)}</i></div>"
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return f"{escape(obj.nom)}<div><i>{escape(obj.prenoms)}</i></div>"

# @register('producteur')
# class ParcelleLookup(LookupChannel):
#
#     model = Parcelle
#
#     def get_query(self, q, request):
#         return self.model.objects.filter(producteur__nom__icontains=q).order_by('producteur__nom')[:25]
#
#     def format_item_display(self, item):
#         return u"<span class='producteur'>%s %s</span>" % item.producteur.nom, item.producteur.prenoms