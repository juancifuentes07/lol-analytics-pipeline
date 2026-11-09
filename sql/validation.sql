-- Conteo total de filas cargadas (esperado: 1000 = 100 partidas x 10 jugadores)
SELECT COUNT(*) FROM raw.match_participants;

-- Winrate total (mín. 10 partidas), sin remakes.
SELECT 
	COUNT (*) AS partidas,
	ROUND(AVG(win::int), 3) AS winrate
FROM raw.match_participants
WHERE riot_id_game_name = 'Juanpa ツ'
    AND game_duration_s >= 600
    AND game_ended_in_early_surrender IS NOT TRUE;

-- Winrate por campeón (mín. 5 partidas), sin remakes. 
-- Debe coincidir con Pandas.
SELECT 
	champion_name AS campeon,
	COUNT (*) AS partidas,
	ROUND(AVG(win::int), 3) AS winrate
FROM raw.match_participants
WHERE riot_id_game_name = 'Juanpa ツ'
	AND game_duration_s >= 600
	AND game_ended_in_early_surrender IS NOT TRUE
GROUP BY campeon
HAVING COUNT (*) >= 5
ORDER BY winrate DESC