import random
import uuid

groups = [
    (
        ['object_' + str(random.randint(1, 100)) for _ in range(0, random.randint(2, 6))], #objects in group
        'SIMILAR_OBJECTS',
        uuid.uuid4()
)
    for _ in range(100)
]