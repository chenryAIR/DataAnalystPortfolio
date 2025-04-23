SELECT 
  test_assignment,
  SUM(order_binary) as order_count,
  SUM(order_binary_non) as order_count_non,
  COUNT(*) as order_count_N
FROM
(
  SELECT 
   f.item_id,
   f.test_assignment,
   f.test_number,
   MAX(CASE WHEN o.item_id IS NULL THEN 0 ELSE 1 END) AS order_binary,
   MAX(CASE WHEN o.item_id IS NULL THEN 1 ELSE 0 END) AS order_binary_non
  FROM 
    dsv1069.final_assignments AS f LEFT JOIN dsv1069.orders AS o
    ON 
      f.item_id = o.item_id AND
      date(o.created_at) >= DATE(f.test_start_date) AND
      DATE_PART('day',o.created_at - f.test_start_date) <= 30
  WHERE test_number = 'item_test_2'
  GROUP BY 
    f.item_id,
    f.test_assignment,
    f.test_number
) AS binary_calc
GROUP BY test_assignment;