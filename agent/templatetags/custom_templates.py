import re
from django import template

register = template.Library()


@register.filter
def insert_br(value):
    # Insert <br> before each capital letter except the first one
    return re.sub(r'(?<!^)(?=[A-Z])', '<br>', value)


@register.filter
def format_animal_facts(value):
    # Split the input string into individual animal entries using '. ' as the delimiter
    entries = value.split('. ')

    result = []
    for entry in entries:
        # Strip any leading/trailing whitespace from the entry
        entry = entry.strip()
        if entry:
            # Split the entry into animal name and facts
            #entry entries
            #['Elephant;Can recognize their own reflection;Communicate using infrasound\n'
            # 'Dolphin;Can stay awake for two weeks;Have names for each other\n'
            # 'Cheetah;Fastest land animal;Can accelerate from 0 to 60 mph in 3 seconds\n'
            # 'Octopus;Have three hearts;Can regenerate lost limbs\n']
            animal, *facts = entry.split(';')
            #animal = 'Elephant'
            #facts = ['Can recognize their own reflection', 'Communicate using infrasound\n']
            # Format the animal name
            animal = animal.capitalize()
            # Format the facts for the animal
            facts = [f'- {fact.capitalize()}' for fact in facts]
            #facts = ['- Can recognize their own reflection', '- Communicate using infrasound']
            #combine the animal name and facts
            result.append(f'{animal}:\n{",\n ".join(facts)}\n')
            #result = ['Elephant:\n- Can recognize their own reflection, - Communicate using infrasound']

    # Return the formatted result as a single string
    return '\n'.join(result)


