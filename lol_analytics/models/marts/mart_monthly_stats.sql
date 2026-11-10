-- Una fila por game month con games, winrate y avg_kda

select 
    game_month,
    count(*) as games,
    round(avg(win::int), 3) as winrate,
    round(avg(kda), 2) as avg_kda
from {{ ref('fct_my_matches') }}
group by game_month