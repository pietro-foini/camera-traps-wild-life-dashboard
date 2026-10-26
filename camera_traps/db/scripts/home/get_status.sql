SELECT
    status::text AS status,
    COUNT(id) AS total
FROM video_inputs
WHERE TRUE
    AND CAST(created_at AS date) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM created_at) >= :start_hour
    AND EXTRACT(HOUR FROM created_at) < :end_hour
    AND (:sites IS NULL OR site = ANY(:sites))
GROUP BY
    status