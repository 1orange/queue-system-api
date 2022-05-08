-- name: reset_order_number#
ALTER SEQUENCE order_number_seq RESTART WITH 1;

-- name: insert_client<!
INSERT INTO sq.queue(condition_id)
     VALUES (:condition_id)
  RETURNING uuid, order_number, arrived;

-- name: get_current_client^
SELECT uuid, 
       arrived, 
       name as condition_name,
       order_number
  FROM sq.queue AS Q 
       JOIN 
       sq.conditions AS C 
       ON 
       Q.condition_id = C.id
 ORDER 
    BY priority DESC,
       arrived ASC;

-- name: delete_current_client!
DELETE FROM sq.queue
 WHERE uuid = (
      SELECT uuid
        FROM sq.queue
       ORDER 
             BY priority DESC,
             arrived ASC
       LIMIT 1
 );

--name: get_queue_status
SELECT uuid, 
       arrived, 
       name as condition_name,
       order_number
  FROM sq.queue AS Q 
       JOIN 
       sq.conditions AS C 
       ON 
       Q.condition_id = C.id
 WHERE uuid
       NOT IN (
               SELECT uuid
                FROM sq.queue
               ORDER
                  BY priority DESC
               LIMIT 1
              )
 ORDER 
    BY priority DESC,
       arrived ASC
 LIMIT 5;

-- name: get_all_conditions
SELECT id,
       name,
       description,
       complexity
  FROM sq.conditions;

-- name: insert_condition!
INSERT INTO sq.conditions(name, description, complexity)
     VALUES (:name, :desc, :complexity);

--name: delete_condition!
DELETE FROM sq.conditions
 WHERE id = :id;

-- name: find_client_by_id^
SELECT count(*) as count
  FROM sq.queue
 WHERE uuid = :uuid;