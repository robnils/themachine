# themachine

Facial and speech recognition app inspired by The Machine from Person of Interest. The goal is to detect faces, determine if they are known or unknown, and if unknown, ask the person to identify themselves. Once identified, save the person so that next time the app is run, it can recognnise and greet the person.

# todo 
A current problem is that running the facial recognition and speech recognition concurrently block each other. I tried to solve this using threads but ran into difficulty sharing data between them. I plan to use two flask microservices instead to overcome them.
