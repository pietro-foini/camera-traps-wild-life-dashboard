SELECT
    CASE
        WHEN vv.tracker_id IS NULL THEN 'Added'
        WHEN vv.is_modified = TRUE THEN 'Relabeled'
        ELSE 'Confirmed'
    END AS validation_status,
    COUNT(vv.id) AS total
FROM video_validations AS vv
JOIN video_inputs AS vi ON vv.video_input_id = vi.id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND (:sites IS NULL OR vi.site = ANY(:sites))
GROUP BY 1