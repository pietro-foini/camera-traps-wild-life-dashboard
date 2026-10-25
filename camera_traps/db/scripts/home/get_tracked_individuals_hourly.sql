SELECT
    date_trunc('hour', vi.created_at AT TIME ZONE 'Europe/Rome') AS created_at,
    COUNT(DISTINCT (vo.video_input_id, vo.tracker_id)) AS total
FROM video_inputs AS vi
LEFT JOIN video_outputs AS vo ON vi.id = vo.video_input_id
WHERE TRUE
    AND CAST((vi.created_at AT TIME ZONE 'Europe/Rome') AS DATE) BETWEEN :start_date AND :end_date
    AND (:sites IS NULL OR vi.site = ANY(:sites))
GROUP BY 1
ORDER BY 1