SELECT
    EXTRACT(EPOCH FROM (processing_started_at - created_at)) AS queue_time,
    EXTRACT(EPOCH FROM (processing_ended_at - processing_started_at)) AS processing_time
FROM video_inputs
WHERE TRUE
    AND status = 'COMPLETED'
    AND processing_started_at IS NOT NULL
    AND processing_ended_at IS NOT NULL
    AND CAST(created_at AS DATE) BETWEEN :start_date AND :end_date
    AND (:sites IS NULL OR site = ANY(:sites));