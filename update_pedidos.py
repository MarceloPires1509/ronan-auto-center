with open('templates/pedidos.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Insert Faturar Button in actions column
if '<th class="px-6 py-3 text-center sm:text-right">Atualizar Status</th>' in content:
    content = content.replace('<th class="px-6 py-3 text-center sm:text-right">Atualizar Status</th>', '<th class="px-6 py-3 text-center sm:text-right">Ações / Status</th>')

# find the form for status
old_form = '''                                    <select name="status" class="w-full sm:w-48 border rounded px-2 py-2 text-sm font-bold uppercase focus:ring-primary focus:border-primary dark:bg-gray-700 dark:border-gray-600 dark:text-white
                                        {% if pedido.status == 'APROVADO' %}text-yellow-600 dark:text-yellow-400
                                        {% elif pedido.status == 'OFICINA' %}text-blue-600 dark:text-blue-400
                                        {% elif pedido.status == 'TESTANDO' %}text-purple-600 dark:text-purple-400
                                        {% elif pedido.status == 'FINALIZADO' %}text-green-600 dark:text-green-400{% endif %}" onchange="this.form.submit()">
                                        <option value="APROVADO" {% if pedido.status == 'APROVADO' %}selected{% endif %}>Aprovado (Fila)</option>
                                        <option value="OFICINA" {% if pedido.status == 'OFICINA' %}selected{% endif %}>Na Oficina</option>
                                        <option value="TESTANDO" {% if pedido.status == 'TESTANDO' %}selected{% endif %}>Testando</option>
                                        <option value="FINALIZADO" {% if pedido.status == 'FINALIZADO' %}selected{% endif %}>Finalizado (Entregue)</option>
                                    </select>'''

new_form = '''                                    <select name="status" class="w-full sm:w-48 border rounded px-2 py-2 text-sm font-bold uppercase focus:ring-primary focus:border-primary dark:bg-gray-700 dark:border-gray-600 dark:text-white
                                        {% if pedido.status == 'APROVADO' %}text-yellow-600 dark:text-yellow-400
                                        {% elif pedido.status == 'OFICINA' %}text-blue-600 dark:text-blue-400
                                        {% elif pedido.status == 'TESTANDO' %}text-purple-600 dark:text-purple-400
                                        {% elif pedido.status == 'FINALIZADO' %}text-green-600 dark:text-green-400{% endif %}" onchange="this.form.submit()">
                                        <option value="APROVADO" {% if pedido.status == 'APROVADO' %}selected{% endif %}>Aprovado (Fila)</option>
                                        <option value="OFICINA" {% if pedido.status == 'OFICINA' %}selected{% endif %}>Na Oficina</option>
                                        <option value="TESTANDO" {% if pedido.status == 'TESTANDO' %}selected{% endif %}>Testando</option>
                                        <option value="FINALIZADO" {% if pedido.status == 'FINALIZADO' %}selected{% endif %}>Finalizado (Entregue)</option>
                                    </select>
                                    
                                    {% if pedido.pagamentos.count == 0 %}
                                    <button type="button" onclick="abrirModalFaturar({{ pedido.id }}, '{{ pedido.total|stringformat:'.2f'|default:'0.00' }}')" class="w-full sm:w-auto bg-green-600 text-white px-3 py-2 rounded font-semibold text-sm hover:bg-green-700 transition-colors flex items-center justify-center gap-1 mt-2 sm:mt-0 ml-0 sm:ml-2">
                                        <i data-lucide="dollar-sign" class="w-4 h-4"></i> Faturar
                                    </button>
                                    {% else %}
                                    <span class="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-bold w-full sm:w-auto text-center mt-2 sm:mt-0 ml-0 sm:ml-2"><i data-lucide="check-circle" class="w-4 h-4 inline"></i> PAGO</span>
                                    {% endif %}'''

content = content.replace(old_form, new_form)

# Add Modal
modal = '''
<div id="modal-faturar" class="hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl w-full max-w-sm overflow-hidden">
        <div class="px-6 py-4 border-b dark:border-gray-700 flex justify-between items-center">
            <h3 class="font-bold text-lg dark:text-white">Faturar Serviço</h3>
            <button onclick="document.getElementById('modal-faturar').classList.add('hidden')" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>
        </div>
        <form id="form-faturar" method="POST" class="p-6 space-y-4">
            {% csrf_token %}
            <div class="text-center mb-4">
                <p class="text-sm text-gray-500 dark:text-gray-400">Total a Receber</p>
                <p class="text-3xl font-bold text-green-600 dark:text-green-400">R$ <span id="modal-faturar-total">0,00</span></p>
            </div>
            <div class="space-y-2">
                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Forma de Pagamento principal</label>
                <select name="forma_pagamento" required class="w-full px-3 py-2 border rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-green-500">
                    <option value="PIX">PIX</option>
                    <option value="Dinheiro">Dinheiro</option>
                    <option value="Cartão de Crédito">Cartão de Crédito</option>
                    <option value="Cartão de Débito">Cartão de Débito</option>
                </select>
            </div>
            <div class="pt-4 flex justify-end gap-3">
                <button type="button" onclick="document.getElementById('modal-faturar').classList.add('hidden')" class="px-4 py-2 border rounded-md font-medium text-gray-500 hover:bg-gray-50">Cancelar</button>
                <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded-md font-medium hover:bg-green-700">Confirmar Pagamento</button>
            </div>
        </form>
    </div>
</div>
<script>
function abrirModalFaturar(id, total) {
    document.getElementById('form-faturar').action = '/pedidos/faturar/' + id + '/';
    document.getElementById('modal-faturar-total').innerText = total;
    document.getElementById('modal-faturar').classList.remove('hidden');
}
</script>
'''

if 'id="modal-faturar"' not in content:
    content = content.replace('{% endblock %}', modal + '\n{% endblock %}')

with open('templates/pedidos.html', 'w', encoding='utf-8') as f:
    f.write(content)
