CREATE TABLE IF NOT EXISTS characters (
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS scenes (
    id TEXT PRIMARY KEY,
    title TEXT,
    summary TEXT,
    order_index INTEGER
);

CREATE TABLE IF NOT EXISTS scene_characters (
    scene_id TEXT,
    character_id TEXT
);

CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY,
    source_id TEXT,
    target_id TEXT,
    type TEXT,
    description TEXT
);
