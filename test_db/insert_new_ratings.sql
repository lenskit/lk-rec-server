DELETE FROM rating WHERE "user" = 4 AND timestamp = 1597161800;
DELETE FROM rating WHERE "user" = 0;

INSERT INTO rating SELECT 4, item, rating, 1597161800 FROM rating r1 WHERE "user" = 2 AND r1.item NOT IN (SELECT r2.item FROM rating r2 WHERE r2."user" = 4);
INSERT INTO rating SELECT 0, item, rating, 1597161800 FROM rating WHERE "user" = 2 ON CONFLICT DO NOTHING;