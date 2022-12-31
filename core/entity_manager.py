from core.entity import Entity


class EntityManager:
    def __init__(self, map_):
        self.entities = []
        self.map = map_

    def add_entity(self, entity: Entity) -> Entity:
        """Add a new entity into the entity list."""
        self.entities.append(entity)
        return entity

    def tick(self, delta):
        for entity in self.entities:
            entity.update(delta, self.map)
