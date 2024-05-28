from django import forms

from django import forms


class SelectionForm(forms.Form):
    MAJOR_CHOICES = [
        ('disabled selected', 'Select a Domain'),
        ('arts_and_crafts', 'Arts and Crafts'),
        ('story_time', 'Story Time'),
        ('science_experiments', 'Science Experiments'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('nature_and_environment', 'Nature and Environment'),
        ('languages', 'Languages'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('computer_science', 'Computer Science'),
        ('business', 'Business Administration'),
        ('engineering', 'Engineering'),
        ('biology', 'Biology'),
        ('psychology', 'Psychology'),
        ('education', 'Education'),
        ('art', 'Art and Design'),
        ('literature', 'Literature'),
        ('mathematics', 'Mathematics'),
    ]

    CHAPTER_CHOICES = {
        'arts_and_crafts': [
            ('drawing', 'Drawing'),
            ('painting', 'Painting'),
            ('origami', 'Origami'),
            ('clay_modeling', 'Clay Modeling'),
            ('collage', 'Collage'),
        ],
        'story_time': [
            ('fairy_tales', 'Fairy Tales'),
            ('adventure_stories', 'Adventure Stories'),
            ('animal_stories', 'Animal Stories'),
            ('fantasy', 'Fantasy'),
            ('bedtime_stories', 'Bedtime Stories'),
        ],
        'science_experiments': [
            ('simple_chemistry', 'Simple Chemistry'),
            ('plant_growth', 'Plant Growth'),
            ('magnetism', 'Magnetism'),
            ('water_cycle', 'Water Cycle'),
            ('volcano_eruption', 'Volcano Eruption'),
        ],
        'sports': [
            ('soccer', 'Soccer'),
            ('basketball', 'Basketball'),
            ('swimming', 'Swimming'),
            ('gymnastics', 'Gymnastics'),
            ('track_and_field', 'Track and Field'),
        ],
        'music': [
            ('singing', 'Singing'),
            ('playing_instruments', 'Playing Instruments'),
            ('music_theory', 'Music Theory'),
            ('composing', 'Composing'),
            ('music_history', 'Music History'),
        ],
        'computer_science': [
            ('programming', 'Programming'),
            ('data_structures', 'Data Structures'),
            ('algorithms', 'Algorithms'),
            ('databases', 'Databases'),
            ('web_development', 'Web Development'),
            ('machine_learning', 'Machine Learning'),
            ('cyber_security', 'Cyber Security'),
        ],
        'business': [
            ('accounting', 'Accounting'),
            ('marketing', 'Marketing'),
            ('management', 'Management'),
            ('finance', 'Finance'),
            ('entrepreneurship', 'Entrepreneurship'),
            ('business_ethics', 'Business Ethics'),
            ('supply_chain', 'Supply Chain Management'),
        ],
        'engineering': [
            ('thermodynamics', 'Thermodynamics'),
            ('circuits', 'Circuits'),
            ('materials_science', 'Materials Science'),
            ('fluid_mechanics', 'Fluid Mechanics'),
            ('mechanics', 'Mechanics'),
            ('control_systems', 'Control Systems'),
            ('robotics', 'Robotics'),
        ],
        'biology': [
            ('genetics', 'Genetics'),
            ('cell_biology', 'Cell Biology'),
            ('ecology', 'Ecology'),
            ('evolution', 'Evolution'),
            ('microbiology', 'Microbiology'),
            ('anatomy', 'Anatomy'),
            ('physiology', 'Physiology'),
        ],
        'psychology': [
            ('cognitive_psychology', 'Cognitive Psychology'),
            ('developmental_psychology', 'Developmental Psychology'),
            ('clinical_psychology', 'Clinical Psychology'),
            ('social_psychology', 'Social Psychology'),
            ('neuropsychology', 'Neuropsychology'),
            ('behavioral_psychology', 'Behavioral Psychology'),
        ],
        'education': [
            ('curriculum_design', 'Curriculum Design'),
            ('educational_technology', 'Educational Technology'),
            ('classroom_management', 'Classroom Management'),
            ('special_education', 'Special Education'),
            ('early_childhood_education', 'Early Childhood Education'),
            ('educational_psychology', 'Educational Psychology'),
        ],
        'art': [
            ('drawing', 'Drawing'),
            ('painting', 'Painting'),
            ('sculpture', 'Sculpture'),
            ('digital_art', 'Digital Art'),
            ('art_history', 'Art History'),
            ('graphic_design', 'Graphic Design'),
            ('photography', 'Photography'),
        ],
        'literature': [
            ('classical_literature', 'Classical Literature'),
            ('modern_literature', 'Modern Literature'),
            ('poetry', 'Poetry'),
            ('drama', 'Drama'),
            ('literary_criticism', 'Literary Criticism'),
            ('world_literature', 'World Literature'),
        ],
        'mathematics': [
            ('algebra', 'Algebra'),
            ('calculus', 'Calculus'),
            ('geometry', 'Geometry'),
            ('statistics', 'Statistics'),
            ('discrete_math', 'Discrete Mathematics'),
            ('linear_algebra', 'Linear Algebra'),
            ('number_theory', 'Number Theory'),
        ],
        'nature and environment': [
            ('animals', 'Animals'),
            ('plants', 'Plants'),
            ('weather', 'Weather'),
            ('recycling', 'Recycling'),
            ('conservation', 'Conservation'),
        ],
        'languages': [
            ('english', 'English'),
            ('spanish', 'Spanish'),
            ('french', 'French'),
            ('german', 'German'),
            ('chinese', 'Chinese'),
            ('japanese', 'Japanese'),
            ('arabic', 'Arabic'),
            ('russian', 'Russian'),
            ('portuguese', 'Portuguese'),
            ('italian', 'Italian'),
        ],
        'history': [
            ('ancient_history', 'Ancient History'),
            ('medieval_history', 'Medieval History'),
            ('modern_history', 'Modern History'),
            ('world_war_history', 'World War History'),
            ('history_of_science', 'History of Science'),
            ('history_of_art', 'History of Art'),
            ('history_of_music', 'History of Music'),
        ],
        'geography': [
        ('world_geography', 'World Geography'),
        ('countries_and_capitals', 'Countries and Capitals'),
        ('maps_and_globes', 'Maps and Globes'),
        ('oceans_and_continents', 'Oceans and Continents'),
        ('climate_zones', 'Climate Zones'),
        ('landforms', 'Landforms'),
        ('natural_disasters', 'Natural Disasters'),
        ('environmental_issues', 'Environmental Issues'),
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
