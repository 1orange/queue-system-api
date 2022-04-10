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
 ORDER 
    BY priority DESC,
       arrived ASC;