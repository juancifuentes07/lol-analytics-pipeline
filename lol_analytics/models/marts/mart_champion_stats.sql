select
    champion_name,
    count(*) as games,
    round(avg(win::int), 3) as winrate,
    round(avg(kda), 2) as avg_kda,
    round(avg(kills), 2) as avg_kills
from {{ ref('fct_my_matches') }}
group by champion_name