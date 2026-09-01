import glob

files = glob.glob('templates/*.html')
for file_path in files:
    if "print" in file_path:
        continue # Don't touch print template

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cards / Forms
    content = content.replace('bg-white rounded-lg border shadow-sm', 'bg-white dark:bg-gray-800 rounded-lg border dark:border-gray-700 shadow-sm')
    
    # Inputs
    content = content.replace('bg-white text-gray-900 focus:outline-none', 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white dark:border-gray-600 focus:outline-none')
    content = content.replace('bg-white">', 'bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600">')
    
    # Labels
    content = content.replace('class="text-sm font-medium"', 'class="text-sm font-medium text-gray-700 dark:text-gray-300"')
    
    # H1 / Headers
    content = content.replace('text-2xl font-bold text-gray-900', 'text-2xl font-bold text-gray-900 dark:text-white')
    content = content.replace('text-lg font-semibold mb-4', 'text-lg font-semibold mb-4 dark:text-white')
    
    # Tables
    content = content.replace('text-xs text-gray-500 uppercase bg-gray-50', 'text-xs text-gray-500 dark:text-gray-400 uppercase bg-gray-50 dark:bg-gray-900/50')
    content = content.replace('divide-y divide-gray-200 text-gray-900', 'divide-y divide-gray-200 dark:divide-gray-700 text-gray-900 dark:text-gray-100')
    content = content.replace('hover:bg-gray-50 transition-colors', 'hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors')
    
    # Links
    content = content.replace('text-gray-500 hover:text-gray-900', 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white')
    
    # Orcamentos JS total card
    content = content.replace('bg-blue-50 rounded-lg border border-blue-100', 'bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-100 dark:border-blue-900/30')
    content = content.replace('text-blue-900', 'text-blue-900 dark:text-blue-100')
    content = content.replace('text-blue-700', 'text-blue-700 dark:text-blue-300')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
