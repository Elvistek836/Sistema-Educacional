import os

path = r'c:\Users\benja\OneDrive\Escritorio\Proyectos\Sistema_Educacional\horarios\templates\modificar_horario.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
target_line_content = '<option value="{{x.id}}" data-nombre="{{x.nombre}}">{{x.nombre}} ({{x.codigo}})</option>'

replacements_count = 0
already_updated_count = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    
    if stripped == target_line_content:
        # Check if already updated
        # The updated block looks like:
        # {% if full_asg_ids ... %}
        #    <option ... disabled ...>
        # {% else %}
        #    <option ...>  <-- We are here
        # {% endif %}
        
        is_updated = False
        if i > 0:
            prev_line = lines[i-1].strip()
            if prev_line == '{% else %}':
                # Check further back for the if
                for k in range(2, 6):
                    if i-k >= 0:
                        l = lines[i-k].strip()
                        if '{% if full_asg_ids' in l or '{% elif full_asg_ids' in l:
                            is_updated = True
                            break
        
        if is_updated:
            new_lines.append(line)
            already_updated_count += 1
        else:
            # Replace
            indent = line[:line.find('<')]
            block = []
            block.append(f'{indent}{{% if full_asg_ids and x.id in full_asg_ids %}}\n')
            block.append(f'{indent}    <option value="{{{{x.id}}}}" data-nombre="{{{{x.nombre}}}}" disabled>{{{{x.nombre}}}} ({{{{x.codigo}}}})</option>\n')
            block.append(f'{indent}{{% else %}}\n')
            block.append(f'{indent}    <option value="{{{{x.id}}}}" data-nombre="{{{{x.nombre}}}}">{{{{x.nombre}}}} ({{{{x.codigo}}}})</option>\n')
            block.append(f'{indent}{{% endif %}}\n')
            
            new_lines.extend(block)
            replacements_count += 1
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Total found: {replacements_count + already_updated_count}")
print(f"Already updated: {already_updated_count}")
print(f"Replaced: {replacements_count}")
