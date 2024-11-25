### ITEM DIRECTORY

Here is a searchable list of all the items with links to their instructions:

{% for item in items %}
- [{{ item.item_str }} - {{ item.variation_str }}](content/{{ item.sku_stem }})
{% endfor %}
