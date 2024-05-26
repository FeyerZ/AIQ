from django.shortcuts import render

def print_images(request):
    planets = [
            {
                'name': 'Mercury',
                'image': 'planetgame/Mercury_in_true_color.jpg',
                'facts': [
                    'Mercury is the closest planet to the Sun and has the shortest orbit in the solar system, taking only 88 Earth days to complete one revolution.',
                    'Despite being so close to the Sun, Mercury is not the hottest planet; Venus holds that title due to its thick, heat-trapping atmosphere.'
                ]
            },
            {
                'name': 'Venus',
                'image': 'planetgame/Venus-real_color.jpg',
                'facts': [
                    'Venus has a very slow rotation and takes longer to rotate on its axis than it does to orbit the Sun, meaning a day on Venus is longer than a year.',
                    'Its atmosphere is composed mostly of carbon dioxide with clouds of sulfuric acid, causing a runaway greenhouse effect with surface temperatures hot enough to melt lead.'
                ]
            },
            {
                'name': 'Earth',
                'image': 'planetgame/The_Earth_seen_from_Apollo_17.jpg',
                'facts': [
                    'Earth is the only planet known to support life, having a perfect balance of air, water, land, and temperature conditions.',
                    'It has a unique and dynamic surface with 71% covered by oceans, and its atmosphere is composed of 78% nitrogen, 21% oxygen, and trace amounts of other gases.'
                ]
            },
            {
                'name': 'Mars',
                'image': 'planetgame/OSIRIS_Mars_true_color.jpg',
                'facts': [
                    'Mars is known as the Red Planet due to its reddish color, which comes from iron oxide, or rust, on its surface.',
                    'It has the tallest volcano in the solar system, Olympus Mons, which is about 13.6 miles (22 kilometers) high, nearly three times the height of Mount Everest.'
                ]
            },
            {
                'name': 'Jupiter',
                'image': 'planetgame/Jupiter_and_its_shrunken_Great_Red_Spot.jpg',
                'facts': [
                    'Jupiter is the largest planet in our solar system, having a mass that is more than twice that of all the other planets combined.',
                    'It has a Great Red Spot, a huge storm that has been raging for at least 400 years and is about 1.3 times as wide as Earth.'
                ]
            },
            {
                'name': 'Saturn',
                'image': 'planetgame/Saturn_during_Equinox2.jpg',
                'facts': [
                    'Saturn is famous for its stunning rings, which are primarily composed of ice particles, with some rock debris and dust.',
                    'It is the least dense planet in our solar system; its density is less than water, meaning it would float if there were a large enough body of water.'
                ]
            },
            {
                'name': 'Uranus',
                'image': 'planetgame/Uranus2.jpg',
                'facts': [
                    'Uranus is unique in that it rotates on its side, meaning it orbits the Sun with its axis tilted nearly parallel to the plane of the solar system.',
                    'It has a very faint ring system and is known for its blue-green color, caused by methane in its atmosphere absorbing red light.'
                ]
            },
            {
               'name': 'Neptune',
                  'image': 'planetgame/Neptune_Full.jpg',
                  'facts': [
                     'Neptune has the strongest winds in the solar system, with speeds reaching up to 1,200 miles per hour (2,000 kilometers per hour).',
                    'It is known for its deep blue color, which is a result of methane in its atmosphere, similar to Uranus.'
                ]
            },
            {
               'name': 'Pluto',
               'image': 'planetgame/pluto.jpg',
               'facts': [
                   'Pluto is classified as a dwarf planet and is part of the Kuiper Belt, a region of the solar system beyond the orbit of Neptune filled with small icy bodies.',
                   'It has five known moons, with the largest, Charon, being about half the size of Pluto itself, making it more like a binary system than a planet with a moon.']
              }
             ]

            context = {
            'planets': planets
        }
        return render(request, 'planetgame/printable_images.html', context)
def rhyme(request):
    return render(request, 'planetgame/rhyme.html')