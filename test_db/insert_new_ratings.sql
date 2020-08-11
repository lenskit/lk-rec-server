DELETE FROM ratings WHERE userId = 4 AND timestamp = 1597161800;
DELETE FROM ratings WHERE userId = 0;

INSERT INTO ratings (SELECT 4, itemId, rating, 1597161800 FROM ratings r1 WHERE userId = 2 AND r1.itemId NOT IN (SELECT r2.itemId FROM ratings r2 WHERE r2.userId = 4));
INSERT INTO ratings (SELECT 0, itemId, rating, 1597161800 FROM ratings WHERE userId = 2) ON CONFLICT DO NOTHING;