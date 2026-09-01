import os

def make_responsive(filepath, rows_old, rows_new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('<thead class="text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">', '<thead class="hidden sm:table-header-group text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50">')
    content = content.replace('<tbody class="divide-y divide-gray-200 dark:divide-gray-700">', '<tbody class="divide-y divide-gray-200 dark:divide-gray-700 flex flex-col sm:table-row-group">')
    
    content = content.replace(rows_old, rows_new)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

detail_old = """                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                        <td class="px-6 py-4">
                            <div class="font-semibold text-gray-900 dark:text-white">#{{ orc.id|stringformat:"04d" }}</div>
                            <div class="text-xs text-gray-500">{{ orc.criado_em|date:"d/m/Y H:i" }}</div>
                        </td>
                        <td class="px-6 py-4">
                            <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full 
                                {% if orc.status == 'APROVADO' %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400
                                {% elif orc.status == 'REJEITADO' %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400
                                {% else %}bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400{% endif %}">
                                {{ orc.get_status_display }}
                            </span>
                        </td>
                        <td class="px-6 py-4 text-right">R$ {{ orc.total_pecas }}</td>
                        <td class="px-6 py-4 text-right">R$ {{ orc.total_mao_de_obra }}</td>
                        <td class="px-6 py-4 text-right font-bold text-gray-900 dark:text-white">R$ {{ orc.total }}</td>
                        <td class="px-6 py-4 text-center">
                            <a href="{% url 'imprimir_orcamento' orc.id %}" target="_blank" class="text-primary hover:underline font-medium">Ver / Imprimir</a>
                        </td>
                    </tr>"""
detail_new = """                    <tr class="flex flex-col sm:table-row hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors p-4 sm:p-0">
                        <td class="px-2 sm:px-6 py-1 sm:py-4 flex justify-between sm:table-cell items-center">
                            <div class="flex items-center gap-2">
                                <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase">ID: </span>
                                <div class="font-semibold text-gray-900 dark:text-white text-lg sm:text-sm">#{{ orc.id|stringformat:"04d" }}</div>
                            </div>
                            <div class="text-xs text-gray-500 sm:mt-1">{{ orc.criado_em|date:"d/m/Y H:i" }}</div>
                        </td>
                        <td class="px-2 sm:px-6 py-1 sm:py-4">
                            <span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2">Status: </span>
                            <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full 
                                {% if orc.status == 'APROVADO' %}bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400
                                {% elif orc.status == 'REJEITADO' %}bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400
                                {% else %}bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400{% endif %}">
                                {{ orc.get_status_display }}
                            </span>
                        </td>
                        <td class="px-2 sm:px-6 py-1 sm:py-4 sm:text-right"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2 font-normal">Peças: </span>R$ {{ orc.total_pecas }}</td>
                        <td class="px-2 sm:px-6 py-1 sm:py-4 sm:text-right"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2 font-normal">Serviços: </span>R$ {{ orc.total_mao_de_obra }}</td>
                        <td class="px-2 sm:px-6 py-1 sm:py-4 sm:text-right font-bold text-gray-900 dark:text-white"><span class="sm:hidden font-medium text-gray-500 dark:text-gray-400 text-xs uppercase mr-2 font-normal">Total: </span>R$ {{ orc.total }}</td>
                        <td class="px-2 sm:px-6 py-3 sm:py-4 sm:text-center mt-2 sm:mt-0 border-t sm:border-0 dark:border-gray-700 flex justify-end">
                            <a href="{% url 'imprimir_orcamento' orc.id %}" target="_blank" class="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-4 py-2 sm:bg-transparent sm:p-0 sm:text-primary rounded sm:rounded-none text-sm sm:hover:underline font-bold sm:font-medium text-center w-full sm:w-auto">Ver / Imprimir</a>
                        </td>
                    </tr>"""

make_responsive('templates/cliente_detail.html', detail_old, detail_new)
