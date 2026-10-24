SELECT
    ipt.id AS id,
    ipt.filename,
    COALESCE(opt.trackers, 0) AS trackers,
    COALESCE(opt.species, 0) AS species,
    COALESCE(opt.labels, '{}') AS labels,
    ipt.created_at AT TIME ZONE 'Europe/Rome' AS date
FROM video_inputs AS ipt
LEFT JOIN (
    SELECT
        video_input_id,
        COUNT(DISTINCT tracker_id) AS trackers,
        COUNT(DISTINCT label) AS species,
        ARRAY_AGG(DISTINCT label) AS labels
    FROM video_outputs
    GROUP BY video_input_id
) AS opt
    ON ipt.id = opt.video_input_id
WHERE TRUE
    AND ipt.processing_ended_at IS NOT NULL
    AND ipt.created_at >= CAST(:start_date AS date)
    AND ipt.created_at < (CAST(:end_date AS date) + INTERVAL '1 day')
    AND NOT EXISTS (
        SELECT 1
        FROM video_validations AS val
        WHERE val.video_input_id = ipt.id
    );