SELECT
    vi.site,
    vv.label AS species,
    CASE
        WHEN vv.tracker_id IS NULL THEN 'Added'
        WHEN vv.is_modified = TRUE THEN 'Relabeled'
        ELSE 'Confirmed'
    END AS validation_status,
    COUNT(vv.id) AS total
FROM video_validations AS vv
INNER JOIN video_inputs AS vi ON vv.video_input_id = vi.id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
    AND (:species IS NULL OR vv.label = ANY(:species))
GROUP BY 1, 2, 3
ORDER BY total DESC