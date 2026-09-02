import os

for filepath in ['templates/clientes.html', 'templates/pecas.html', 'templates/servicos.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add toggle tabs
    url_name = 'lista_clientes' if 'clientes' in filepath else ('lista_pecas' if 'pecas' in filepath else 'lista_servicos')
    
    tabs_html = f'''    <div class="flex gap-4 border-b border-gray-200 dark:border-gray-700">
        <a href="{{% url '{url_name}' %}}" class="pb-2 px-1 border-b-2 font-medium text-sm {{% if not ver_arquivados %}}border-primary text-primary{{% else %}}border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300{{% endif %}}">
            Ativos
        </a>
        <a href="{{% url '{url_name}' %}}?arquivados=1" class="pb-2 px-1 border-b-2 font-medium text-sm {{% if ver_arquivados %}}border-primary text-primary{{% else %}}border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300{{% endif %}}">
            Arquivados
        </a>
    </div>'''
    
    content = content.replace(
        '<div class="bg-white dark:bg-gray-800 rounded-lg border dark:border-gray-700 shadow-sm overflow-hidden">',
        tabs_html + '\n    <div class="bg-white dark:bg-gray-800 rounded-lg border dark:border-gray-700 shadow-sm overflow-hidden mt-4">'
    )
    
    # Update button to Restore if arquivados
    if 'clientes' in filepath:
        old_form = '''<form action="{% url 'arquivar_cliente' cliente.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar este cliente?')">
                                        Arquivar
                                    </button>
                                </form>'''
        new_form = '''{% if ver_arquivados %}
                                <form action="{% url 'restaurar_cliente' cliente.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-green-600 dark:text-green-400 hover:underline font-medium" onclick="return confirm('Deseja restaurar este cliente?')">
                                        Restaurar
                                    </button>
                                </form>
                                {% else %}
                                <form action="{% url 'arquivar_cliente' cliente.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar este cliente?')">
                                        Arquivar
                                    </button>
                                </form>
                                {% endif %}'''
    elif 'pecas' in filepath:
        old_form = '''<form action="{% url 'arquivar_peca' peca.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar esta peça?')">
                                        Arquivar
                                    </button>
                                </form>'''
        new_form = '''{% if ver_arquivados %}
                                <form action="{% url 'restaurar_peca' peca.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-green-600 dark:text-green-400 hover:underline font-medium" onclick="return confirm('Deseja restaurar esta peça?')">
                                        Restaurar
                                    </button>
                                </form>
                                {% else %}
                                <form action="{% url 'arquivar_peca' peca.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar esta peça?')">
                                        Arquivar
                                    </button>
                                </form>
                                {% endif %}'''
    else:
        old_form = '''<form action="{% url 'arquivar_servico' servico.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar este serviço?')">
                                        Arquivar
                                    </button>
                                </form>'''
        new_form = '''{% if ver_arquivados %}
                                <form action="{% url 'restaurar_servico' servico.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-green-600 dark:text-green-400 hover:underline font-medium" onclick="return confirm('Deseja restaurar este serviço?')">
                                        Restaurar
                                    </button>
                                </form>
                                {% else %}
                                <form action="{% url 'arquivar_servico' servico.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar este serviço?')">
                                        Arquivar
                                    </button>
                                </form>
                                {% endif %}'''

    content = content.replace(old_form, new_form)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
