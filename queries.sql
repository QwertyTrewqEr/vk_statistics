SELECT COUNT(*) - COUNT(DISTINCT user_id, group_id) as dupl from vk.subscribtions;
SELECT group_id, COUNT(*) as CNT FROM vk.subscribtions GROUP BY group_id order by CNT DESC limit 10;
select count(*) as cnt from vk.subscribtions;