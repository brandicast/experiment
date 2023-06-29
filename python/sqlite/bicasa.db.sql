BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "configuration" (
	"id"	INTEGER NOT NULL UNIQUE,
	"rootpath"	TEXT,
	"enable_facial_recognition"	INTEGER DEFAULT 0,
	"version"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "photos" (
	"id"	INTEGER NOT NULL UNIQUE,
	"fullpath"	TEXT NOT NULL UNIQUE,
	"filename"	TEXT NOT NULL,
	"size"	INTEGER NOT NULL,
	"last_access_time"	INTEGER NOT NULL,
	"exif"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "faces" (
	"id"	INTEGER NOT NULL UNIQUE,
	"photo_id"	INTEGER NOT NULL,
	"facial_area"	INTEGER NOT NULL,
	"embedding"	BLOB NOT NULL,
	"thumbnail"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
create virtual table vss_faces using vss0(
	embedding(384)
);
COMMIT;
