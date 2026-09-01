import os

def make_responsive(filepath, rows_old, rows_new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<thead class="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">', '<thead class="hidden sm:table-header-group text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">')
    content = content.replace('<thead class="text-xs text-gray-700 uppercase bg-gray-200">', '<thead class="hidden sm:table-header-group text-xs text-gray-700 uppercase bg-gray-200">')
    content = content.replace('<tbody class="divide-y divide-gray-200 dark:divide-gray-700 text-gray-900 dark:text-gray-100">', '<tbody class="divide-y divide-gray-200 dark:divide-gray-700 text-gray-900 dark:text-gray-100 flex flex-col sm:table-row-group">')
    content = content.replace('<tbody class="divide-y divide-gray-200">', '<tbody class="divide-y divide-gray-200 flex flex-col sm:table-row-group">')
    
    content = content.replace(rows_old, rows_new)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

clientes_old = """                        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                            <td class="px-6 py-4 font-semibold"><a href="{% url 'detalhe_cliente' cliente.id %}" class="text-primary hover:underline">{{ cliente.nome }}</a></td>
                            <td class="px-6 py-4">{{ cliente.telefone|default:"-" }}</td>
                            <td class="px-6 py-4">{{ cliente.veiculo|default:"-" }}</td>
                            <td class="px-6 py-4">{{ cliente.placa|default:"-" }}</td>
                            <td class="px-6 py-4 text-right">
                                <form action="{% url 'arquivar_cliente' cliente.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-red-500 hover:text-red-700 font-medium">
                                        Excluir
                                    </button>
                                </form>
                            </td>
                        </tr>"""
clientes_new = """                        <tr class="flex flex-col sm:table-row hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors p-4 sm:p-0">
                            <td class="px-2 sm:px-6 py-1 sm:py-4 font-semibold text-lg sm:text-sm"><a href="{% url 'detalhe_cliente' cliente.id %}" class="text-primary hover:underline">{{ cliente.nome }}</a></td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">Telefone: </span>{{ cliente.telefone|default:"-" }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">Veículo: </span>{{ cliente.veiculo|default:"-" }}</td>
                            <td class="px-2 sm:px-6 py-1 sm:py-4"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">Placa: </span>{{ cliente.placa|default:"-" }}</td>
                            <td class="px-2 sm:px-6 py-3 sm:py-4 sm:text-right mt-2 sm:mt-0 border-t sm:border-0 dark:border-gray-700 flex justify-end">
                                <form action="{% url 'arquivar_cliente' cliente.id %}" method="POST" class="inline">
                                    {% csrf_token %}
                                    <button type="submit" class="text-yellow-600 dark:text-yellow-400 hover:underline font-medium" onclick="return confirm('Deseja arquivar este cliente?')">
                                        Arquivar
                                    </button>
                                </form>
                            </td>
                        </tr>"""

make_responsive('templates/clientes.html', clientes_old, clientes_new)
