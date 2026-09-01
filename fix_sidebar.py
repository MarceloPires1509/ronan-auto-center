import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded active state for Dashboard
content = content.replace(
    'href="{% url \'dashboard\' %}" class="flex items-center gap-3 px-3 py-2 bg-primary text-white rounded-md font-medium"',
    'href="{% url \'dashboard\' %}" class="flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-colors {% if request.resolver_match.url_name == \'dashboard\' %}bg-primary text-white{% else %}text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700{% endif %}"'
)

# Function to replace other links
def make_dynamic(url_name_base, url_name_match):
    old = f'href="{{% url \'{url_name_base}\' %}}" class="flex items-center gap-3 px-3 py-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md font-medium transition-colors"'
    new = f'href="{{% url \'{url_name_base}\' %}}" class="flex items-center gap-3 px-3 py-2 rounded-md font-medium transition-colors {{% if \'{url_name_match}\' in request.path %}}bg-primary text-white{{% else %}}text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700{{% endif %}}"'
    return old, new

replaces = [
    ('lista_clientes', 'clientes'),
    ('lista_pecas', 'pecas'),
    ('lista_servicos', 'servicos'),
    ('lista_orcamentos', 'orcamentos'),
]

for url_base, url_match in replaces:
    old, new = make_dynamic(url_base, url_match)
    content = content.replace(old, new)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
