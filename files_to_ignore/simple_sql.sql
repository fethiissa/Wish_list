use employee_jobs_db;

select * from registered_users;

update  jobs set assigned_to_id = NULL where id = 27;

select * from jobs where posted_by_id = 16;

delete from jobs where id = 21;


 table assigned_tasks;

DELETE FROM `employee_jobs_db`.`assigned_tasks`
WHERE job_id = 18 and user_id = 16;


INSERT INTO `employee_jobs_db`.`assigned_tasks`
(`job_id`,
`user_id`)
VALUES
(1,
16);
