SELECT
    vi.id AS id,
    vi.filename,
    vi.site AS site,
    COALESCE(vo.trackers, 0) AS trackers,
    COALESCE(vo.species, 0) AS species,
    COALESCE(vo.labels, '{}') AS labels,
    vi.created_at AT TIME ZONE 'Europe/Rome' AS date
FROM video_inputs AS vi
LEFT JOIN (
    SELECT
        video_input_id,
        COUNT(DISTINCT tracker_id) AS trackers,
        COUNT(DISTINCT label) AS species,
        ARRAY_AGG(DISTINCT label) AS labels
    FROM video_outputs
    GROUP BY video_input_id
) AS vo
    ON vi.id = vo.video_input_id
WHERE TRUE
    AND vi.status = 'COMPLETED'
    AND CAST(vi.created_at AS DATE) BETWEEN :start_date AND :end_date
    AND EXTRACT(HOUR FROM vi.created_at) >= :start_hour
    AND EXTRACT(HOUR FROM vi.created_at) < :end_hour
    AND (:sites IS NULL OR vi.site = ANY(:sites))
    AND NOT EXISTS (
        SELECT 1
        FROM video_validations AS val
        WHERE val.video_input_id = vi.id
    );