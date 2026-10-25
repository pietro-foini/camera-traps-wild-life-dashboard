SELECT
    COUNT(DISTINCT (vi.id)) AS total_videos,
    COUNT(vv.id) AS total_validated,
    COUNT(vv.id) FILTER (WHERE vv.is_modified = TRUE OR vv.tracker_id IS NULL) AS total_modified
FROM video_validations AS vv
JOIN video_inputs AS vi ON vv.video_input_id = vi.id
WHERE TRUE
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND (:sites IS NULL OR vi.site = ANY(:sites))