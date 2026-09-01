import os

def make_responsive(filepath, rows_old, rows_new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<thead class="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">', '<thead class="hidden sm:table-header-group text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">')
    content = content.replace('<tbody class="divide-y divide-gray-200 dark:divide-gray-700">', '<tbody class="divide-y divide-gray-200 dark:divide-gray-700 flex flex-col sm:table-row-group">')
    
    content = content.replace(rows_old, rows_new)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

orcamentos_old = """                        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                            <td class="px-6 py-4">
                                <div class="font-semibold text-gray-900 dark:text-white">#{{ orcamento.id|stringformat:"04d" }}</div>
                            </td>
                            <td class="px-6 py-4">
                                <a href="{% url 'detalhe_cliente' orcamento.cliente.id %}" class="text-primary hover:underline font-medium">{{ orcamento.cliente.nome }}</a>
                            </td>
                            <td class="px-6 py-4 font-medium">{{ orcamento.criado_em|date:"d/m/Y H:i" }}</td>
                            <td class="px-6 py-4">
                                <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full 
                                    {% if orcamento.status == 'APROVADO' %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400
                                    {% elif orcamento.status == 'REJEITADO' %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400
                                    {% else %}bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400{% endif %}">
                                    {{ orcamento.get_status_display }}
                                </span>
                            </td>
                            <td class="px-6 py-4 font-bold text-gray-900 dark:text-white">R$ {{ orcamento.total }}</td>
                            <td class="px-6 py-4 text-right space-x-2">
                                <a href="{% url 'imprimir_orcamento' orcamento.id %}" target="_blank" class="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-3 py-1 rounded text-xs font-bold hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors" title="Imprimir PDF">
                                    PDF
                                </a>
                                {% if orcamento.status == 'PENDENTE' %}
                                <form action="{% url 'aprovar_orcamento' orcamento.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 px-3 py-1 rounded text-xs font-bold hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors">
                                        Aprovar
                                    </button>
                                </form>
                                {% endif %}
                                <form action="{% url 'arquivar_orcamento' orcamento.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-red-500 hover:text-red-700 font-medium text-sm ml-2">
                                        Excluir
                                    </button>
                                </form>
                            </td>
                        </tr>"""
orcamentos_new = """                        <tr class="flex flex-col sm:table-row hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors p-4 sm:p-0">
                            <td class="px-2 sm:px-6 py-1 sm:py-4">
                                <div class="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                                    <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">ID: </span>
                                    #{{ orcamento.id|stringformat:"04d" }}
                                </div>
                            </td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4">
                                <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2">Cliente: </span>
                                <a href="{% url 'detalhe_cliente' orcamento.cliente.id %}" class="text-primary hover:underline font-medium text-lg sm:text-sm">{{ orcamento.cliente.nome }}</a>
                            </td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4 font-medium"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2 font-normal">Data: </span>{{ orcamento.criado_em|date:"d/m/Y H:i" }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4">
                                <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2">Status: </span>
                                <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full 
                                    {% if orcamento.status == 'APROVADO' %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400
                                    {% elif orcamento.status == 'REJEITADO' %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400
                                    {% else %}bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400{% endif %}">
                                    {{ orcamento.get_status_display }}
                                </span>
                            </td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4 font-bold text-gray-900 dark:text-white"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2 font-normal">Total: </span>R$ {{ orcamento.total }}</td>
                            <td class="px-2 sm:px-6 py-3 sm:py-4 sm:text-right space-x-2 mt-2 sm:mt-0 border-t sm:border-0 dark:border-gray-700 flex flex-wrap gap-2 justify-end items-center">
                                <a href="{% url 'imprimir_orcamento' orcamento.id %}" target="_blank" class="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-3 py-1 rounded text-xs font-bold hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors" title="Imprimir PDF">
                                    PDF
                                </a>
                                {% if orcamento.status == 'PENDENTE' %}
                                <form action="{% url 'aprovar_orcamento' orcamento.id %}" method="POST" class="inline m-0">
                                    {% csrf_token %}
                                    <button type="submit" class="bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 px-3 py-1 rounded text-xs font-bold hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors">
                                        Aprovar
                                    </button>
                                </form>
                                {% endif %}
                                <form action="{% url 'arquivar_orcamento' orcamento.id %}" method="POST" class="inline m-0">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium text-sm ml-2" onclick="return confirm('Deseja arquivar este orçamento?')">
                                        Arquivar
                                    </button>
                                </form>
                            </td>
                        </tr>"""

make_responsive('templates/orcamentos.html', orcamentos_old, orcamentos_new)
