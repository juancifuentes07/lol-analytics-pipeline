-- Una fila por team_position con games, winrate y avg_kda

select
    team_position,
    count(*) as games,
    round(avg(win::int), 3) as winrate,
    round(avg(kda), 2) as avg_kda
from {{ ref('fct_my_matches') }}
group by team_position