SELECT
    vi.id AS id,
    vi.filename,
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
    AND vi.processing_ended_at IS NOT NULL
    AND vi.created_at >= CAST(:start_date AS date)
    AND vi.created_at < (CAST(:end_date AS date) + INTERVAL '1 day')
    AND NOT EXISTS (
        SELECT 1
        FROM video_validations AS val
        WHERE val.video_input_id = vi.id
    );