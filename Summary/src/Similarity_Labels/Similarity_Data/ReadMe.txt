Sql to create convince me and createdebtae gay marriage posts.
/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights.csv 

saved in file 
use iac;
select p.dataset_id,p.discussion_id, p.post_id, d.discussion_url, t.text,d.topic_id
from  discussions as d 
join 
posts as p
on p.dataset_id=d.dataset_id and
   p.discussion_id = d.discussion_id
   

join texts as t

on t.dataset_id=p.dataset_id and
    t.text_id=p.text_id

where (d.dataset_id=2 and d.topic_id=8)   or (d.dataset_id=3 and d.topic_id=8) ;