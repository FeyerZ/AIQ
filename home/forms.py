from django import forms

class SelectionForm(forms.Form):
    MAJOR_CHOICES = [
        ('disabled selected', 'Select a Major'),
        ('computer_science', 'Computer Science'),
        ('business', 'Business Administration'),
        ('engineering', 'Engineering'),
        ('biology', 'Biology'),
    ]

    CHAPTER_CHOICES = {
        'computer_science': [
            ('programming', 'Programming'),
            ('data_structures', 'Data Structures'),
            ('algorithms', 'Algorithms'),
            ('databases', 'Databases'),
            ('web_development', 'Web Development'),
        ],
        'business': [
            ('accounting', 'Accounting'),
            ('marketing', 'Marketing'),
            ('management', 'Management'),
            ('finance', 'Finance'),
            ('entrepreneurship', 'Entrepreneurship'),
        ],
        'engineering': [
            ('thermodynamics', 'Thermodynamics'),
            ('circuits', 'Circuits'),
            ('materials_science', 'Materials Science'),
            ('fluid_mechanics', 'Fluid Mechanics'),
            ('mechanics', 'Mechanics'),
        ],
        'biology': [
            ('genetics', 'Genetics'),
            ('cell_biology', 'Cell Biology'),
            ('ecology', 'Ecology'),
            ('evolution', 'Evolution'),
            ('microbiology', 'Microbiology'),
        ],
    }

    domain = forms.ChoiceField(choices=MAJOR_CHOICES)
    subdomain = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        if 'domain' in self.data:
            domain = self.data.get('domain')
            self.fields['subdomain'].choices = self.CHAPTER_CHOICES.get(domain, [])
        else:
            self.fields['subdomain'].choices = []
