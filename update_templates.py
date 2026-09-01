import glob

for filename in ['clientes.html', 'pecas.html', 'servicos.html', 'orcamentos.html']:
    filepath = f'templates/{filename}'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change 'excluir_' to 'arquivar_'
    content = content.replace("action=\"{% url 'excluir_", "action=\"{% url 'arquivar_")
    content = content.replace("value=\"Excluir\"", "value=\"Arquivar\"")
    content = content.replace("text-red-600 dark:text-red-400 hover:underline bg-transparent border-none cursor-pointer", "text-yellow-600 dark:text-yellow-400 hover:underline bg-transparent border-none cursor-pointer font-medium")
    content = content.replace("return confirm('Tem certeza", "return confirm('Deseja arquivar")
    
    if filename == 'clientes.html':
        content = content.replace(
            '<td class="px-6 py-4">{{ cliente.nome }}</td>',
            '<td class="px-6 py-4 font-semibold"><a href="{% url \'detalhe_cliente\' cliente.id %}" class="text-primary hover:underline">{{ cliente.nome }}</a></td>'
        )
        content = content.replace(
            '<td class="px-6 py-4 font-medium">{{ cliente.nome }}</td>',
            '<td class="px-6 py-4 font-semibold"><a href="{% url \'detalhe_cliente\' cliente.id %}" class="text-primary hover:underline">{{ cliente.nome }}</a></td>'
        )
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
