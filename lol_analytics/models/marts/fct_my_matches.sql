select
    match_id,
    champion_name,
    team_position,
    win,
    kills,
    deaths,
    assists,
    kda,
    gold_earned,
    vision_score,
    queue_id,
    game_duration_s,
    game_start,
    date_trunc('month', game_start)::date as game_month
from {{ ref('stg_match_participants') }}
where puuid = '{{ env_var("PUUID") }}'