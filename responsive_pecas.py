import os

def make_responsive(filepath, rows_old, rows_new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<thead class="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">', '<thead class="hidden sm:table-header-group text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">')
    content = content.replace('<tbody class="divide-y divide-gray-200 dark:divide-gray-700 text-gray-900 dark:text-gray-100">', '<tbody class="divide-y divide-gray-200 dark:divide-gray-700 text-gray-900 dark:text-gray-100 flex flex-col sm:table-row-group">')
    
    content = content.replace(rows_old, rows_new)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

pecas_old = """                        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                            <td class="px-6 py-4 font-semibold">{{ peca.nome }}</td>
                            <td class="px-6 py-4">R$ {{ peca.preco_custo }}</td>
                            <td class="px-6 py-4">R$ {{ peca.preco_venda }}</td>
                            <td class="px-6 py-4">
                                <span class="px-2 py-1 text-xs font-bold rounded-full {% if peca.estoque <= 5 %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400{% else %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400{% endif %}">
                                    {{ peca.estoque }}
                                </span>
                            </td>
                            <td class="px-6 py-4 text-right">
                                <form action="{% url 'arquivar_peca' peca.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-red-500 hover:text-red-700 font-medium">
                                        Excluir
                                    </button>
                                </form>
                            </td>
                        </tr>"""
pecas_new = """                        <tr class="flex flex-col sm:table-row hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors p-4 sm:p-0">
                            <td class="px-2 sm:px-6 py-1 sm:py-4 font-semibold text-lg sm:text-sm">{{ peca.nome }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">Custo: </span>R$ {{ peca.preco_custo }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">Venda: </span>R$ {{ peca.preco_venda }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4">
                                <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2">Estoque: </span>
                                <span class="px-2 py-1 text-xs font-bold rounded-full {% if peca.estoque <= 5 %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400{% else %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400{% endif %}">
                                    {{ peca.estoque }}
                                </span>
                            </td>
                            <td class="px-2 sm:px-6 py-3 sm:py-4 sm:text-right mt-2 sm:mt-0 border-t sm:border-0 dark:border-gray-700 flex justify-end">
                                <form action="{% url 'arquivar_peca' peca.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar esta peça?')">
                                        Arquivar
                                    </button>
                                </form>
                            </td>
                        </tr>"""

make_responsive('templates/pecas.html', pecas_old, pecas_new)
