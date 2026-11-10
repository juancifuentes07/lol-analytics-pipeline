select
    match_id,
    puuid,
    riot_id_game_name,
    champion_name,
    team_position,
    win,
    kills,
    deaths,
    assists,
    round(
    	(kills + assists)::numeric
    	/ case when deaths = 0 then 1 else deaths end,
    	2
	) as kda,
    gold_earned,
    vision_score,
    queue_id,
    game_duration_s,
    game_start
from {{ source('raw', 'match_participants') }}
where game_duration_s >= 600
  and game_ended_in_early_surrender is not true