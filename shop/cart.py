"""Shopping cart kept in the visitor's session. Each line is one bottle with its own gift choice."""
import uuid

from .models import GIFT_COLORS, GiftPerfume, Variant

SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.lines = self.session.get(SESSION_KEY, [])

    def _save(self):
        self.session[SESSION_KEY] = self.lines
        self.session.modified = True

    def add(self, data):
        self.lines.append({
            'id': uuid.uuid4().hex[:12],
            'variant': data['variant'].pk,
            'gift_color': data.get('gift_color') or '',
            'engraving': (data.get('engraving') or '').strip(),
            'perfumes': [g.pk for g in data.get('gift_perfumes') or []],
        })
        self._save()

    def remove(self, line_id):
        self.lines = [line for line in self.lines if line['id'] != line_id]
        self._save()

    def clear(self):
        self.lines = []
        self._save()

    def __len__(self):
        return len(self.lines)

    def items(self):
        """Lines resolved to objects; lines whose perfume was removed from the shop are dropped."""
        variants = Variant.objects.select_related('product').in_bulk([line['variant'] for line in self.lines])
        perfumes = GiftPerfume.objects.in_bulk([pk for line in self.lines for pk in line['perfumes']])
        colors = dict(GIFT_COLORS)
        out = []
        for line in self.lines:
            variant = variants.get(line['variant'])
            if not variant or not variant.product.is_active:
                continue
            out.append({
                'id': line['id'],
                'variant': variant,
                'gift_color': line['gift_color'],
                'gift_color_label': colors.get(line['gift_color'], ''),
                'engraving': line['engraving'],
                'perfumes': [perfumes[pk] for pk in line['perfumes'] if pk in perfumes],
            })
        return out

    @staticmethod
    def totals(items):
        total = sum(i['variant'].price for i in items)
        old = sum(i['variant'].old_price or i['variant'].price for i in items)
        return {'total': total, 'old_total': old, 'saving': old - total}
