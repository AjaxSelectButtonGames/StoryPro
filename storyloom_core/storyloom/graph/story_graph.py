class StoryGraph:
    def __init__(self):
        self.edges = {}

    def connect(self, a_id: str, b_id: str, reason: str = ""):
        self.edges.setdefault(a_id, []).append((b_id, reason))
        self.edges.setdefault(b_id, []).append((a_id, reason))

    def connections_for(self, entity_id: str):
        return self.edges.get(entity_id, [])
