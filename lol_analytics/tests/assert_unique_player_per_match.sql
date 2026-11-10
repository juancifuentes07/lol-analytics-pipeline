select match_id, puuid, count(*) as n
from {{ ref('stg_match_participants') }}
group by match_id, puuid
having count(*) > 1